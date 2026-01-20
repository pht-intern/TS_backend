"""
Amenities routes
"""
from flask import request, jsonify, make_response
import json
import re
import traceback
from database import execute_query
from utils.helpers import abort_with_message


def register_amenities_routes(app):
    """Register amenities routes"""
    
    @app.route("/api/amenities", methods=["GET"])
    def get_amenities():
        """Get all available amenities/features (master list + any from properties)"""
        try:
            # Master list of all possible amenities
            master_amenities = [
                "club_house",
                "security",
                "24hr_backup",
                "rain_water_harvesting",
                "maintenance_staff",
                "intercom",
                "garden",
                "community_hall",
                "electricity_full",
                "electricity_partial",
                "basketball_court",
                "play_area",
                "badminton_court",
                "swimming_pool",
                "tennis_court",
                "gymnasium",
                "indoor_games",
                "banks_atm",
                "cafeteria",
                "library",
                "health_facilities",
                "recreation_facilities",
                "wifi_broadband",
                "temple"
            ]
            
            # Also get any additional amenities that might be in the database
            # Use the unified property_features table (as per database schema)
            db_amenity_names = []
            try:
                query = """
                    SELECT DISTINCT feature_name as name
                    FROM property_features
                    WHERE feature_name IS NOT NULL AND feature_name != ''
                    ORDER BY feature_name ASC
                """
                db_amenities = execute_query(query)
                db_amenity_names = [a['name'] for a in db_amenities] if db_amenities else []
            except Exception as db_error:
                # If query fails, just use master list
                print(f"Warning: Could not fetch amenities from database: {str(db_error)}")
                db_amenity_names = []
            
            # Combine master list with any additional amenities from database, remove duplicates
            all_amenities = list(set(master_amenities + db_amenity_names))
            all_amenities.sort()
            
            data = {
                "success": True,
                "amenities": all_amenities
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
            print(f"Error fetching amenities: {str(e)}")
            traceback.print_exc()
            # Support JSONP even for errors
            callback = request.args.get('callback')
            if callback:
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                    response = make_response(f"{callback}({{'success': False, 'amenities': []}});")
                    response.headers['Content-Type'] = 'application/javascript'
                    return response
            abort_with_message(500, f"Error fetching amenities: {str(e)}")
