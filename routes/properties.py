"""
Properties routes
"""
from flask import request, jsonify, current_app, make_response
from datetime import datetime
from decimal import Decimal
import traceback
from database import execute_query, execute_update, execute_insert
from models import PropertyType, PropertyStatus
from schemas import PaginatedResponse
from utils.helpers import (
    get_pagination_params, calculate_pages, normalize_image_url, error_response, success_response,
    process_image_urls, require_admin_auth, safe_int, safe_float
)
from config import IMAGES_DIR


def register_properties_routes(app):
    """Register properties routes"""
    
    @app.route("/api/properties", methods=["GET", "OPTIONS"])
    def get_properties_route():
        """Get all properties with filtering and pagination"""
        # Handle OPTIONS request for CORS preflight
        if request.method == "OPTIONS":
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        return get_properties()
    
    @app.route("/api/properties", methods=["POST"])
    @require_admin_auth
    def create_property_route():
        """Create a new property"""
        return create_property()
    
    def get_properties():
        """Get all properties with filtering and pagination"""
        try:
            pagination = get_pagination_params()
            offset = (pagination.page - 1) * pagination.limit
            
            # Get query parameters
            type_str = request.args.get('type')
            status_str = request.args.get('status')
            min_price = request.args.get('min_price', type=float)
            max_price = request.args.get('max_price', type=float)
            location = request.args.get('location')
            is_featured = request.args.get('is_featured', type=lambda x: x.lower() == 'true' if x else None)
            is_active = request.args.get('is_active', default='true', type=lambda x: x.lower() == 'true' if x else True)
            
            # Build WHERE clause
            is_active_int = 1 if is_active else 0
            conditions = ["is_active = %s"]
            params = [is_active_int]
            
            if type_str:
                try:
                    prop_type = PropertyType(type_str)
                    conditions.append("type = %s")
                    params.append(prop_type.value)
                except ValueError:
                    pass
            
            if status_str:
                try:
                    prop_status = PropertyStatus(status_str)
                    conditions.append("status = %s")
                    params.append(prop_status.value)
                except ValueError:
                    pass
            
            if min_price is not None:
                conditions.append("price >= %s")
                params.append(min_price)
            
            if max_price is not None:
                conditions.append("price <= %s")
                params.append(max_price)
            
            if location:
                # Search in both city and locality fields
                conditions.append("(LOWER(city) LIKE %s OR LOWER(locality) LIKE %s)")
                params.append(f"%{location.lower()}%")
                params.append(f"%{location.lower()}%")
            
            if is_featured is not None:
                is_featured_int = 1 if is_featured else 0
                conditions.append("is_featured = %s")
                params.append(is_featured_int)
            
            where_clause = " AND ".join(conditions)
            
            # Build separate conditions for residential and plot properties
            # For plots, exclude type filter since they don't have a type field
            type_filter_index = None
            if type_str and "type = %s" in where_clause:
                # Find the index of type filter in conditions
                for i, cond in enumerate(conditions):
                    if cond == "type = %s":
                        type_filter_index = i
                        break
            
            # Build params for residential (include type filter) and plot (exclude type filter)
            residential_params = list(params)
            plot_params = [p for i, p in enumerate(params) if i != type_filter_index] if type_filter_index is not None else list(params)
            
            # Build where clauses
            residential_where = where_clause
            plot_where = " AND ".join([c for i, c in enumerate(conditions) if i != type_filter_index]) if type_filter_index is not None else where_clause
            
            # Get total count from both tables
            count_res = execute_query(f"SELECT COUNT(*) as total FROM residential_properties WHERE {residential_where}", tuple(residential_params)) if residential_where else [{'total': 0}]
            count_plot = execute_query(f"SELECT COUNT(*) as total FROM plot_properties WHERE {plot_where}", tuple(plot_params)) if plot_where else [{'total': 0}]
            total = (count_res[0]['total'] if count_res else 0) + (count_plot[0]['total'] if count_plot else 0)
            
            # Query both tables separately and combine results
            import time
            query_start = time.time()
            
            # Query residential properties
            residential_query = f"""
                SELECT 
                    id, city, locality, property_name as title, property_name, 
                    unit_type, bedrooms, bathrooms, buildup_area as area, buildup_area, carpet_area, 
                    super_built_up_area, price, price_text, price_negotiable, price_includes_registration,
                    type, status, property_status, description,
                    location_link, directions, length, breadth,
                    builder, configuration, total_flats, total_floors, total_acres,
                    is_featured, is_active, created_at, updated_at,
                    'residential' as property_category,
                    NULL as plot_area, NULL as plot_length, NULL as plot_breadth,
                    NULL as project_name,
                    type as property_type
                FROM residential_properties
                WHERE {residential_where}
                ORDER BY created_at DESC
            """
            residential_props = execute_query(residential_query, tuple(residential_params)) if residential_where else []
            
            # Query plot properties (only if no type filter is set, since plots don't have a type field)
            plot_props = []
            if type_filter_index is None:
                plot_query = f"""
                    SELECT 
                        id, city, locality, project_name as title, project_name as property_name,
                        NULL as unit_type, 0 as bedrooms, 0 as bathrooms, plot_area as area, NULL as buildup_area, NULL as carpet_area,
                        NULL as super_built_up_area, price, price_text, price_negotiable, price_includes_registration,
                        'plot' as type, status, property_status, description,
                        location_link, directions, NULL as length, NULL as breadth,
                        builder, NULL as configuration, NULL as total_flats, NULL as total_floors, total_acres,
                        is_featured, is_active, created_at, updated_at,
                        'plot' as property_category,
                        plot_area, plot_length, plot_breadth,
                        project_name
                    FROM plot_properties
                    WHERE {plot_where}
                    ORDER BY created_at DESC
                """
                plot_props = execute_query(plot_query, tuple(plot_params)) if plot_where else []
            
            # Combine and sort by created_at
            all_properties = residential_props + plot_props
            all_properties.sort(key=lambda x: x.get('created_at', datetime.min), reverse=True)
            
            # Apply pagination
            properties = all_properties[offset:offset + pagination.limit]
            
            query_time = time.time() - query_start
            
            if query_time > 1.0:  # Log slow queries (> 1 second)
                print(f"[PERF] Slow query detected: {query_time:.2f}s for page {pagination.page}, limit {pagination.limit}")
            
            # Fetch primary images for each property and normalize image URLs
            normalized_properties = []
            for prop in properties:
                prop_dict = dict(prop)
                property_id = prop_dict.get('id')
                property_category = prop_dict.get('property_category', 'residential')
                
                # Fetch primary image from the new image tables (project, floorplan, masterplan)
                if property_id:
                    try:
                        if property_category == 'residential':
                            primary_image_query = """
                                SELECT image_url 
                                FROM residential_property_images
                                WHERE property_id = %s
                                ORDER BY created_at ASC, image_order ASC 
                                LIMIT 1
                            """
                        else:
                            primary_image_query = """
                                SELECT image_url 
                                FROM plot_property_images
                                WHERE property_id = %s
                                ORDER BY created_at ASC, image_order ASC 
                                LIMIT 1
                            """
                        
                        primary_images = execute_query(primary_image_query, (property_id,))
                        if primary_images and primary_images[0].get('image_url'):
                            normalized_first_image = normalize_image_url(primary_images[0]['image_url'])
                            prop_dict['primary_image'] = normalized_first_image
                            # Populate images array with the first image for frontend display
                            prop_dict['images'] = [{'image_url': normalized_first_image}]
                    except Exception as e:
                        # If image fetch fails, continue without images
                        print(f"Warning: Could not fetch images for property {property_id}: {str(e)}")
                
                # Normalize existing primary_image if it exists (fallback - in case property table has primary_image field)
                if 'primary_image' in prop_dict and prop_dict['primary_image']:
                    prop_dict['primary_image'] = normalize_image_url(prop_dict['primary_image'])
                    # If images array is empty but primary_image exists, populate it
                    if 'images' not in prop_dict or not prop_dict.get('images'):
                        prop_dict['images'] = [{'image_url': prop_dict['primary_image']}]
                
                # Ensure images array exists
                if 'images' not in prop_dict:
                    prop_dict['images'] = []
                
                # Construct location from city and locality if not already present
                if 'location' not in prop_dict or not prop_dict.get('location'):
                    city = prop_dict.get('city', '')
                    locality = prop_dict.get('locality', '')
                    if city and locality:
                        prop_dict['location'] = f"{city}, {locality}"
                    elif city:
                        prop_dict['location'] = city
                    elif locality:
                        prop_dict['location'] = locality
                    else:
                        prop_dict['location'] = 'Location not specified'
                
                # Convert TINYINT(1) to boolean for price_negotiable and price_includes_registration
                if 'price_negotiable' in prop_dict:
                    prop_dict['price_negotiable'] = bool(prop_dict['price_negotiable'])
                if 'price_includes_registration' in prop_dict:
                    prop_dict['price_includes_registration'] = bool(prop_dict['price_includes_registration'])
                
                # Convert numeric fields to proper types
                if 'bathrooms' in prop_dict and prop_dict['bathrooms'] is not None:
                    prop_dict['bathrooms'] = float(prop_dict['bathrooms'])
                if 'area' in prop_dict and prop_dict['area'] is not None:
                    prop_dict['area'] = int(float(prop_dict['area']))
                
                normalized_properties.append(prop_dict)
            
            response = PaginatedResponse(
                total=total,
                page=pagination.page,
                limit=pagination.limit,
                pages=calculate_pages(total, pagination.limit),
                items=normalized_properties
            )
            result = jsonify(response.dict())
            result.headers['Access-Control-Allow-Origin'] = '*'
            return result
        except Exception as e:
            error_msg = str(e)
            print(f"Error fetching properties: {error_msg}")
            traceback.print_exc()
            error_resp, status_code = error_response(f"Error fetching properties: {error_msg}", 500)
            error_resp.headers['Access-Control-Allow-Origin'] = '*'
            return error_resp, status_code
    
    def create_property():
        """Create a new property (residential or plot) based on property_type"""
        try:
            data = request.get_json()
            if not data:
                return error_response("Invalid request data", 400)
            
            property_type = data.get("property_type")
            if not property_type:
                # Try to infer from other fields
                if data.get("unit_type") or data.get("bedrooms") is not None:
                    property_type = "apartments"  # Default to apartments
                else:
                    property_type = "plot_properties"
            
            # Determine if it's a plot property or residential property
            is_plot = property_type == "plot_properties"
            
            # Map frontend property_type to DB type
            _type_map = {
                "individual_house": "house",
                "apartments": "apartment", 
                "villas": "villa",
                "plot_properties": "plot"
            }
            db_type = _type_map.get(property_type, property_type)
            
            # Handle status and property_status
            _status = data.get("status", "sale")
            _pstat = None if _status in ("sale", "rent") else data.get("property_status")
            
            if is_plot:
                # Create plot property
                city = data.get("city")
                locality = data.get("locality")
                project_name = data.get("property_name") or data.get("project_name")
                
                if not city or not locality or not project_name:
                    return error_response("City, locality, and project name are required", 400)
                
                plot_area = safe_float(data.get("plot_area"), 0.0)
                plot_length = safe_float(data.get("plot_length") or data.get("length"), 0.0)
                plot_breadth = safe_float(data.get("plot_breadth") or data.get("breadth"), 0.0)
                price = safe_float(data.get("price"), 0.0)
                
                if price <= 0:
                    return error_response("Price is required and must be greater than 0", 400)
                
                insert_query = """
                    INSERT INTO plot_properties (
                        city, locality, project_name, plot_area, plot_length, plot_breadth,
                        price, price_text, price_negotiable, price_includes_registration,
                        status, property_status, description,
                        location_link, directions, builder, total_acres,
                        is_featured, is_active
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                property_id = execute_insert(insert_query, (
                    city, locality, project_name, plot_area, plot_length, plot_breadth,
                    price, data.get("price_text"), 
                    1 if data.get("price_negotiable") else 0,
                    1 if data.get("price_includes_registration") else 0,
                    _status, _pstat, data.get("description"),
                    data.get("location_link"), data.get("directions"),
                    data.get("builder"), safe_float(data.get("total_acres"), None),
                    1 if data.get("is_featured") else 0,
                    1 if data.get("is_active", True) else 0
                ))
                
                img_table = "plot_property_images"
                feature_category = "plot"
            else:
                # Create residential property
                city = data.get("city")
                locality = data.get("locality")
                property_name = data.get("property_name")
                
                if not city or not locality or not property_name:
                    return error_response("City, locality, and property name are required", 400)
                
                # Validate unit_type - must be one of: 'rk', 'bhk', '4plus' (database constraint)
                unit_type = data.get("unit_type", "bhk")
                if unit_type not in ("rk", "bhk", "4plus"):
                    # If invalid, determine based on bedrooms
                    bedrooms_temp = safe_int(data.get("bedrooms"), 1)
                    if bedrooms_temp == 0:
                        unit_type = "rk"
                    elif bedrooms_temp >= 4:
                        unit_type = "4plus"
                    else:
                        unit_type = "bhk"
                bedrooms = safe_int(data.get("bedrooms"), 1)
                bathrooms = safe_float(data.get("bathrooms") or data.get("bathrooms_count"), 0.0)
                buildup_area = safe_float(data.get("buildup_area"), 0.0)
                carpet_area = safe_float(data.get("carpet_area"), 0.0)
                super_buildup_area = safe_float(data.get("super_buildup_area") or data.get("super_buildup_area"), None)
                price = safe_float(data.get("price"), 0.0)
                
                if price <= 0:
                    return error_response("Price is required and must be greater than 0", 400)
                
                # Map property_type to DB type
                db_property_type = _type_map.get(property_type, "apartment")
                
                insert_query = """
                    INSERT INTO residential_properties (
                        city, locality, property_name, unit_type, bedrooms, bathrooms,
                        buildup_area, carpet_area, super_built_up_area,
                        price, price_text, price_negotiable, price_includes_registration,
                        type, status, property_status, description,
                        location_link, directions, length, breadth,
                        builder, configuration, total_flats, total_floors, total_acres,
                        is_featured, is_active
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                property_id = execute_insert(insert_query, (
                    city, locality, property_name, unit_type, bedrooms, bathrooms,
                    buildup_area, carpet_area, super_buildup_area,
                    price, data.get("price_text"),
                    1 if data.get("price_negotiable") else 0,
                    1 if data.get("price_includes_registration") else 0,
                    db_property_type, _status, _pstat, data.get("description"),
                    data.get("location_link"), data.get("directions"),
                    safe_float(data.get("length"), None),
                    safe_float(data.get("breadth"), None),
                    data.get("builder"), data.get("configuration"),
                    safe_int(data.get("total_flats"), None),
                    safe_int(data.get("total_floors"), None),
                    safe_float(data.get("total_acres"), None),
                    1 if data.get("is_featured") else 0,
                    1 if data.get("is_active", True) else 0
                ))
                
                img_table = "residential_property_images"
                feature_category = "residential"
            
            # Handle images from gallery
            image_gallery = data.get("image_gallery") or []
            images = data.get("images") or []
            
            # Process gallery images if available
            if image_gallery:
                try:
                    for idx, gallery_item in enumerate(image_gallery):
                        image_url = gallery_item.get("image_url")
                        if image_url:
                            # Process and normalize image URL
                            processed_urls = process_image_urls([image_url], None)
                            if processed_urls:
                                image_category = gallery_item.get("category", "project")
                                # Map frontend categories to DB categories
                                category_map = {
                                    "project": "project",
                                    "floorplan": "floorplan",
                                    "masterplan": "masterplan"
                                }
                                db_category = category_map.get(image_category, "project")
                                
                                # Insert into property images table
                                execute_insert(
                                    f"INSERT INTO {img_table} (property_id, image_url, image_category, image_order) VALUES (%s, %s, %s, %s)",
                                    (property_id, processed_urls[0], db_category, idx)
                                )
                except Exception as img_err:
                    print(f"Warning: could not insert gallery images for property {property_id}: {img_err}")
            
            # Fallback to flat images list if gallery is empty
            if not image_gallery and images:
                try:
                    processed = process_image_urls(images, None)
                    for idx, url in enumerate(processed):
                        if url:
                            # Insert into property images table
                            execute_insert(
                                f"INSERT INTO {img_table} (property_id, image_url, image_category, image_order) VALUES (%s, %s, %s, %s)",
                                (property_id, url, 'project', idx)
                            )
                except Exception as img_err:
                    print(f"Warning: could not insert images for property {property_id}: {img_err}")
            
            # Handle features/amenities
            features = data.get("features") or data.get("amenities") or []
            if features:
                try:
                    for name in features:
                        if name:
                            execute_insert(
                                "INSERT IGNORE INTO property_features (property_category, property_id, feature_name) VALUES (%s, %s, %s)",
                                (feature_category, property_id, name)
                            )
                except Exception as fe:
                    print(f"Warning: could not insert features for property {property_id}: {fe}")
            
            return jsonify({"message": "Property created successfully", "id": property_id}), 201
        except ValueError as e:
            error_msg = f"Invalid data type: {str(e)}"
            print(f"Error creating property: {error_msg}")
            print(f"Received data: {request.get_json()}")
            traceback.print_exc()
            return error_response(error_msg, 400)
        except Exception as e:
            error_msg = f"Error creating property: {str(e)}"
            print(error_msg)
            print(f"Received data: {request.get_json()}")
            traceback.print_exc()
            return error_response(error_msg, 500)
    
    @app.route("/api/properties/<int:property_id>", methods=["GET"])
    def get_property(property_id: int):
        """Get a single property by ID with images and features"""
        try:
            # Check residential_properties first (minimal columns to avoid missing-column errors)
            residential_query = """
                SELECT 
                    id, city, locality, property_name as title, property_name, 
                    unit_type, bedrooms, bathrooms, buildup_area as area, buildup_area, carpet_area, 
                    super_built_up_area, price, price_text, price_negotiable, price_includes_registration,
                    type, status, property_status, description,
                    location_link, directions, length, breadth,
                    builder, configuration, total_flats, total_floors, total_acres,
                    is_featured, is_active, created_at, updated_at,
                    'residential' as property_category,
                    NULL as plot_area, NULL as plot_length, NULL as plot_breadth,
                    NULL as project_name,
                    type as property_type
                FROM residential_properties
                WHERE id = %s
            """
            properties = execute_query(residential_query, (property_id,))
            property_category = 'residential'
            
            # If not found in residential, check plot_properties
            if not properties:
                plot_query = """
                    SELECT 
                        id, city, locality, project_name as title, project_name as property_name,
                        NULL as unit_type, 0 as bedrooms, 0 as bathrooms, plot_area as area, NULL as buildup_area, NULL as carpet_area,
                        NULL as super_built_up_area, price, price_text, price_negotiable, price_includes_registration,
                        'plot' as type, status, property_status, description,
                        location_link, directions, NULL as length, NULL as breadth,
                        builder, NULL as configuration, NULL as total_flats, NULL as total_floors, total_acres,
                        is_featured, is_active, created_at, updated_at,
                        'plot' as property_category,
                        plot_area, plot_length, plot_breadth,
                        project_name,
                        'plot_properties' as property_type
                    FROM plot_properties
                    WHERE id = %s
                """
                properties = execute_query(plot_query, (property_id,))
                property_category = 'plot'
            
            if not properties:
                return error_response("Property not found", 404)
            
            property_data = dict(properties[0])
            
            # Construct location from city and locality if not already present
            if 'location' not in property_data or not property_data.get('location'):
                city = property_data.get('city', '')
                locality = property_data.get('locality', '')
                if city and locality:
                    property_data['location'] = f"{city}, {locality}"
                elif city:
                    property_data['location'] = city
                elif locality:
                    property_data['location'] = locality
                else:
                    property_data['location'] = 'Location not specified'
            
            # Get images (wrap in try/except – some image tables may not exist)
            normalized_images = []
            try:
                if property_category == 'residential':
                    images_query = """
                        SELECT id, property_id, image_url, image_category as image_type, image_order, created_at
                        FROM residential_property_images
                        WHERE property_id = %s
                    """
                else:
                    images_query = """
                        SELECT id, property_id, image_url, image_category as image_type, image_order, created_at
                        FROM plot_property_images
                        WHERE property_id = %s
                    """
                images = execute_query(images_query, (property_id,))
                images = sorted(images, key=lambda x: (x.get('image_order') if x.get('image_order') is not None else 0, str(x.get('created_at') or '')))
                for i, img in enumerate(images):
                    img_dict = dict(img)
                    if img_dict.get('image_url'):
                        img_dict['image_url'] = normalize_image_url(img_dict['image_url'])
                    # Convert datetime to ISO format string
                    if 'created_at' in img_dict and isinstance(img_dict['created_at'], datetime):
                        img_dict['created_at'] = img_dict['created_at'].isoformat()
                    img_dict['is_primary'] = (i == 0)
                    img_dict['image_order'] = img_dict.get('image_order') if img_dict.get('image_order') is not None else i
                    normalized_images.append(img_dict)
            except Exception as img_err:
                print(f"Warning: could not load images for property {property_id}: {img_err}")
            property_data['images'] = normalized_images
            
            # Build image_gallery array for frontend
            image_gallery = []
            for img in normalized_images:
                image_category = img.get('image_type', 'project')
                # Map DB categories to frontend categories
                category_map = {
                    'project': 'project',
                    'floorplan': 'floorplan',
                    'masterplan': 'masterplan'
                }
                frontend_category = category_map.get(image_category, 'project')
                image_gallery.append({
                    'image_url': img.get('image_url'),
                    'category': frontend_category,
                    'title': '',  # Images don't have titles in DB yet
                    'order': img.get('image_order', 0)
                })
            property_data['image_gallery'] = image_gallery
            
            property_data['project_images'] = []
            property_data['floorplan_images'] = []
            property_data['masterplan_images'] = []
            
            # Get features (wrap in try/except – table or column may not exist)
            try:
                features = execute_query(
                    "SELECT feature_name FROM property_features WHERE property_category = %s AND property_id = %s",
                    (property_category, property_id)
                )
                property_data['features'] = [feat.get('feature_name') for feat in features if feat.get('feature_name')]
            except Exception as feat_err:
                print(f"Warning: could not load features for property {property_id}: {feat_err}")
                property_data['features'] = []
            
            # Convert TINYINT(1) to boolean
            if property_data.get('price_negotiable') is not None:
                property_data['price_negotiable'] = bool(property_data['price_negotiable'])
            if property_data.get('price_includes_registration') is not None:
                property_data['price_includes_registration'] = bool(property_data['price_includes_registration'])
            
            # Ensure numeric types (MySQL may return Decimal; avoid jsonify errors)
            def _to_int(v):
                if v is None: return None
                try: return int(float(v))
                except (TypeError, ValueError): return None
            def _to_float(v):
                if v is None: return None
                try: return float(v)
                except (TypeError, ValueError): return None
            property_data['bedrooms'] = _to_int(property_data.get('bedrooms')) or 0
            if 'bathrooms' in property_data: property_data['bathrooms'] = _to_float(property_data['bathrooms'])
            if 'area' in property_data: property_data['area'] = _to_int(property_data['area'])
            if 'price' in property_data: property_data['price'] = _to_float(property_data['price'])
            
            # Convert any remaining Decimals (e.g. in features, plot_area) so jsonify does not fail
            def _decimal_to_float(obj):
                if isinstance(obj, Decimal): return float(obj)
                if isinstance(obj, dict):
                    return {k: _decimal_to_float(v) for k, v in obj.items()}
                if isinstance(obj, list):
                    return [_decimal_to_float(v) for v in obj]
                return obj
            
            # Convert datetime objects to ISO format strings for JSON serialization
            def _datetime_to_iso(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()
                if isinstance(obj, dict):
                    return {k: _datetime_to_iso(v) for k, v in obj.items()}
                if isinstance(obj, list):
                    return [_datetime_to_iso(v) for v in obj]
                return obj
            
            property_data = _decimal_to_float(property_data)
            property_data = _datetime_to_iso(property_data)
            
            return jsonify(property_data)
        except Exception as e:
            print(f"Error fetching property: {str(e)}")
            traceback.print_exc()
            return error_response(f"Error fetching property: {str(e)}", 500)
    
    @app.route("/api/properties/<int:property_id>", methods=["POST"])
    @require_admin_auth
    def update_property(property_id: int):
        """Update a property (residential or plot). Dispatches by which table contains the id."""
        try:
            # Resolve which table has this id
            res = execute_query("SELECT id FROM residential_properties WHERE id = %s", (property_id,))
            if res:
                table, cat = "residential_properties", "residential"
                feature_table = "property_features"
                feature_category = "residential"
                img_table = "residential_property_images"
            else:
                res = execute_query("SELECT id FROM plot_properties WHERE id = %s", (property_id,))
                if not res:
                    return error_response("Property not found", 404)
                table, cat = "plot_properties", "plot"
                feature_table = "property_features"
                feature_category = "plot"
                img_table = "plot_property_images"
            
            data = request.get_json()
            if not data:
                return error_response("Invalid request data", 400)
            
            # Map frontend type to DB enum: individual_house->house, apartments->apartment, villas->villa (avoids chk on type)
            _type_map = {"individual_house": "house", "apartments": "apartment", "villas": "villa"}
            # When status is 'sale' or 'rent', property_status must be NULL (residential_properties_chk_2)
            _status = data.get("status")
            _pstat = None if _status in ("sale", "rent") else data.get("property_status")
            
            def _add(sets, params, key, val, as_int=False, as_float=False):
                if val is None: return
                if as_int and isinstance(val, bool): val = 1 if val else 0
                elif as_int: val = safe_int(val, 0)
                elif as_float: val = safe_float(val, 0.0)
                sets.append(f"{key} = %s")
                params.append(val)
            
            def _set_null(sets, params, key):
                sets.append(f"{key} = %s")
                params.append(None)
            
            sets, params = [], []
            if cat == "residential":
                _add(sets, params, "city", data.get("city"))
                _add(sets, params, "locality", data.get("locality"))
                _add(sets, params, "property_name", data.get("property_name"))
                # Validate unit_type - must be one of: 'rk', 'bhk', '4plus' (database constraint)
                _unit_type = data.get("unit_type", "bhk")
                if _unit_type not in ("rk", "bhk", "4plus"):
                    # If invalid, determine based on bedrooms
                    _bedrooms = safe_int(data.get("bedrooms"), 1)
                    if _bedrooms == 0:
                        _unit_type = "rk"
                    elif _bedrooms >= 4:
                        _unit_type = "4plus"
                    else:
                        _unit_type = "bhk"
                _add(sets, params, "unit_type", _unit_type)
                _add(sets, params, "bedrooms", data.get("bedrooms"), as_int=True)
                _add(sets, params, "bathrooms", data.get("bathrooms") or data.get("bathrooms_count"), as_float=True)
                _add(sets, params, "buildup_area", data.get("buildup_area"), as_float=True)
                _add(sets, params, "carpet_area", data.get("carpet_area"), as_float=True)
                _add(sets, params, "super_built_up_area", data.get("super_buildup_area") or data.get("super_buildup_area"), as_float=True)
                _add(sets, params, "price", data.get("price"), as_float=True)
                _add(sets, params, "price_text", data.get("price_text"))
                if "price_negotiable" in data: _add(sets, params, "price_negotiable", 1 if data.get("price_negotiable") else 0, as_int=True)
                if "price_includes_registration" in data: _add(sets, params, "price_includes_registration", 1 if data.get("price_includes_registration") else 0, as_int=True)
                _add(sets, params, "type", _type_map.get(data.get("type"), data.get("type")))
                _add(sets, params, "status", _status)
                if _status in ("sale", "rent"): _set_null(sets, params, "property_status")
                else: _add(sets, params, "property_status", _pstat)
                _add(sets, params, "description", data.get("description"))
                if "is_featured" in data: _add(sets, params, "is_featured", 1 if data.get("is_featured") else 0, as_int=True)
                if "is_active" in data: _add(sets, params, "is_active", 1 if data.get("is_active", True) else 0, as_int=True)
                _add(sets, params, "location_link", data.get("location_link"))
                _add(sets, params, "directions", data.get("directions"))
                _add(sets, params, "length", data.get("length"), as_float=True)
                _add(sets, params, "breadth", data.get("breadth"), as_float=True)
                _add(sets, params, "builder", data.get("builder"))
                _add(sets, params, "configuration", data.get("configuration"))
                _add(sets, params, "total_flats", data.get("total_flats"), as_int=True)
                _add(sets, params, "total_floors", data.get("total_floors"), as_int=True)
                _add(sets, params, "total_acres", data.get("total_acres"), as_float=True)
            else:
                _add(sets, params, "city", data.get("city"))
                _add(sets, params, "locality", data.get("locality"))
                _add(sets, params, "project_name", data.get("project_name") or data.get("property_name"))
                _add(sets, params, "plot_area", data.get("plot_area"), as_float=True)
                _add(sets, params, "plot_length", data.get("plot_length"), as_float=True)
                _add(sets, params, "plot_breadth", data.get("plot_breadth"), as_float=True)
                _add(sets, params, "price", data.get("price"), as_float=True)
                _add(sets, params, "price_text", data.get("price_text"))
                if "price_negotiable" in data: _add(sets, params, "price_negotiable", 1 if data.get("price_negotiable") else 0, as_int=True)
                if "price_includes_registration" in data: _add(sets, params, "price_includes_registration", 1 if data.get("price_includes_registration") else 0, as_int=True)
                _add(sets, params, "status", _status)
                if _status in ("sale", "rent"): _set_null(sets, params, "property_status")
                else: _add(sets, params, "property_status", _pstat)
                _add(sets, params, "description", data.get("description"))
                if "is_featured" in data: _add(sets, params, "is_featured", 1 if data.get("is_featured") else 0, as_int=True)
                if "is_active" in data: _add(sets, params, "is_active", 1 if data.get("is_active", True) else 0, as_int=True)
                _add(sets, params, "location_link", data.get("location_link"))
                _add(sets, params, "directions", data.get("directions"))
                _add(sets, params, "builder", data.get("builder"))
                _add(sets, params, "total_acres", data.get("total_acres"), as_float=True)
            
            if sets:
                params.append(property_id)
                execute_update(f"UPDATE {table} SET {', '.join(sets)} WHERE id = %s", tuple(params))
            
            # Images: replace all images - handle both image_gallery (with categories) and flat images array
            image_gallery = data.get("image_gallery") or []
            images = data.get("images") or []
            
            try:
                execute_update(f"DELETE FROM {img_table} WHERE property_id = %s", (property_id,))
            except Exception as img_del_err:
                print(f"Warning: could not delete images for property {property_id}: {img_del_err}")
            
            # Process gallery images if available (preferred format with categories)
            if image_gallery:
                try:
                    for idx, gallery_item in enumerate(image_gallery):
                        image_url = gallery_item.get("image_url")
                        if image_url:
                            # Process and normalize image URL
                            processed_urls = process_image_urls([image_url], None)
                            if processed_urls:
                                image_category = gallery_item.get("category", "project")
                                # Map frontend categories to DB categories
                                category_map = {
                                    "project": "project",
                                    "floorplan": "floorplan",
                                    "masterplan": "masterplan"
                                }
                                db_category = category_map.get(image_category, "project")
                                
                                # Insert into property images table
                                execute_update(
                                    f"INSERT INTO {img_table} (property_id, image_url, image_category, image_order) VALUES (%s, %s, %s, %s)",
                                    (property_id, processed_urls[0], db_category, idx)
                                )
                except Exception as img_err:
                    print(f"Warning: could not update gallery images for property {property_id}: {img_err}")
            
            # Fallback to flat images list if gallery is empty
            if not image_gallery and images:
                try:
                    processed = process_image_urls(images, None)
                    for idx, url in enumerate(processed):
                        if url:
                            # Insert into property images table
                            execute_update(
                                f"INSERT INTO {img_table} (property_id, image_url, image_category, image_order) VALUES (%s, %s, %s, %s)",
                                (property_id, url, 'project', idx)
                            )
                except Exception as img_err:
                    print(f"Warning: could not update images for property {property_id}: {img_err}")
            
            # Features: replace
            features = data.get("features") or data.get("amenities") or []
            try:
                execute_update(
                    f"DELETE FROM {feature_table} WHERE property_category = %s AND property_id = %s",
                    (feature_category, property_id)
                )
                for name in features:
                    if name:
                        execute_update(
                            f"INSERT IGNORE INTO {feature_table} (property_category, property_id, feature_name) VALUES (%s, %s, %s)",
                            (feature_category, property_id, name)
                        )
            except Exception as fe:
                print(f"Warning: could not update features for property {property_id}: {fe}")
            
            return jsonify({"message": "Property updated successfully", "id": property_id})
        except ValueError as e:
            error_msg = f"Invalid data type: {str(e)}"
            print(f"Error updating property: {error_msg}")
            print(f"Received data: {request.get_json()}")
            traceback.print_exc()
            return error_response(error_msg, 400)
        except Exception as e:
            error_msg = f"Error updating property: {str(e)}"
            print(error_msg)
            print(f"Received data: {request.get_json()}")
            traceback.print_exc()
            return error_response(error_msg, 500)
    
    @app.route("/api/properties/<int:property_id>", methods=["DELETE"])
    @require_admin_auth
    def delete_property(property_id: int):
        """Delete a property (residential or plot) - Production-safe implementation"""
        try:
            current_app.logger.info(f"Attempting to delete property {property_id}")
            
            # Determine property category first
            property_category = None
            residential_check = execute_query("SELECT id FROM residential_properties WHERE id = %s", (property_id,))
            if residential_check:
                property_category = 'residential'
                current_app.logger.info(f"Property {property_id} found in residential_properties")
            else:
                plot_check = execute_query("SELECT id FROM plot_properties WHERE id = %s", (property_id,))
                if plot_check:
                    property_category = 'plot'
                    current_app.logger.info(f"Property {property_id} found in plot_properties")
                else:
                    current_app.logger.warning(f"Delete failed: Property {property_id} not found in any table")
                    return error_response("Property not found", 404)
            
            # Delete related data first (property_features has no CASCADE, so must delete manually)
            # Images will be deleted automatically via CASCADE foreign key
            try:
                deleted_features = execute_update(
                    "DELETE FROM property_features WHERE property_category = %s AND property_id = %s",
                    (property_category, property_id)
                )
                current_app.logger.info(f"Deleted {deleted_features} property_features for property {property_id}")
            except Exception as fe:
                current_app.logger.warning(f"Warning: Could not delete property_features for property {property_id}: {str(fe)}")
                # Continue with property deletion even if features deletion fails
            
            # Delete the property itself
            if property_category == 'residential':
                result = execute_update("DELETE FROM residential_properties WHERE id = %s", (property_id,))
                current_app.logger.info(f"DELETE query executed, affected rows: {result}")
                if result == 0:
                    current_app.logger.warning(f"Delete failed: Property {property_id} not found in residential_properties")
                    return error_response("Property not found", 404)
                current_app.logger.info(f"Property {property_id} deleted successfully from residential_properties")
            else:  # plot
                result = execute_update("DELETE FROM plot_properties WHERE id = %s", (property_id,))
                current_app.logger.info(f"DELETE query executed, affected rows: {result}")
                if result == 0:
                    current_app.logger.warning(f"Delete failed: Property {property_id} not found in plot_properties")
                    return error_response("Property not found", 404)
                current_app.logger.info(f"Property {property_id} deleted successfully from plot_properties")
            
            # Verify deletion
            verify_residential = execute_query("SELECT id FROM residential_properties WHERE id = %s", (property_id,))
            verify_plot = execute_query("SELECT id FROM plot_properties WHERE id = %s", (property_id,))
            if verify_residential or verify_plot:
                current_app.logger.error(f"Property {property_id} still exists after deletion attempt!")
                return error_response("Property deletion failed - property still exists", 500)
            
            # Success - return 200 with success message
            current_app.logger.info(f"Property {property_id} deletion verified successfully")
            return success_response("Property deleted successfully")
        except Exception as e:
            error_msg = f"Error deleting property {property_id}: {str(e)}"
            current_app.logger.error(error_msg, exc_info=True)
            print(error_msg)
            traceback.print_exc()
            return error_response(f"Failed to delete property: {str(e)}", 500)
    
    @app.route("/api/residential-properties", methods=["POST"])
    @require_admin_auth
    def create_residential_property():
        """Create property functionality has been removed"""
        return error_response("Property creation functionality has been disabled", 403)
    
    @app.route("/api/plot-properties", methods=["POST"])
    @require_admin_auth
    def create_plot_property():
        """Create property functionality has been removed"""
        return error_response("Property creation functionality has been disabled", 403)
    
    
    @app.route("/api/upload-image", methods=["POST"])
    @require_admin_auth
    def upload_image():
        """Upload an image from base64 data, save to filesystem, and optionally store in property images table if property_id is provided"""
        try:
            data = request.get_json()
            if not data or 'image' not in data:
                return error_response("Image data is required", 400)
            
            base64_string = data['image']
            if not base64_string or not isinstance(base64_string, str):
                return error_response("Invalid image data", 400)
            
            # Get property category and image category from request
            property_category = data.get('property_category', 'residential')  # Default to residential
            image_category = data.get('image_category', 'project')  # Default to project
            property_id = data.get('property_id')  # Optional, for linking to existing property
            
            # Use the helper function to save the image to filesystem
            from utils.helpers import save_base64_image
            image_url = save_base64_image(base64_string, IMAGES_DIR)
            
            # If save_base64_image returns None or the original base64 string, it means saving failed
            if not image_url or image_url == base64_string or not image_url.startswith('/images/'):
                return error_response("Failed to save image. The image may be corrupted or in an unsupported format. Please check server logs.", 500)
            
            # If property_id is provided, store image in the appropriate property images table immediately
            image_id = None
            if property_id:
                try:
                    # Determine which table to use based on property category
                    if property_category == 'plot' or property_category == 'plot_properties':
                        img_table = "plot_property_images"
                    else:
                        img_table = "residential_property_images"
                    
                    # Map frontend image categories to DB categories
                    category_map = {
                        "project": "project",
                        "floorplan": "floorplan",
                        "masterplan": "masterplan"
                    }
                    db_category = category_map.get(image_category, "project")
                    
                    # Get current max order for this property to set next order
                    order_query = f"""
                        SELECT COALESCE(MAX(image_order), -1) + 1 as next_order 
                        FROM {img_table} 
                        WHERE property_id = %s
                    """
                    order_result = execute_query(order_query, (property_id,))
                    next_order = order_result[0]['next_order'] if order_result else 0
                    
                    # Insert image into property images table
                    insert_query = f"""
                        INSERT INTO {img_table} (property_id, image_url, image_category, image_order) 
                        VALUES (%s, %s, %s, %s)
                    """
                    image_id = execute_insert(insert_query, (
                        property_id,
                        image_url,
                        db_category,
                        next_order
                    ))
                except Exception as db_err:
                    # If database insert fails, log but still return image URL
                    print(f"Warning: Could not store image in database: {str(db_err)}")
                    traceback.print_exc()
            
            # Return success response with image URL
            # Note: If property_id is not provided, image will be stored in database when property is created/updated
            return success_response({
                "image_url": image_url,
                "image_id": image_id,
                "property_category": property_category,
                "image_category": image_category
            }, "Image uploaded successfully" + (" and stored in database" if image_id else ""))
            
        except Exception as e:
            error_msg = f"Error uploading image: {str(e)}"
            current_app.logger.error(error_msg, exc_info=True)
            print(error_msg)
            traceback.print_exc()
            return error_response(f"Failed to upload image: {str(e)}", 500)