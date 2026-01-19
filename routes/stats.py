"""
Statistics routes
"""
from flask import jsonify
from datetime import datetime
import traceback
import json
from database import execute_query
from models import PropertyStatus
from schemas import PropertyStatsSchema, FrontendStatsSchema, DashboardStatsSchema
from utils.helpers import abort_with_message, require_admin_auth


def register_stats_routes(app):
    """Register statistics routes"""
    
    @app.route("/api/stats/properties", methods=["GET"])
    def get_property_stats():
        """Get property statistics (optimized with single query)"""
        try:
            # Query both residential_properties and plot_properties
            query = f"""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = '{PropertyStatus.SALE.value}' THEN 1 ELSE 0 END) as for_sale,
                    SUM(CASE WHEN status = '{PropertyStatus.RENT.value}' THEN 1 ELSE 0 END) as for_rent,
                    SUM(CASE WHEN is_featured = 1 THEN 1 ELSE 0 END) as featured
                FROM (
                    SELECT status, is_featured FROM residential_properties WHERE is_active = 1
                    UNION ALL
                    SELECT status, is_featured FROM plot_properties WHERE is_active = 1
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
            
            # Get type breakdown from both tables
            by_type = {}
            try:
                type_stats_res = execute_query("SELECT type, COUNT(*) as count FROM residential_properties WHERE is_active = 1 GROUP BY type")
                type_stats_plot = execute_query("SELECT 'plot' as type, COUNT(*) as count FROM plot_properties WHERE is_active = 1")
                
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
            
            return jsonify(result_dict)
        except Exception as e:
            print(f"Error fetching property stats: {str(e)}")
            traceback.print_exc()
            result = PropertyStatsSchema(total=0, for_sale=0, for_rent=0, by_type={}, featured=0)
            return jsonify(result.dict())
    
    @app.route("/api/stats/frontend", methods=["GET"])
    def get_frontend_stats():
        """Get frontend statistics for homepage"""
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
            
            return jsonify(result_dict)
        except Exception as e:
            print(f"Error in get_frontend_stats: {str(e)}")
            # Calculate years of experience dynamically even in error case
            current_year = datetime.now().year
            base_year = 2010
            years_experience = current_year - base_year
            result = FrontendStatsSchema(properties_listed=0, happy_clients=45, years_experience=years_experience, deals_closed=20)
            return jsonify(result.dict())
    
    @app.route("/api/admin/stats/dashboard", methods=["GET"])
    @require_admin_auth
    def get_dashboard_stats():
        """Get dashboard statistics (admin endpoint)"""
        try:
            def get_count(query):
                result = execute_query(query)
                return result[0]['count'] if result else 0
            
            # Count properties from both tables
            total_properties = get_count("SELECT COUNT(*) as count FROM (SELECT id FROM residential_properties UNION ALL SELECT id FROM plot_properties) as combined")
            active_properties = get_count("SELECT COUNT(*) as count FROM (SELECT id FROM residential_properties WHERE is_active = 1 UNION ALL SELECT id FROM plot_properties WHERE is_active = 1) as combined")
            featured_properties = get_count("SELECT COUNT(*) as count FROM (SELECT id FROM residential_properties WHERE is_featured = 1 UNION ALL SELECT id FROM plot_properties WHERE is_featured = 1) as combined")
            total_partners = get_count("SELECT COUNT(*) as count FROM partners")
            active_partners = get_count("SELECT COUNT(*) as count FROM partners WHERE is_active = 1")
            total_testimonials = get_count("SELECT COUNT(*) as count FROM testimonials")
            approved_testimonials = get_count("SELECT COUNT(*) as count FROM testimonials WHERE is_approved = 1")
            new_inquiries = get_count("SELECT COUNT(*) as count FROM contact_inquiries WHERE status = 'new'")
            total_inquiries = get_count("SELECT COUNT(*) as count FROM contact_inquiries")
            total_logs = get_count("SELECT COUNT(*) as count FROM logs")
            
            # Get type stats from both tables
            type_stats_res = execute_query("SELECT type, COUNT(*) as count FROM residential_properties GROUP BY type")
            type_stats_plot = execute_query("SELECT 'plot' as type, COUNT(*) as count FROM plot_properties")
            properties_by_type = {}
            if type_stats_res:
                for row in type_stats_res:
                    properties_by_type[row['type']] = row['count']
            if type_stats_plot and type_stats_plot[0]['count'] > 0:
                properties_by_type['plot'] = properties_by_type.get('plot', 0) + type_stats_plot[0]['count']
            
            # Get status stats from both tables
            status_stats = execute_query("SELECT status, COUNT(*) as count FROM (SELECT status FROM residential_properties UNION ALL SELECT status FROM plot_properties) as combined GROUP BY status")
            properties_by_status = {row['status']: row['count'] for row in status_stats} if status_stats else {}
            
            result = DashboardStatsSchema(
                total_properties=total_properties,
                active_properties=active_properties,
                featured_properties=featured_properties,
                total_partners=total_partners,
                active_partners=active_partners,
                total_testimonials=total_testimonials,
                approved_testimonials=approved_testimonials,
                new_inquiries=new_inquiries,
                total_inquiries=total_inquiries,
                total_logs=total_logs,
                properties_by_type=properties_by_type,
                properties_by_status=properties_by_status
            )
            return jsonify(result.dict())
        except Exception as e:
            print(f"Error fetching dashboard stats: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching dashboard stats: {str(e)}")
    
    @app.route("/api/admin/stats/page-visits", methods=["GET"])
    @require_admin_auth
    def get_page_visit_stats():
        """Get page visit statistics (admin endpoint)"""
        try:
            import json
            import re
            
            # Get all page_view logs with metadata and description
            all_logs = execute_query("""
                SELECT metadata, description 
                FROM logs 
                WHERE action = 'page_view'
            """)
            
            page_counts = {}
            for log in all_logs:
                page = None
                
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
                page_counts[page] = page_counts.get(page, 0) + 1
            
            # Convert to list and sort by visits
            page_visits = [{'page': page, 'visits': count} for page, count in sorted(page_counts.items(), key=lambda x: x[1], reverse=True)[:50]]
            
            return jsonify({
                'page_visits': page_visits or []
            })
        except Exception as e:
            print(f"Error fetching page visit stats: {str(e)}")
            traceback.print_exc()
            return jsonify({'page_visits': []})
