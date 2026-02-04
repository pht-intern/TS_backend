"""
Statistics routes
"""
from flask import jsonify, request, make_response
from datetime import datetime, date
from decimal import Decimal
import traceback
import json
import re
from database import execute_query
from models import PropertyStatus
from schemas import PropertyStatsSchema, FrontendStatsSchema, DashboardStatsSchema
from utils.helpers import abort_with_message, require_admin_auth


def register_stats_routes(app):
    """Register statistics routes"""
    
    @app.route("/api/stats/properties", methods=["GET", "OPTIONS"])
    def get_property_stats():
        """Get property statistics (optimized with single query)"""
        # Handle OPTIONS request for CORS preflight
        if request.method == "OPTIONS":
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        
        try:
            # Query residential_properties, plot_properties, and commercial_properties.
            # Normalize status: residential uses 'sell'/'new', plot/commercial use 'sale'/'rent'
            query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status IN ('sell', 'sale') THEN 1 ELSE 0 END) as for_sale,
                    SUM(CASE WHEN status IN ('new', 'rent') THEN 1 ELSE 0 END) as for_rent,
                    SUM(CASE WHEN is_featured = 1 THEN 1 ELSE 0 END) as featured
                FROM (
                    SELECT status, is_featured FROM residential_properties WHERE is_active = 1
                    UNION ALL
                    SELECT status, is_featured FROM plot_properties WHERE is_active = 1
                    UNION ALL
                    SELECT status, is_featured FROM commercial_properties WHERE is_active = 1
                ) as combined
            """
            
            stats_result = execute_query(query)
            total = 0
            for_sale = 0
            for_rent = 0
            featured = 0
            
            if stats_result and len(stats_result) > 0 and stats_result[0]:
                total = int(stats_result[0].get('total', 0) or 0)
                for_sale = int(stats_result[0].get('for_sale', 0) or 0)
                for_rent = int(stats_result[0].get('for_rent', 0) or 0)
                featured = int(stats_result[0].get('featured', 0) or 0)
            
            # Get type breakdown from residential, plot, and commercial tables
            by_type = {}
            try:
                type_stats_res = execute_query("SELECT type, COUNT(*) as count FROM residential_properties WHERE is_active = 1 GROUP BY type")
                type_stats_plot = execute_query("SELECT 'plot' as type, COUNT(*) as count FROM plot_properties WHERE is_active = 1")
                type_stats_com = execute_query("SELECT property_type as type, COUNT(*) as count FROM commercial_properties WHERE is_active = 1 GROUP BY property_type")
                
                if type_stats_res:
                    for row in type_stats_res:
                        if row and row.get('type') is not None:
                            type_name = str(row.get('type', ''))
                            count_val = row.get('count', 0)
                            by_type[type_name] = int(count_val or 0)
                
                if type_stats_plot:
                    for row in type_stats_plot:
                        if row and row.get('count', 0) > 0:
                            by_type['plot'] = by_type.get('plot', 0) + int(row.get('count', 0))
                
                if type_stats_com:
                    for row in type_stats_com:
                        if row and row.get('type') is not None:
                            type_name = str(row.get('type', ''))
                            count_val = row.get('count', 0)
                            by_type[type_name] = by_type.get(type_name, 0) + int(count_val or 0)
            except Exception as e:
                print(f"Error fetching property types: {str(e)}")
            
            result = PropertyStatsSchema(
                total=int(total or 0),
                for_sale=int(for_sale or 0),
                for_rent=int(for_rent or 0),
                by_type=by_type if by_type else {},
                featured=int(featured or 0)
            )
            
            result_dict = result.dict()
            
            # Support JSONP if callback parameter is provided
            callback = request.args.get('callback')
            if callback:
                # Validate callback name to prevent XSS
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                    response = make_response(f"{callback}({json.dumps(result_dict)});")
                    response.headers['Content-Type'] = 'application/javascript'
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response
                else:
                    # Invalid callback name, return regular JSON
                    response = jsonify({'error': 'Invalid callback parameter'})
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response, 400
            
            response = jsonify(result_dict)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Exception as e:
            print(f"Error fetching property stats: {str(e)}")
            traceback.print_exc()
            result = PropertyStatsSchema(total=0, for_sale=0, for_rent=0, by_type={}, featured=0)
            result_dict = result.dict()
            
            # Support JSONP in error case too
            callback = request.args.get('callback')
            if callback and re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                response = make_response(f"{callback}({json.dumps(result_dict)});")
                response.headers['Content-Type'] = 'application/javascript'
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            
            response = jsonify(result_dict)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
    
    @app.route("/api/stats/frontend", methods=["GET", "OPTIONS"])
    def get_frontend_stats():
        """Get frontend statistics for homepage"""
        # Handle OPTIONS request for CORS preflight
        if request.method == "OPTIONS":
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        
        try:
            # Optimized: Use single query with conditional aggregation where possible
            def get_count(query):
                try:
                    result = execute_query(query)
                    return result[0]['count'] if result and len(result) > 0 else 0
                except Exception as e:
                    print(f"Error executing query: {query}, Error: {str(e)}")
                    return 0
            
            properties_listed = get_count("SELECT COUNT(*) as count FROM (SELECT id FROM residential_properties WHERE is_active = 1 UNION ALL SELECT id FROM plot_properties WHERE is_active = 1) as combined")
            
            # Fixed values as requested
            happy_clients = 45
            deals_closed = 20
            
            # Calculate years of experience dynamically (auto-increase each year)
            # Base year: 2010 (2026 - 2010 = 16 years)
            current_year = datetime.now().year
            base_year = 2010
            years_experience = current_year - base_year
            
            result = FrontendStatsSchema(
                properties_listed=properties_listed,
                happy_clients=happy_clients,
                years_experience=years_experience,
                deals_closed=deals_closed
            )
            
            result_dict = result.dict()
            
            # Support JSONP if callback parameter is provided
            callback = request.args.get('callback')
            if callback:
                # Validate callback name to prevent XSS
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                    response = make_response(f"{callback}({json.dumps(result_dict)});")
                    response.headers['Content-Type'] = 'application/javascript'
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response
                else:
                    # Invalid callback name, return regular JSON
                    return jsonify({'error': 'Invalid callback parameter'}), 400
            
            response = jsonify(result_dict)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Exception as e:
            print(f"Error in get_frontend_stats: {str(e)}")
            traceback.print_exc()
            # Calculate years of experience dynamically even in error case
            current_year = datetime.now().year
            base_year = 2010
            years_experience = current_year - base_year
            result = FrontendStatsSchema(properties_listed=0, happy_clients=45, years_experience=years_experience, deals_closed=20)
            result_dict = result.dict()
            
            # Support JSONP in error case too
            callback = request.args.get('callback')
            if callback and re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                response = make_response(f"{callback}({json.dumps(result_dict)});")
                response.headers['Content-Type'] = 'application/javascript'
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            
            response = jsonify(result_dict)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
    
    @app.route("/api/admin/stats/dashboard", methods=["GET"])
    @require_admin_auth
    def get_dashboard_stats():
        """Get dashboard statistics (admin endpoint)"""
        try:
            def get_count(query):
                """Safely get count from query result"""
                try:
                    result = execute_query(query)
                    if result and len(result) > 0 and result[0]:
                        count = result[0].get('count', 0)
                        # Handle int, string, Decimal, and None counts
                        if count is None:
                            return 0
                        # Convert Decimal to int if needed
                        if isinstance(count, Decimal):
                            return int(count)
                        return int(count) if count is not None else 0
                    return 0
                except Exception as e:
                    print(f"Warning: Error executing count query: {query[:100]}... Error: {str(e)}")
                    return 0
            
            # Count properties from residential, plot, and commercial tables - Guard: Handle missing tables gracefully
            total_properties = get_count("SELECT COUNT(*) as count FROM (SELECT id FROM residential_properties UNION ALL SELECT id FROM plot_properties UNION ALL SELECT id FROM commercial_properties) as combined")
            active_properties = get_count("SELECT COUNT(*) as count FROM (SELECT id FROM residential_properties WHERE is_active = 1 UNION ALL SELECT id FROM plot_properties WHERE is_active = 1 UNION ALL SELECT id FROM commercial_properties WHERE is_active = 1) as combined")
            featured_properties = get_count("SELECT COUNT(*) as count FROM (SELECT id FROM residential_properties WHERE is_featured = 1 UNION ALL SELECT id FROM plot_properties WHERE is_featured = 1 UNION ALL SELECT id FROM commercial_properties WHERE is_featured = 1) as combined")
            
            # Guard: Handle tables that might not exist
            total_partners = get_count("SELECT COUNT(*) as count FROM partners")
            active_partners = get_count("SELECT COUNT(*) as count FROM partners WHERE is_active = 1")
            total_testimonials = get_count("SELECT COUNT(*) as count FROM testimonials")
            approved_testimonials = get_count("SELECT COUNT(*) as count FROM testimonials WHERE is_approved = 1")
            new_inquiries = get_count("SELECT COUNT(*) as count FROM contact_inquiries WHERE status = 'new'")
            total_inquiries = get_count("SELECT COUNT(*) as count FROM contact_inquiries")
            total_logs = get_count("SELECT COUNT(*) as count FROM logs")
            
            # Get type stats from both tables - Guard: Handle empty results
            properties_by_type = {}
            try:
                type_stats_res = execute_query("SELECT type, COUNT(*) as count FROM residential_properties GROUP BY type")
                if type_stats_res:
                    for row in type_stats_res:
                        if row and 'type' in row and 'count' in row:
                            count_val = row['count']
                            # Convert Decimal to int if needed
                            if isinstance(count_val, Decimal):
                                count_val = int(count_val)
                            properties_by_type[row['type']] = int(count_val) if count_val is not None else 0
            except Exception as e:
                print(f"Warning: Error fetching residential property type stats: {str(e)}")
            
            try:
                type_stats_plot = execute_query("SELECT 'plot' as type, COUNT(*) as count FROM plot_properties")
                if type_stats_plot and len(type_stats_plot) > 0 and type_stats_plot[0]:
                    plot_count = type_stats_plot[0].get('count', 0)
                    # Convert Decimal to int if needed
                    if isinstance(plot_count, Decimal):
                        plot_count = int(plot_count)
                    if plot_count and int(plot_count) > 0:
                        properties_by_type['plot'] = properties_by_type.get('plot', 0) + int(plot_count)
            except Exception as e:
                print(f"Warning: Error fetching plot property type stats: {str(e)}")
            
            try:
                type_stats_com = execute_query("SELECT property_type as type, COUNT(*) as count FROM commercial_properties GROUP BY property_type")
                if type_stats_com:
                    for row in type_stats_com:
                        if row and 'type' in row and 'count' in row:
                            count_val = row['count']
                            if isinstance(count_val, Decimal):
                                count_val = int(count_val)
                            t = row['type']
                            properties_by_type[t] = properties_by_type.get(t, 0) + (int(count_val) if count_val is not None else 0)
            except Exception as e:
                print(f"Warning: Error fetching commercial property type stats: {str(e)}")
            
            # Get status stats from residential, plot, and commercial tables - Guard: Handle empty results and NULL values
            properties_by_status = {}
            try:
                # Handle NULL status values by using COALESCE
                status_stats = execute_query("""
                    SELECT 
                        COALESCE(status, 'unknown') as status, 
                        COUNT(*) as count 
                    FROM (
                        SELECT status FROM residential_properties 
                        UNION ALL 
                        SELECT status FROM plot_properties
                        UNION ALL 
                        SELECT status FROM commercial_properties
                    ) as combined 
                    GROUP BY COALESCE(status, 'unknown')
                """)
                if status_stats:
                    for row in status_stats:
                        if row and 'status' in row and 'count' in row:
                            status_key = row['status']
                            # Skip 'unknown' status if it's 0 or handle it gracefully
                            if status_key and status_key != 'unknown':
                                count_val = row['count']
                                # Convert Decimal to int if needed
                                if isinstance(count_val, Decimal):
                                    count_val = int(count_val)
                                properties_by_status[status_key] = int(count_val) if count_val is not None else 0
            except Exception as e:
                print(f"Warning: Error fetching status stats: {str(e)}")
                traceback.print_exc()
            
            # Ensure all required fields have valid values
            result = DashboardStatsSchema(
                total_properties=int(total_properties) if total_properties is not None else 0,
                active_properties=int(active_properties) if active_properties is not None else 0,
                featured_properties=int(featured_properties) if featured_properties is not None else 0,
                total_partners=int(total_partners) if total_partners is not None else 0,
                active_partners=int(active_partners) if active_partners is not None else 0,
                total_testimonials=int(total_testimonials) if total_testimonials is not None else 0,
                approved_testimonials=int(approved_testimonials) if approved_testimonials is not None else 0,
                new_inquiries=int(new_inquiries) if new_inquiries is not None else 0,
                total_inquiries=int(total_inquiries) if total_inquiries is not None else 0,
                total_logs=int(total_logs) if total_logs is not None else 0,
                properties_by_type=properties_by_type if properties_by_type else {},
                properties_by_status=properties_by_status if properties_by_status else {}
            )
            
            # Convert to dict and ensure all values are JSON serializable
            result_dict = result.dict()
            
            # Double-check all values are serializable
            def make_serializable(obj):
                if isinstance(obj, dict):
                    return {k: make_serializable(v) for k, v in obj.items()}
                elif isinstance(obj, (list, tuple)):
                    return [make_serializable(item) for item in obj]
                elif isinstance(obj, Decimal):
                    return int(obj)
                elif isinstance(obj, (datetime, date)):
                    return obj.isoformat()
                else:
                    return obj
            
            result_dict = make_serializable(result_dict)
            
            response = jsonify(result_dict)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Exception as e:
            print(f"Error fetching dashboard stats: {str(e)}")
            traceback.print_exc()
            # Return a safe error response instead of aborting
            error_response = jsonify({
                'error': f'Error fetching dashboard stats: {str(e)}',
                'success': False
            })
            error_response.headers['Access-Control-Allow-Origin'] = '*'
            return error_response, 500
    
    @app.route("/api/admin/stats/page-visits", methods=["GET"])
    @require_admin_auth
    def get_page_visit_stats():
        """Get page visit statistics with unique and authenticated visitors (admin endpoint)"""
        try:
            import json
            import re
            
            # Get all page_view logs with metadata, description, ip_address, and user_email
            all_logs = execute_query("""
                SELECT metadata, description, ip_address, user_email 
                FROM logs 
                WHERE action = 'page_view'
                ORDER BY created_at DESC
            """)
            
            # Structure: {page_name: {'visits': count, 'unique_ips': set(), 'authenticated_emails': set()}}
            page_stats = {}
            
            for log in all_logs:
                page = None
                ip_address = log.get('ip_address')
                user_email = log.get('user_email')
                is_authenticated = bool(user_email and user_email.strip())
                
                # First, try to get page from metadata
                try:
                    metadata = log.get('metadata')
                    if metadata:
                        if isinstance(metadata, str):
                            metadata = json.loads(metadata)
                        if isinstance(metadata, dict):
                            page = metadata.get('page')
                except:
                    pass
                
                # If not in metadata, try to extract from description
                if not page:
                    try:
                        description = log.get('description', '')
                        if description:
                            # Extract page name from description like "Page viewed: Homepage" or "User email viewed: Properties Page"
                            match = re.search(r'(?:viewed|viewing):\s*(.+?)(?:\s*$|,|\.)', description, re.IGNORECASE)
                            if match:
                                page = match.group(1).strip()
                            else:
                                # Fallback: try to extract from URL patterns in description
                                # Or use a default based on description content
                                if 'homepage' in description.lower() or 'index' in description.lower():
                                    page = 'Homepage'
                                elif 'properties' in description.lower():
                                    page = 'Properties Page'
                                elif 'dashboard' in description.lower():
                                    page = 'Dashboard'
                                elif 'blog' in description.lower():
                                    page = 'Blogs Page'
                                else:
                                    # Last resort: use a sanitized version of description
                                    page = description.split(':')[-1].strip() if ':' in description else 'Unknown Page'
                    except:
                        pass
                
                # Use page name or default
                page = page or 'Unknown Page'
                
                # Initialize page stats if not exists
                if page not in page_stats:
                    page_stats[page] = {
                        'visits': 0,
                        'unique_ips': set(),
                        'authenticated_emails': set()
                    }
                
                # Increment total visits
                page_stats[page]['visits'] += 1
                
                # Track unique IP addresses
                if ip_address and ip_address.strip():
                    page_stats[page]['unique_ips'].add(ip_address.strip())
                
                # Track authenticated visitors
                if is_authenticated:
                    page_stats[page]['authenticated_emails'].add(user_email.strip())
            
            # Convert to list format with all metrics
            page_visits = []
            for page, stats in sorted(page_stats.items(), key=lambda x: x[1]['visits'], reverse=True)[:50]:
                page_visits.append({
                    'page': page,
                    'visits': stats['visits'],
                    'unique_visitors': len(stats['unique_ips']),
                    'authenticated_visitors': len(stats['authenticated_emails'])
                })
            
            return jsonify({
                'page_visits': page_visits or []
            })
        except Exception as e:
            print(f"Error fetching page visit stats: {str(e)}")
            traceback.print_exc()
            return jsonify({'page_visits': []})
