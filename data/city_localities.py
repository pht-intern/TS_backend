"""
City to Localities/Areas Mapping
This module fetches city localities dynamically from Google Maps Places API.
Results are cached to minimize API calls and improve performance.
"""
import os
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
from config import PROJECT_ROOT, ENV_FILE
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)
else:
    load_dotenv()

try:
    import googlemaps
    GOOGLEMAPS_AVAILABLE = True
except ImportError:
    GOOGLEMAPS_AVAILABLE = False
    print("WARNING: googlemaps library not installed. Install it with: pip install googlemaps")

# Google Maps API key from environment
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

# Initialize Google Maps client if API key is available
gmaps_client = None
if GOOGLEMAPS_AVAILABLE and GOOGLE_MAPS_API_KEY:
    try:
        gmaps_client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        print("✓ Google Maps API client initialized successfully")
    except Exception as e:
        print(f"WARNING: Failed to initialize Google Maps client: {str(e)}")
        gmaps_client = None
elif not GOOGLE_MAPS_API_KEY:
    print("WARNING: GOOGLE_MAPS_API_KEY not found in environment variables. Google Maps API will not be available.")

# Cache configuration
CACHE_DIR = Path(PROJECT_ROOT) / "backend" / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = CACHE_DIR / "city_localities_cache.json"
CACHE_EXPIRY_DAYS = 30  # Cache results for 30 days

# In-memory cache for faster access
_memory_cache: Dict[str, Dict] = {}

def load_cache() -> Dict:
    """Load cache from file if it exists and is not expired"""
    global _memory_cache
    
    if not CACHE_FILE.exists():
        return {}
    
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        # Filter out expired entries
        current_time = time.time()
        valid_cache = {}
        for city, data in cache_data.items():
            cached_time = data.get('cached_at', 0)
            if current_time - cached_time < (CACHE_EXPIRY_DAYS * 24 * 60 * 60):
                valid_cache[city] = data
        
        _memory_cache = valid_cache
        return valid_cache
    except Exception as e:
        print(f"Error loading cache: {str(e)}")
        return {}

def save_cache(cache_data: Dict):
    """Save cache to file"""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving cache: {str(e)}")

def fetch_localities_from_google_maps(city_name: str) -> List[str]:
    """
    Fetch localities/neighborhoods for a city using Google Maps Places API.
    
    Args:
        city_name (str): Name of the city
    
    Returns:
        List[str]: List of locality names
    """
    if not gmaps_client:
        print(f"[Google Maps] API not available for city '{city_name}'")
        return []
    
    localities = []
    
    try:
        # Step 1: Find the city using Text Search
        city_query = f"{city_name}, India"
        print(f"[Google Maps] Searching for city: {city_query}")
        
        places_result = gmaps_client.places(query=city_query, type='locality')
        
        if not places_result.get('results'):
            # Try without "India" suffix
            places_result = gmaps_client.places(query=city_name, type='locality')
        
        if not places_result.get('results'):
            print(f"[Google Maps] City '{city_name}' not found")
            return []
        
        # Get the first result (most relevant city)
        city_place = places_result['results'][0]
        city_location = city_place.get('geometry', {}).get('location', {})
        
        if not city_location:
            print(f"[Google Maps] No location found for city '{city_name}'")
            return []
        
        lat = city_location.get('lat')
        lng = city_location.get('lng')
        
        print(f"[Google Maps] Found city '{city_name}' at coordinates: {lat}, {lng}")
        
        # Step 2: Search for neighborhoods/sublocalities using Nearby Search
        # Search for different types of places that represent localities
        place_types = ['neighborhood', 'sublocality', 'sublocality_level_1', 'sublocality_level_2']
        
        all_places = set()
        
        for place_type in place_types:
            try:
                # Nearby search for neighborhoods
                nearby_result = gmaps_client.places_nearby(
                    location=(lat, lng),
                    radius=20000,  # 20km radius
                    type=place_type
                )
                
                if nearby_result.get('results'):
                    for place in nearby_result.get('results', []):
                        place_name = place.get('name', '').strip()
                        if place_name and len(place_name) > 2:
                            all_places.add(place_name)
                
                # Also try Text Search for neighborhoods in the city
                text_query = f"neighborhoods in {city_name}"
                text_result = gmaps_client.places(query=text_query)
                
                if text_result.get('results'):
                    for place in text_result.get('results', []):
                        place_name = place.get('name', '').strip()
                        if place_name and len(place_name) > 2:
                            all_places.add(place_name)
                
                # Small delay to respect rate limits
                time.sleep(0.1)
                
            except Exception as e:
                print(f"[Google Maps] Error searching for {place_type} in {city_name}: {str(e)}")
                continue
        
        # Step 3: Use Autocomplete to get more locality suggestions
        try:
            autocomplete_result = gmaps_client.places_autocomplete(
                input_text=f"{city_name} ",
                types='(cities)',
                components={'country': 'in'}  # Restrict to India
            )
            
            # Also search for specific areas/neighborhoods
            for suggestion in autocomplete_result[:10]:  # Limit to first 10
                description = suggestion.get('description', '')
                # Extract locality names from descriptions like "Locality, City, State, India"
                parts = description.split(',')
                if len(parts) > 0:
                    locality_name = parts[0].strip()
                    if locality_name and locality_name.lower() != city_name.lower():
                        all_places.add(locality_name)
        except Exception as e:
            print(f"[Google Maps] Error in autocomplete for {city_name}: {str(e)}")
        
        # Step 4: Use Place Details to get address components
        try:
            place_id = city_place.get('place_id')
            if place_id:
                place_details = gmaps_client.place(place_id=place_id, fields=['address_component'])
                
                address_components = place_details.get('result', {}).get('address_components', [])
                for component in address_components:
                    types = component.get('types', [])
                    if 'sublocality' in types or 'neighborhood' in types or 'sublocality_level_1' in types:
                        name = component.get('long_name', '').strip()
                        if name:
                            all_places.add(name)
        except Exception as e:
            print(f"[Google Maps] Error getting place details for {city_name}: {str(e)}")
        
        localities = sorted(list(all_places))
        print(f"[Google Maps] Found {len(localities)} localities for '{city_name}'")
        
        return localities
        
    except Exception as e:
        print(f"[Google Maps] Error fetching localities for '{city_name}': {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def get_localities_for_city(city_name: str) -> List[str]:
    """
    Get localities for a given city name.
    First checks cache, then Google Maps API if needed.
    Returns a list of localities or empty list if city not found.
    
    Args:
        city_name (str): Name of the city (case-insensitive)
    
    Returns:
        list: List of locality names for the city
    """
    if not city_name:
        return []
    
    # Normalize city name (trim whitespace, lowercase for cache key)
    city_normalized = city_name.strip()
    city_key = city_normalized.lower()
    
    # Load cache if memory cache is empty
    if not _memory_cache:
        load_cache()
    
    # Check cache first
    if city_key in _memory_cache:
        cached_data = _memory_cache[city_key]
        localities = cached_data.get('localities', [])
        print(f"[City Mapping] Cache hit for '{city_normalized}': {len(localities)} localities")
        return localities.copy()
    
    # Cache miss - fetch from Google Maps API
    print(f"[City Mapping] Cache miss for '{city_normalized}', fetching from Google Maps...")
    localities = fetch_localities_from_google_maps(city_normalized)
    
    # Store in cache
    if localities:
        _memory_cache[city_key] = {
            'localities': localities,
            'cached_at': time.time(),
            'city_name': city_normalized
        }
        save_cache(_memory_cache)
        print(f"[City Mapping] Cached {len(localities)} localities for '{city_normalized}'")
    else:
        # Cache empty result to avoid repeated API calls for cities with no results
        _memory_cache[city_key] = {
            'localities': [],
            'cached_at': time.time(),
            'city_name': city_normalized
        }
        save_cache(_memory_cache)
        print(f"[City Mapping] No localities found for '{city_normalized}', cached empty result")
    
    return localities.copy()

def get_all_cities() -> List[str]:
    """
    Get all cities that have cached localities.
    Note: This only returns cities that have been queried and cached.
    For a complete list of cities, use the database or cities API endpoint.
    
    Returns:
        list: List of city names that have cached data
    """
    if not _memory_cache:
        load_cache()
    
    cities = []
    for city_key, data in _memory_cache.items():
        city_name = data.get('city_name', city_key)
        if city_name:
            cities.append(city_name)
    
    return sorted(cities)

def clear_cache(city_name: Optional[str] = None):
    """
    Clear cache for a specific city or all cities.
    
    Args:
        city_name (str, optional): City name to clear cache for. If None, clears all cache.
    """
    global _memory_cache
    
    if city_name:
        city_key = city_name.strip().lower()
        if city_key in _memory_cache:
            del _memory_cache[city_key]
            save_cache(_memory_cache)
            print(f"Cache cleared for '{city_name}'")
    else:
        _memory_cache = {}
        if CACHE_FILE.exists():
            CACHE_FILE.unlink()
        print("All cache cleared")

# Initialize cache on module load
load_cache()
