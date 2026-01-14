"""
Amenities routes
"""
from flask import request, jsonify
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
            
            return jsonify({
                "success": True,
                "amenities": all_amenities
            })
        except Exception as e:
            print(f"Error fetching amenities: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching amenities: {str(e)}")
