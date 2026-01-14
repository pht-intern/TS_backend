"""
Statistics routes
"""
from flask import jsonify
from datetime import datetime
import traceback
from database import execute_query
from models import PropertyStatus
from schemas import PropertyStatsSchema, FrontendStatsSchema


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
