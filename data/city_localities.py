"""
City to Localities/Areas Mapping
This module fetches city localities dynamically from Pelias geocoding API.
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
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("WARNING: requests library not installed. Install it with: pip install requests")

# Pelias API endpoint from environment
# Default to geocode.earth public API, but can be overridden for self-hosted instances
PELIAS_API_URL = os.getenv("PELIAS_API_URL", "https://api.geocode.earth/v1")

# Validate Pelias API URL
if not PELIAS_API_URL.endswith('/v1'):
    if PELIAS_API_URL.endswith('/'):
        PELIAS_API_URL = PELIAS_API_URL.rstrip('/') + '/v1'
    else:
        PELIAS_API_URL = PELIAS_API_URL.rstrip('/') + '/v1'

if REQUESTS_AVAILABLE:
    print(f"✓ Pelias API client initialized with endpoint: {PELIAS_API_URL}")
else:
    print("WARNING: requests library not available. Pelias API will not be available.")

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

def fetch_localities_from_pelias(city_name: str) -> List[str]:
    """
    Fetch localities/neighborhoods for a city using Pelias geocoding API.
    
    Args:
        city_name (str): Name of the city
    
    Returns:
        List[str]: List of locality names
    """
    if not REQUESTS_AVAILABLE:
        print(f"[Pelias] API not available for city '{city_name}'")
        return []
    
    localities = set()
    
    try:
        # Step 1: Find the city using search API
        city_query = f"{city_name}, India"
        print(f"[Pelias] Searching for city: {city_query}")
        
        search_url = f"{PELIAS_API_URL}/search"
        params = {
            'text': city_query,
            'size': 10,
            'layers': 'locality,localadmin',  # Focus on cities/localities
            'boundary.country': 'IN'  # Restrict to India
        }
        
        response = requests.get(search_url, params=params, timeout=10)
        
        if response.status_code != 200:
            # Try without "India" suffix
            params['text'] = city_name
            response = requests.get(search_url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"[Pelias] API request failed with status {response.status_code} for city '{city_name}'")
            return []
        
        data = response.json()
        features = data.get('features', [])
        
        if not features:
            print(f"[Pelias] City '{city_name}' not found")
            return []
        
        # Get the first result (most relevant city)
        city_feature = features[0]
        city_properties = city_feature.get('properties', {})
        city_geometry = city_feature.get('geometry', {})
        
        if not city_geometry or 'coordinates' not in city_geometry:
            print(f"[Pelias] No coordinates found for city '{city_name}'")
            return []
        
        coordinates = city_geometry['coordinates']
        lon, lat = coordinates[0], coordinates[1]
        
        print(f"[Pelias] Found city '{city_name}' at coordinates: {lat}, {lon}")
        
        # Step 2: Search for neighborhoods/localities in the city using autocomplete
        # Autocomplete is better for finding sub-localities
        autocomplete_url = f"{PELIAS_API_URL}/autocomplete"
        
        # Try multiple search strategies
        search_queries = [
            f"{city_name}",
            f"neighborhoods in {city_name}",
            f"areas in {city_name}",
            f"localities in {city_name}"
        ]
        
        for query in search_queries:
            try:
                autocomplete_params = {
                    'text': query,
                    'size': 20,
                    'layers': 'neighbourhood,locality,localadmin',  # Include neighborhoods
                    'boundary.country': 'IN',
                    'focus.point.lat': lat,
                    'focus.point.lon': lon
                }
                
                autocomplete_response = requests.get(
                    autocomplete_url, 
                    params=autocomplete_params, 
                    timeout=10
                )
                
                if autocomplete_response.status_code == 200:
                    autocomplete_data = autocomplete_response.json()
                    autocomplete_features = autocomplete_data.get('features', [])
                    
                    for feature in autocomplete_features:
                        props = feature.get('properties', {})
                        
                        # Extract locality/neighborhood names
                        # Pelias provides different fields depending on the result type
                        name = props.get('name', '').strip()
                        locality = props.get('locality', '').strip()
                        neighbourhood = props.get('neighbourhood', '').strip()
                        localadmin = props.get('localadmin', '').strip()
                        
                        # Add valid locality names
                        for loc_name in [name, locality, neighbourhood, localadmin]:
                            if loc_name and len(loc_name) > 2:
                                # Filter out the city name itself and common non-locality terms
                                loc_lower = loc_name.lower()
                                city_lower = city_name.lower()
                                if (loc_lower != city_lower and 
                                    loc_lower not in ['india', 'indian', 'city', 'town'] and
                                    city_lower not in loc_lower):  # Avoid city name in locality
                                    localities.add(loc_name)
                
                # Small delay to respect rate limits
                time.sleep(0.2)
                
            except Exception as e:
                print(f"[Pelias] Error in autocomplete query '{query}': {str(e)}")
                continue
        
        # Step 3: Use reverse geocoding to find nearby localities
        try:
            reverse_url = f"{PELIAS_API_URL}/reverse"
            reverse_params = {
                'point.lat': lat,
                'point.lon': lon,
                'size': 50,
                'layers': 'neighbourhood,locality,localadmin'
            }
            
            reverse_response = requests.get(reverse_url, params=reverse_params, timeout=10)
            
            if reverse_response.status_code == 200:
                reverse_data = reverse_response.json()
                reverse_features = reverse_data.get('features', [])
                
                for feature in reverse_features:
                    props = feature.get('properties', {})
                    name = props.get('name', '').strip()
                    locality = props.get('locality', '').strip()
                    neighbourhood = props.get('neighbourhood', '').strip()
                    
                    for loc_name in [name, locality, neighbourhood]:
                        if loc_name and len(loc_name) > 2:
                            loc_lower = loc_name.lower()
                            city_lower = city_name.lower()
                            if (loc_lower != city_lower and 
                                loc_lower not in ['india', 'indian', 'city', 'town'] and
                                city_lower not in loc_lower):
                                localities.add(loc_name)
        except Exception as e:
            print(f"[Pelias] Error in reverse geocoding for {city_name}: {str(e)}")
        
        # Step 4: Search for specific areas using broader search
        try:
            # Search with different locality-related terms
            locality_terms = ['area', 'sector', 'colony', 'nagar', 'layout', 'extension']
            
            for term in locality_terms:
                search_params = {
                    'text': f"{term} {city_name}",
                    'size': 15,
                    'layers': 'neighbourhood,locality',
                    'boundary.country': 'IN',
                    'focus.point.lat': lat,
                    'focus.point.lon': lon
                }
                
                search_response = requests.get(search_url, params=search_params, timeout=10)
                
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    search_features = search_data.get('features', [])
                    
                    for feature in search_features:
                        props = feature.get('properties', {})
                        name = props.get('name', '').strip()
                        
                        if name and len(name) > 2:
                            loc_lower = name.lower()
                            city_lower = city_name.lower()
                            if (loc_lower != city_lower and 
                                city_lower not in loc_lower):
                                localities.add(name)
                
                time.sleep(0.1)
                
        except Exception as e:
            print(f"[Pelias] Error in locality term search for {city_name}: {str(e)}")
        
        # Convert to sorted list
        localities_list = sorted(list(localities))
        print(f"[Pelias] Found {len(localities_list)} localities for '{city_name}'")
        
        return localities_list
        
    except requests.exceptions.RequestException as e:
        print(f"[Pelias] Network error fetching localities for '{city_name}': {str(e)}")
        return []
    except Exception as e:
        print(f"[Pelias] Error fetching localities for '{city_name}': {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def get_localities_for_city(city_name: str) -> List[str]:
    """
    Get localities for a given city name.
    First checks cache, then Pelias API if needed.
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
    
    # Cache miss - fetch from Pelias API
    print(f"[City Mapping] Cache miss for '{city_normalized}', fetching from Pelias...")
    localities = fetch_localities_from_pelias(city_normalized)
    
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
