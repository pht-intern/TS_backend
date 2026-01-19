"""
Properties routes
"""
from flask import request, jsonify
from datetime import datetime
from decimal import Decimal
import traceback
from database import execute_query, execute_update, execute_insert
from models import PropertyType, PropertyStatus
from schemas import PaginatedResponse
from utils.helpers import (
    get_pagination_params, calculate_pages, normalize_image_url, abort_with_message,
    process_image_urls, require_admin_auth, safe_int, safe_float
)
from config import IMAGES_DIR


def register_properties_routes(app):
    """Register properties routes"""
    
    @app.route("/api/properties", methods=["GET"])
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
                    NULL as project_name
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
                                ORDER BY image_order ASC, created_at ASC 
                                LIMIT 1
                            """
                        else:
                            primary_image_query = """
                                SELECT image_url 
                                FROM plot_property_images
                                WHERE property_id = %s
                                ORDER BY image_order ASC, created_at ASC 
                                LIMIT 1
                            """
                        
                        primary_images = execute_query(primary_image_query, (property_id,))
                        if primary_images and primary_images[0].get('image_url'):
                            prop_dict['primary_image'] = normalize_image_url(primary_images[0]['image_url'])
                    except Exception as e:
                        # If image fetch fails, continue without images
                        print(f"Warning: Could not fetch images for property {property_id}: {str(e)}")
                
                # Normalize existing primary_image if it exists (fallback - in case property table has primary_image field)
                if 'primary_image' in prop_dict and prop_dict['primary_image']:
                    prop_dict['primary_image'] = normalize_image_url(prop_dict['primary_image'])
                
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
            return jsonify(response.dict())
        except Exception as e:
            error_msg = str(e)
            print(f"Error fetching properties: {error_msg}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching properties: {error_msg}")
    
    @app.route("/api/properties/<int:property_id>", methods=["GET"])
    def get_property(property_id: int):
        """Get a single property by ID with images and features"""
        try:
            # Check residential_properties first (minimal columns to avoid missing-column errors)
            residential_query = """
                SELECT 
                    id, city, locality, property_name as title, property_name, 
                    unit_type, bedrooms, buildup_area as area, buildup_area, carpet_area, 
                    price, price_text, price_negotiable, price_includes_registration,
                    type, status, property_status, description,
                    is_featured, is_active, created_at, updated_at,
                    'residential' as property_category,
                    NULL as plot_area, NULL as plot_length, NULL as plot_breadth,
                    NULL as project_name, 0 as bathrooms
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
                        NULL as unit_type, 0 as bedrooms, plot_area as area, NULL as buildup_area, NULL as carpet_area,
                        price, price_text, price_negotiable, price_includes_registration,
                        'plot' as type, status, property_status, description,
                        is_featured, is_active, created_at, updated_at,
                        'plot' as property_category,
                        plot_area, plot_length, plot_breadth,
                        project_name, 0 as bathrooms
                    FROM plot_properties
                    WHERE id = %s
                """
                properties = execute_query(plot_query, (property_id,))
                property_category = 'plot'
            
            if not properties:
                abort_with_message(404, "Property not found")
            
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
                    img_dict['is_primary'] = (i == 0)
                    img_dict['image_order'] = img_dict.get('image_order') if img_dict.get('image_order') is not None else i
                    normalized_images.append(img_dict)
            except Exception as img_err:
                print(f"Warning: could not load images for property {property_id}: {img_err}")
            property_data['images'] = normalized_images
            property_data['project_images'] = []
            property_data['floorplan_images'] = []
            property_data['masterplan_images'] = []
            
            # Get features (wrap in try/except – table or column may not exist)
            try:
                features = execute_query(
                    "SELECT * FROM property_features WHERE property_category = %s AND property_id = %s",
                    (property_category, property_id)
                )
                property_data['features'] = [dict(feat) for feat in features]
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
            property_data = _decimal_to_float(property_data)
            
            return jsonify(property_data)
        except Exception as e:
            print(f"Error fetching property: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching property: {str(e)}")
    
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
                    abort_with_message(404, "Property not found")
                table, cat = "plot_properties", "plot"
                feature_table = "property_features"
                feature_category = "plot"
                img_table = "plot_property_images"
            
            data = request.get_json()
            if not data:
                abort_with_message(400, "Invalid request data")
            
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
                _add(sets, params, "unit_type", data.get("unit_type"))
                _add(sets, params, "bedrooms", data.get("bedrooms"), as_int=True)
                _add(sets, params, "buildup_area", data.get("buildup_area"), as_float=True)
                _add(sets, params, "carpet_area", data.get("carpet_area"), as_float=True)
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
            else:
                _add(sets, params, "city", data.get("city"))
                _add(sets, params, "locality", data.get("locality"))
                _add(sets, params, "project_name", data.get("project_name"))
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
            
            if sets:
                params.append(property_id)
                execute_update(f"UPDATE {table} SET {', '.join(sets)} WHERE id = %s", tuple(params))
            
            # Images: replace all images (form sends flat list, we store all as 'project' category)
            images = data.get("images") or []
            try:
                execute_update(f"DELETE FROM {img_table} WHERE property_id = %s", (property_id,))
            except Exception as img_del_err:
                print(f"Warning: could not delete images for property {property_id}: {img_del_err}")
            if images:
                processed = process_image_urls(images, None)
                for idx, url in enumerate(processed):
                    if url:
                        execute_update(
                            f"INSERT INTO {img_table} (property_id, image_url, image_category, image_order) VALUES (%s, %s, %s, %s)",
                            (property_id, url, 'project', idx)
                        )
            
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
            abort_with_message(400, error_msg)
        except Exception as e:
            error_msg = f"Error updating property: {str(e)}"
            print(error_msg)
            print(f"Received data: {request.get_json()}")
            traceback.print_exc()
            abort_with_message(500, error_msg)
    
    @app.route("/api/properties/<int:property_id>", methods=["DELETE"])
    @require_admin_auth
    def delete_property(property_id: int):
        """Delete a property (residential or plot)."""
        try:
            residential_check = execute_query("SELECT id FROM residential_properties WHERE id = %s", (property_id,))
            if residential_check:
                result = execute_update("DELETE FROM residential_properties WHERE id = %s", (property_id,))
            else:
                plot_check = execute_query("SELECT id FROM plot_properties WHERE id = %s", (property_id,))
                if not plot_check:
                    abort_with_message(404, "Property not found")
                result = execute_update("DELETE FROM plot_properties WHERE id = %s", (property_id,))
            if result == 0:
                abort_with_message(404, "Property not found")
            return jsonify({"message": "Property deleted successfully"})
        except Exception as e:
            print(f"Error deleting property: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error deleting property: {str(e)}")
    
    @app.route("/api/residential-properties", methods=["POST"])
    @require_admin_auth
    def create_residential_property():
        """Create a new residential property"""
        try:
            data = request.get_json()
            print(f"[DEBUG] Received data for residential property: {data}")
            if not data:
                abort_with_message(400, "Invalid request data: No JSON data received")
            
            # Validate and extract required fields with safe type conversion
            city = data.get('city')
            locality = data.get('locality')
            property_name = data.get('property_name')
            
            # Validate required fields first
            if not city or not isinstance(city, str) or not city.strip():
                abort_with_message(400, "Invalid or missing 'city' field")
            if not locality or not isinstance(locality, str) or not locality.strip():
                abort_with_message(400, "Invalid or missing 'locality' field")
            if not property_name or not isinstance(property_name, str) or not property_name.strip():
                abort_with_message(400, "Invalid or missing 'property_name' field")
            
            # Clean string fields
            city = city.strip()
            locality = locality.strip()
            property_name = property_name.strip()
            
            unit_type = data.get('unit_type', 'bhk')
            bedrooms = safe_int(data.get('bedrooms'), 1)
            bathrooms = safe_float(data.get('bathrooms'), 0.0)
            buildup_area = safe_float(data.get('buildup_area'), 0.0)
            carpet_area = safe_float(data.get('carpet_area'), 0.0)
            super_built_up_area = safe_float(data.get('super_built_up_area'), None) if data.get('super_built_up_area') is not None else None
            
            # Price validation - ensure it's a valid number
            price_raw = data.get('price')
            price = safe_float(price_raw, 0.0)
            if price <= 0:
                print(f"[WARNING] Price is {price} (from raw value: {price_raw}). Using default 1.0")
                price = 1.0  # Database requires NOT NULL and > 0
            price_text = data.get('price_text')
            price_negotiable = 1 if data.get('price_negotiable') else 0
            price_includes_registration = 1 if data.get('price_includes_registration') else 0
            property_type = data.get('type', 'apartment')
            status = data.get('status', 'sale')
            # Validate status matches database CHECK constraint: ('sale', 'rent', 'resale', 'new')
            if status not in ['sale', 'rent', 'resale', 'new']:
                abort_with_message(400, f"Invalid status value: {status}. Must be one of: sale, rent, resale, new")
            # When status is 'sale' or 'rent', property_status must be NULL (residential_properties_chk_2)
            property_status = None if status in ('sale', 'rent') else data.get('property_status')
            description = data.get('description')
            location_link = data.get('location_link')
            directions = data.get('directions') or data.get('direction')  # Handle both singular and plural
            length = safe_float(data.get('length'), None) if data.get('length') is not None else None
            breadth = safe_float(data.get('breadth'), None) if data.get('breadth') is not None else None
            builder = data.get('builder')
            configuration = data.get('configuration')
            total_flats = safe_int(data.get('total_flats'), None) if data.get('total_flats') is not None else None
            total_floors = safe_int(data.get('total_floors'), None) if data.get('total_floors') is not None else None
            total_acres = safe_float(data.get('total_acres'), None) if data.get('total_acres') is not None else None
            is_featured = 1 if data.get('is_featured') else 0
            is_active = 1 if data.get('is_active', True) else 0
            images = data.get('images', [])
            features = data.get('features', []) or data.get('amenities', [])
            
            # Log the values being inserted for debugging
            print(f"[DEBUG] Residential property values: city={city}, locality={locality}, property_name={property_name}")
            print(f"[DEBUG] Dimensions: buildup_area={buildup_area}, carpet_area={carpet_area}, length={length}, breadth={breadth}")
            print(f"[DEBUG] Price: {price} (type: {type(price)}, raw: {price_raw})")
            print(f"[DEBUG] Status: {status}, property_status: {property_status}")
            print(f"[DEBUG] Bedrooms: {bedrooms}, Bathrooms: {bathrooms}")
            
            insert_query = """
                INSERT INTO residential_properties (
                    city, locality, property_name, unit_type,
                    bedrooms, bathrooms,
                    buildup_area, carpet_area, super_built_up_area,
                    price, price_text, price_negotiable, price_includes_registration,
                    type, status, property_status, description,
                    location_link, directions, length, breadth,
                    builder, configuration, total_flats, total_floors, total_acres,
                    is_featured, is_active
                ) VALUES (
                    %s, %s, %s, %s,
                    %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s
                )
            """
            
            insert_params = (
                city, locality, property_name, unit_type,
                bedrooms, bathrooms,
                buildup_area, carpet_area, super_built_up_area,
                price, price_text, price_negotiable, price_includes_registration,
                property_type, status, property_status, description,
                location_link, directions, length, breadth,
                builder, configuration, total_flats, total_floors, total_acres,
                is_featured, is_active
            )
            
            # Validate placeholder count matches params count
            placeholder_count = insert_query.count('%s')
            params_count = len(insert_params)
            if placeholder_count != params_count:
                error_msg = f"SQL placeholder count ({placeholder_count}) does not match params count ({params_count})"
                print(f"[ERROR] {error_msg}")
                print(f"[ERROR] Query: {insert_query}")
                print(f"[ERROR] Params: {insert_params}")
                abort_with_message(500, f"Database query error: {error_msg}")
            
            print(f"[DEBUG] Insert params ({params_count} values): {insert_params}")
            
            property_id = execute_insert(insert_query, insert_params)
            
            # Insert images into unified residential_property_images table
            if images:
                processed_images = process_image_urls(images, IMAGES_DIR)
                for idx, image_url in enumerate(processed_images):
                    image_query = "INSERT INTO residential_property_images (property_id, image_url, image_category, image_order) VALUES (%s, %s, %s, %s)"
                    execute_insert(image_query, (property_id, image_url, 'project', idx))
            
            # Insert features into unified property_features table
            if features:
                for feature_name in features:
                    feature_query = "INSERT IGNORE INTO property_features (property_category, property_id, feature_name) VALUES (%s, %s, %s)"
                    execute_update(feature_query, ('residential', property_id, feature_name))
            
            return jsonify({"message": "Residential property created successfully", "id": property_id}), 201
        except ValueError as e:
            error_msg = f"Invalid data type: {str(e)}"
            print(f"[ERROR] ValueError creating residential property: {error_msg}")
            print(f"[ERROR] Received data: {request.get_json()}")
            traceback.print_exc()
            abort_with_message(400, f"Invalid data format: {str(e)}")
        except KeyError as e:
            error_msg = f"Missing required field: {str(e)}"
            print(f"[ERROR] KeyError creating residential property: {error_msg}")
            print(f"[ERROR] Received data: {request.get_json()}")
            traceback.print_exc()
            abort_with_message(400, error_msg)
        except Exception as e:
            error_msg = f"Error creating residential property: {str(e)}"
            error_type = type(e).__name__
            print(f"[ERROR] {error_type} creating residential property: {error_msg}")
            print(f"[ERROR] Received data: {request.get_json()}")
            print(f"[ERROR] Exception details:")
            traceback.print_exc()
            # Return more detailed error message for debugging
            abort_with_message(500, f"Server error ({error_type}): {str(e)}")
    
    @app.route("/api/plot-properties", methods=["POST"])
    @require_admin_auth
    def create_plot_property():
        """Create a new plot property"""
        try:
            data = request.get_json()
            print(f"[DEBUG] Received data for plot property: {data}")
            if not data:
                abort_with_message(400, "Invalid request data")
            
            # Validate and extract required fields with safe type conversion
            city = data.get('city')
            locality = data.get('locality')
            project_name = data.get('project_name')
            
            # Validate required fields first
            if not city or not isinstance(city, str) or not city.strip():
                abort_with_message(400, "Invalid or missing 'city' field")
            if not locality or not isinstance(locality, str) or not locality.strip():
                abort_with_message(400, "Invalid or missing 'locality' field")
            if not project_name or not isinstance(project_name, str) or not project_name.strip():
                abort_with_message(400, "Invalid or missing 'project_name' field")
            
            # Clean string fields
            city = city.strip()
            locality = locality.strip()
            project_name = project_name.strip()
            
            # Ensure plot dimensions are never None (database requires NOT NULL)
            plot_area = safe_float(data.get('plot_area'), 0.0)
            plot_length = safe_float(data.get('plot_length'), 0.0)
            plot_breadth = safe_float(data.get('plot_breadth'), 0.0)
            
            # Price validation - ensure it's a valid number
            price_raw = data.get('price')
            price = safe_float(price_raw, 0.0)
            if price <= 0:
                print(f"[WARNING] Price is {price} (from raw value: {price_raw}). Using default 1.0")
                price = 1.0  # Database requires NOT NULL and > 0
            price_text = data.get('price_text')
            price_negotiable = 1 if data.get('price_negotiable') else 0
            price_includes_registration = 1 if data.get('price_includes_registration') else 0
            status = data.get('status', 'sale')
            # Validate status matches database CHECK constraint: ('sale', 'rent', 'resale', 'new')
            if status not in ['sale', 'rent', 'resale', 'new']:
                abort_with_message(400, f"Invalid status value: {status}. Must be one of: sale, rent, resale, new")
            # When status is 'sale' or 'rent', property_status must be NULL (plot_properties_chk_2)
            property_status = None if status in ('sale', 'rent') else data.get('property_status')
            description = data.get('description')
            location_link = data.get('location_link')
            directions = data.get('directions') or data.get('direction')  # Handle both singular and plural
            builder = data.get('builder')
            total_acres = safe_float(data.get('total_acres'), None) if data.get('total_acres') is not None else None
            is_featured = 1 if data.get('is_featured') else 0
            is_active = 1 if data.get('is_active', True) else 0
            images = data.get('images', [])
            features = data.get('features', []) or data.get('amenities', [])
            
            # Log the values being inserted for debugging
            print(f"[DEBUG] Plot property values: city={city}, locality={locality}, project_name={project_name}")
            print(f"[DEBUG] Plot dimensions: plot_area={plot_area} (type: {type(plot_area)}), plot_length={plot_length}, plot_breadth={plot_breadth}")
            print(f"[DEBUG] Price: {price} (type: {type(price)}, raw: {price_raw})")
            print(f"[DEBUG] Status: {status}, property_status: {property_status}")
            
            insert_query = """
                INSERT INTO plot_properties (
                    city, locality, project_name, plot_area, plot_length, plot_breadth,
                    price, price_text, price_negotiable, price_includes_registration,
                    status, property_status, description,
                    location_link, directions, builder, total_acres,
                    is_featured, is_active
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            insert_params = (
                city, locality, project_name, plot_area, plot_length, plot_breadth,
                price, price_text, price_negotiable, price_includes_registration,
                status, property_status, description,
                location_link, directions, builder, total_acres,
                is_featured, is_active
            )
            
            # Validate placeholder count matches params count
            placeholder_count = insert_query.count('%s')
            params_count = len(insert_params)
            if placeholder_count != params_count:
                error_msg = f"SQL placeholder count ({placeholder_count}) does not match params count ({params_count})"
                print(f"[ERROR] {error_msg}")
                print(f"[ERROR] Query: {insert_query}")
                print(f"[ERROR] Params: {insert_params}")
                abort_with_message(500, f"Database query error: {error_msg}")
            
            print(f"[DEBUG] Insert params ({params_count} values): {insert_params}")
            
            property_id = execute_insert(insert_query, insert_params)
            
            # Insert images into unified plot_property_images table
            if images:
                processed_images = process_image_urls(images, IMAGES_DIR)
                for idx, image_url in enumerate(processed_images):
                    image_query = "INSERT INTO plot_property_images (property_id, image_url, image_category, image_order) VALUES (%s, %s, %s, %s)"
                    execute_insert(image_query, (property_id, image_url, 'project', idx))
            
            # Insert features into unified property_features table
            if features:
                for feature_name in features:
                    feature_query = "INSERT IGNORE INTO property_features (property_category, property_id, feature_name) VALUES (%s, %s, %s)"
                    execute_update(feature_query, ('plot', property_id, feature_name))
            
            return jsonify({"message": "Plot property created successfully", "id": property_id}), 201
        except ValueError as e:
            error_msg = f"Invalid data type: {str(e)}"
            print(f"[ERROR] ValueError creating plot property: {error_msg}")
            print(f"[ERROR] Received data: {request.get_json()}")
            traceback.print_exc()
            abort_with_message(400, f"Invalid data format: {str(e)}")
        except KeyError as e:
            error_msg = f"Missing required field: {str(e)}"
            print(f"[ERROR] KeyError creating plot property: {error_msg}")
            print(f"[ERROR] Received data: {request.get_json()}")
            traceback.print_exc()
            abort_with_message(400, error_msg)
        except Exception as e:
            error_msg = f"Error creating plot property: {str(e)}"
            error_type = type(e).__name__
            print(f"[ERROR] {error_type} creating plot property: {error_msg}")
            print(f"[ERROR] Received data: {request.get_json()}")
            print(f"[ERROR] Exception details:")
            traceback.print_exc()
            # Return more detailed error message for debugging
            abort_with_message(500, f"Server error ({error_type}): {str(e)}")
