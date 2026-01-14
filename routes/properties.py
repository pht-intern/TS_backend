"""
Properties routes
"""
from flask import request, jsonify
from datetime import datetime
import traceback
from database import execute_query
from models import PropertyType, PropertyStatus
from schemas import PaginatedResponse
from utils.helpers import (
    get_pagination_params, calculate_pages, normalize_image_url, abort_with_message
)


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
                                FROM (
                                    SELECT image_url, image_order, created_at
                                    FROM residential_property_project_images
                                    WHERE property_id = %s
                                    UNION ALL
                                    SELECT image_url, image_order, created_at
                                    FROM residential_property_floorplan_images
                                    WHERE property_id = %s
                                    UNION ALL
                                    SELECT image_url, image_order, created_at
                                    FROM residential_property_masterplan_images
                                    WHERE property_id = %s
                                ) AS all_images
                                ORDER BY image_order ASC, created_at ASC 
                                LIMIT 1
                            """
                        else:
                            primary_image_query = """
                                SELECT image_url 
                                FROM (
                                    SELECT image_url, image_order, created_at
                                    FROM plot_property_project_images
                                    WHERE property_id = %s
                                    UNION ALL
                                    SELECT image_url, image_order, created_at
                                    FROM plot_property_floorplan_images
                                    WHERE property_id = %s
                                    UNION ALL
                                    SELECT image_url, image_order, created_at
                                    FROM plot_property_masterplan_images
                                    WHERE property_id = %s
                                ) AS all_images
                                ORDER BY image_order ASC, created_at ASC 
                                LIMIT 1
                            """
                        
                        primary_images = execute_query(primary_image_query, (property_id, property_id, property_id))
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
