"""
Cities routes
"""
from flask import request, jsonify, make_response
import json
import re
import traceback
from database import execute_query, execute_update
from utils.helpers import abort_with_message, require_admin_auth
from data.city_localities import get_localities_for_city

# Mapping of important/well-known cities per state
IMPORTANT_CITIES_BY_STATE = {
    'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Nellore', 'Kurnool', 'Rajahmundry', 'Tirupati', 'Kakinada', 'Kadapa', 'Anantapur'],
    'Arunachal Pradesh': ['Itanagar', 'Naharlagun', 'Tawang', 'Bomdila'],
    'Assam': ['Guwahati', 'Silchar', 'Dibrugarh', 'Jorhat', 'Nagaon', 'Tinsukia', 'Tezpur'],
    'Bihar': ['Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Purnia', 'Darbhanga', 'Arrah', 'Bihar Sharif'],
    'Chhattisgarh': ['Raipur', 'Bhilai', 'Bilaspur', 'Korba', 'Raigarh', 'Jagdalpur', 'Ambikapur', 'Durg'],
    'Goa': ['Panaji', 'Vasco da Gama', 'Margao', 'Mapusa', 'Ponda'],
    'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar', 'Jamnagar', 'Gandhinagar', 'Anand', 'Bharuch', 'Gandhidham'],
    'Haryana': ['Gurgaon', 'Faridabad', 'Panipat', 'Ambala', 'Yamunanagar', 'Rohtak', 'Hisar', 'Karnal', 'Sonipat'],
    'Himachal Pradesh': ['Shimla', 'Dharamshala', 'Solan', 'Mandi', 'Kullu', 'Manali', 'Palampur', 'Chamba'],
    'Jharkhand': ['Ranchi', 'Jamshedpur', 'Dhanbad', 'Bokaro', 'Hazaribagh', 'Deoghar', 'Giridih'],
    'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mangalore', 'Belagavi', 'Gulbarga', 'Davangere', 'Shimoga', 'Tumkur', 'Udupi'],
    'Kerala': ['Kochi', 'Thiruvananthapuram', 'Kozhikode', 'Thrissur', 'Kollam', 'Kannur', 'Alappuzha', 'Kottayam', 'Palakkad', 'Malappuram'],
    'Madhya Pradesh': ['Indore', 'Bhopal', 'Gwalior', 'Jabalpur', 'Ujjain', 'Sagar', 'Dewas', 'Satna', 'Ratlam', 'Rewa', 'Burhanpur'],
    'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad', 'Solapur', 'Thane', 'Pimpri-Chinchwad', 'Kalyan', 'Vasai-Virar', 'Navi Mumbai', 'Amravati', 'Kolhapur', 'Sangli'],
    'Manipur': ['Imphal', 'Thoubal', 'Bishnupur'],
    'Meghalaya': ['Shillong', 'Tura', 'Jowai'],
    'Mizoram': ['Aizawl', 'Lunglei', 'Champhai'],
    'Nagaland': ['Kohima', 'Dimapur', 'Mokokchung'],
    'Odisha': ['Bhubaneswar', 'Cuttack', 'Rourkela', 'Berhampur', 'Sambalpur', 'Puri', 'Balasore'],
    'Punjab': ['Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala', 'Bathinda', 'Mohali', 'Pathankot', 'Hoshiarpur'],
    'Rajasthan': ['Jaipur', 'Jodhpur', 'Kota', 'Bikaner', 'Ajmer', 'Udaipur', 'Bhilwara', 'Alwar', 'Bharatpur', 'Sikar'],
    'Sikkim': ['Gangtok', 'Namchi', 'Mangan'],
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tirunelveli', 'Erode', 'Vellore', 'Thoothukudi', 'Dindigul'],
    'Telangana': ['Hyderabad', 'Warangal', 'Nizamabad', 'Karimnagar', 'Ramagundam', 'Khammam', 'Mahbubnagar', 'Nalgonda'],
    'Tripura': ['Agartala', 'Udaipur', 'Dharmanagar'],
    'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Agra', 'Varanasi', 'Allahabad', 'Prayagraj', 'Meerut', 'Bareilly', 'Aligarh', 'Moradabad', 'Saharanpur', 'Gorakhpur', 'Jhansi', 'Mathura', 'Firozabad'],
    'Uttarakhand': ['Dehradun', 'Haridwar', 'Roorkee', 'Haldwani', 'Rudrapur', 'Rishikesh', 'Nainital', 'Mussoorie'],
    'West Bengal': ['Kolkata', 'Howrah', 'Durgapur', 'Asansol', 'Siliguri', 'Bardhaman', 'Malda', 'Kharagpur', 'Krishnanagar'],
    'Dadra and Nagar Haveli and Daman and Diu': ['Daman', 'Diu', 'Silvassa'],
    'Lakshadweep': ['Kavaratti', 'Agatti'],
    'Puducherry': ['Puducherry', 'Karaikal'],
    'Andaman and Nicobar Islands': ['Port Blair', 'Diglipur']
}


def register_cities_routes(app):
    """Register cities routes"""
    
    @app.route("/api/cities", methods=["GET"])
    def get_active_cities():
        """Get all active cities (public endpoint) - returns all cities from active states"""
        try:
            query = """
                SELECT 
                    c.name,
                    c.state
                FROM cities c
                WHERE c.is_active = 1
                ORDER BY c.state, c.name
            """
            cities = execute_query(query)
            
            # Return all active cities (not just important ones)
            # When a state is activated, all its cities become active and should appear in dropdowns
            filtered_cities = []
            if cities:
                for city in cities:
                    city_name = city.get('name', '').strip()
                    state_name = city.get('state', '').strip()
                    
                    if city_name and state_name:
                        filtered_cities.append({
                            'name': city_name,
                            'state': state_name
                        })
            
            data = {
                "success": True,
                "cities": filtered_cities
            }
            
            # Support JSONP if callback parameter is provided
            callback = request.args.get('callback')
            if callback:
                # Validate callback name to prevent XSS
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                    response = make_response(f"{callback}({json.dumps(data)});")
                    response.headers['Content-Type'] = 'application/javascript'
                    return response
                else:
                    # Invalid callback name, return regular JSON
                    return jsonify({'error': 'Invalid callback parameter'}), 400
            
            return jsonify(data)
        except Exception as e:
            print(f"Error fetching active cities: {str(e)}")
            traceback.print_exc()
            # Support JSONP even for errors
            callback = request.args.get('callback')
            if callback:
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                    response = make_response(f"{callback}({{'success': False, 'cities': []}});")
                    response.headers['Content-Type'] = 'application/javascript'
                    return response
            abort_with_message(500, f"Error fetching active cities: {str(e)}")
    
    @app.route("/api/admin/cities", methods=["GET"])
    @require_admin_auth
    def get_all_cities():
        """Get all cities (admin endpoint - includes inactive cities)"""
        try:
            query = """
                SELECT 
                    c.id,
                    c.name,
                    c.state,
                    c.is_active,
                    c.created_at,
                    c.updated_at
                FROM cities c
                ORDER BY c.state, c.name
            """
            cities = execute_query(query)
            
            # Convert datetime objects to ISO format strings for JSON serialization
            def convert_datetime_to_iso(obj):
                """Recursively convert datetime objects to ISO format strings"""
                if hasattr(obj, 'isoformat'):
                    return obj.isoformat()
                if isinstance(obj, dict):
                    return {k: convert_datetime_to_iso(v) for k, v in obj.items()}
                if isinstance(obj, list):
                    return [convert_datetime_to_iso(v) for v in obj]
                return obj
            
            # Convert datetime fields in cities data
            cities_data = [convert_datetime_to_iso(dict(city)) for city in cities] if cities else []
            
            return jsonify(cities_data)
        except Exception as e:
            print(f"Error fetching all cities: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching all cities: {str(e)}")
    
    @app.route("/api/admin/cities/bulk", methods=["GET", "POST"])
    @require_admin_auth
    def bulk_update_cities():
        """Bulk update cities (admin endpoint) - updates is_active status for multiple cities
        GET: Returns list of all cities for bulk update
        POST: Updates is_active status for multiple cities"""
        try:
            if request.method == "GET":
                # GET request - return all cities for bulk update
                query = """
                    SELECT name, state, is_active
                    FROM cities
                    ORDER BY state, name
                """
                cities = execute_query(query)
                
                return jsonify({
                    'success': True,
                    'cities': cities if cities else []
                })
            
            # POST request - bulk update cities
            data = request.get_json()
            if not data or 'cities' not in data:
                return jsonify({'success': False, 'message': 'Missing cities data'}), 400
            
            cities = data.get('cities', [])
            if not isinstance(cities, list) or len(cities) == 0:
                return jsonify({'success': False, 'message': 'Cities must be a non-empty array'}), 400
            
            # Use INSERT ... ON DUPLICATE KEY UPDATE to handle both inserts and updates
            # This ensures cities are created if they don't exist, or updated if they do
            query = """
                INSERT INTO cities (name, state, is_active)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    is_active = VALUES(is_active),
                    updated_at = CURRENT_TIMESTAMP
            """
            
            updated_count = 0
            for city in cities:
                name = city.get('name', '').strip()
                state = city.get('state', '').strip()
                is_active = city.get('is_active', False)
                
                # Validate required fields
                if not name or not state:
                    continue
                
                # Convert boolean to int (0 or 1) for MySQL
                is_active_int = 1 if is_active else 0
                
                try:
                    execute_update(query, (name, state, is_active_int))
                    updated_count += 1
                except Exception as e:
                    print(f"Error updating city {name}, {state}: {str(e)}")
                    # Continue with other cities even if one fails
                    continue
            
            return jsonify({
                'success': True,
                'message': f'Successfully updated {updated_count} cities',
                'updated_count': updated_count
            })
        except Exception as e:
            print(f"Error in bulk update cities: {str(e)}")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'message': f'Error updating cities: {str(e)}'
            }), 500
    
    @app.route("/api/localities", methods=["GET"])
    def get_localities_by_city():
        """Get all unique localities/areas for a given city (public endpoint)
        Returns ALL localities from both active and inactive properties to ensure
        all available areas are shown in dropdowns"""
        try:
            city = request.args.get('city', '').strip()
            
            if not city:
                return jsonify({
                    "success": True,
                    "localities": []
                })
            
            # Query both residential_properties and plot_properties tables
            # to get ALL unique localities for the given city (including from inactive properties)
            # Use TRIM and case-insensitive matching to handle any whitespace or case issues
            query = """
                SELECT DISTINCT locality
                FROM (
                    SELECT DISTINCT TRIM(locality) as locality
                    FROM residential_properties
                    WHERE LOWER(TRIM(city)) = LOWER(TRIM(%s)) 
                      AND locality IS NOT NULL 
                      AND TRIM(locality) != ''
                    UNION
                    SELECT DISTINCT TRIM(locality) as locality
                    FROM plot_properties
                    WHERE LOWER(TRIM(city)) = LOWER(TRIM(%s)) 
                      AND locality IS NOT NULL 
                      AND TRIM(locality) != ''
                ) AS all_localities
                WHERE locality IS NOT NULL AND locality != ''
                ORDER BY locality
            """
            # First, try to get localities from the static mapping file
            locality_list = get_localities_for_city(city)
            
            # Debug logging
            print(f"[API] Looking up localities for city: '{city}' (trimmed: '{city.strip()}')")
            print(f"[API] Found {len(locality_list)} localities from static mapping")
            
            # If no localities found in static file, query the database
            if not locality_list:
                # Trim the city parameter to ensure exact match
                city_trimmed = city.strip()
                localities = execute_query(query, (city_trimmed, city_trimmed))
                
                # If no results with exact match, try partial match (in case of city name variations)
                if not localities or len(localities) == 0:
                    fallback_query = """
                        SELECT DISTINCT locality
                        FROM (
                            SELECT DISTINCT TRIM(locality) as locality
                            FROM residential_properties
                            WHERE LOWER(TRIM(city)) LIKE LOWER(CONCAT('%%', TRIM(%s), '%%'))
                              AND locality IS NOT NULL 
                              AND TRIM(locality) != ''
                            UNION
                            SELECT DISTINCT TRIM(locality) as locality
                            FROM plot_properties
                            WHERE LOWER(TRIM(city)) LIKE LOWER(CONCAT('%%', TRIM(%s), '%%'))
                              AND locality IS NOT NULL 
                              AND TRIM(locality) != ''
                        ) AS all_localities
                        WHERE locality IS NOT NULL AND locality != ''
                        ORDER BY locality
                    """
                    localities = execute_query(fallback_query, (city_trimmed, city_trimmed))
                
                # Extract locality names from database
                if localities:
                    for loc in localities:
                        locality_name = loc.get('locality', '').strip()
                        if locality_name:
                            locality_list.append(locality_name)
            
            # Remove duplicates and sort
            locality_list = sorted(list(set(locality_list)))
            
            # Ensure we always return a valid response structure
            data = {
                "success": True,
                "localities": locality_list if locality_list else []
            }
            
            # Additional debug logging
            print(f"[API] Returning {len(data['localities'])} localities for city '{city}'")
            if len(data['localities']) == 0:
                print(f"[API] WARNING: No localities found for city '{city}'. Check static mapping and database.")
            
            # Support JSONP if callback parameter is provided
            callback = request.args.get('callback')
            if callback:
                # Validate callback name to prevent XSS
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                    response = make_response(f"{callback}({json.dumps(data)});")
                    response.headers['Content-Type'] = 'application/javascript'
                    return response
                else:
                    # Invalid callback name, return regular JSON
                    return jsonify({'error': 'Invalid callback parameter'}), 400
            
            return jsonify(data)
        except Exception as e:
            print(f"Error fetching localities for city {city}: {str(e)}")
            traceback.print_exc()
            # Support JSONP even for errors
            callback = request.args.get('callback')
            if callback:
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                    response = make_response(f"{callback}({{'success': False, 'localities': []}});")
                    response.headers['Content-Type'] = 'application/javascript'
                    return response
            abort_with_message(500, f"Error fetching localities: {str(e)}")