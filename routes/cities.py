"""
Cities routes
"""
from flask import request, jsonify, make_response
import json
import re
import traceback
from database import execute_query
from utils.helpers import abort_with_message, require_admin_auth

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
        """Get all active cities (public endpoint) - returns only important cities for active states"""
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
            
            # Group active cities by state to determine which states are active
            active_states = set()
            cities_by_state = {}
            
            if cities:
                for city in cities:
                    city_name = city.get('name', '').strip()
                    state_name = city.get('state', '').strip()
                    
                    if city_name and state_name:
                        active_states.add(state_name)
                        if state_name not in cities_by_state:
                            cities_by_state[state_name] = []
                        cities_by_state[state_name].append(city_name)
            
            # Filter to only include important cities for active states
            filtered_cities = []
            for state in active_states:
                important_cities = IMPORTANT_CITIES_BY_STATE.get(state, [])
                if important_cities:
                    # Get all active cities for this state
                    active_cities_in_state = cities_by_state.get(state, [])
                    # Create a case-insensitive lookup map
                    active_cities_lower = {city.lower(): city for city in active_cities_in_state}
                    important_cities_lower = {city.lower(): city for city in important_cities}
                    
                    # Filter to only include important cities that are also active
                    for important_city_lower, important_city in important_cities_lower.items():
                        if important_city_lower in active_cities_lower:
                            # Use the actual city name from database (preserves exact casing)
                            filtered_cities.append({
                                'name': active_cities_lower[important_city_lower],
                                'state': state
                            })
                else:
                    # If no important cities list exists for this state, include all active cities
                    for city_name in cities_by_state.get(state, []):
                        filtered_cities.append({
                            'name': city_name,
                            'state': state
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