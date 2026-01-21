"""
Metrics routes
"""
from flask import request, jsonify, make_response
import traceback
from datetime import datetime
from database import execute_update, execute_query
from utils.helpers import require_admin_auth, abort_with_message


def register_metrics_routes(app):
    """Register metrics routes"""
    
    @app.route("/api/admin/application-metrics", methods=["GET", "OPTIONS"])
    @require_admin_auth
    def get_application_metrics():
        """Get application metrics aggregated by time period"""
        # Handle OPTIONS request for CORS preflight
        if request.method == "OPTIONS":
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        
        try:
            hours = request.args.get('hours', default=48, type=int)
            if hours < 1:
                hours = 48
            if hours > 168:  # Max 7 days
                hours = 168
            
            # Get metrics aggregated by hour from application_metrics table
            query = """
                SELECT 
                    DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:00:00') as time_bucket,
                    COUNT(*) as request_count,
                    AVG(response_time_ms) as avg_response_time,
                    MAX(response_time_ms) as max_response_time,
                    MIN(response_time_ms) as min_response_time,
                    SUM(CASE WHEN is_error = 1 THEN 1 ELSE 0 END) as error_count,
                    SUM(CASE WHEN status_code >= 200 AND status_code < 300 THEN 1 ELSE 0 END) as success_count,
                    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) as client_error_count,
                    SUM(CASE WHEN status_code >= 500 THEN 1 ELSE 0 END) as server_error_count
                FROM application_metrics
                WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s HOUR)
                GROUP BY time_bucket
                ORDER BY time_bucket ASC
            """
            
            metrics = execute_query(query, (hours,))
            
            # Get current stats (last hour)
            current_query = """
                SELECT 
                    COUNT(*) as request_count,
                    AVG(response_time_ms) as avg_response_time,
                    SUM(CASE WHEN is_error = 1 THEN 1 ELSE 0 END) as error_count,
                    SUM(CASE WHEN status_code >= 200 AND status_code < 300 THEN 1 ELSE 0 END) as success_count
                FROM application_metrics
                WHERE created_at >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
            """
            
            current_stats = execute_query(current_query)
            current = current_stats[0] if current_stats and len(current_stats) > 0 else {}
            
            # Get top endpoints by request count
            top_endpoints_query = """
                SELECT 
                    endpoint,
                    method,
                    COUNT(*) as request_count,
                    AVG(response_time_ms) as avg_response_time,
                    SUM(CASE WHEN is_error = 1 THEN 1 ELSE 0 END) as error_count
                FROM application_metrics
                WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s HOUR)
                GROUP BY endpoint, method
                ORDER BY request_count DESC
                LIMIT 10
            """
            
            top_endpoints = execute_query(top_endpoints_query, (hours,))
            
            # Get cache statistics from cache_logs (if table exists)
            cache_stats = {
                "total_operations": 0,
                "cache_hits": 0,
                "cache_misses": 0,
                "cache_hit_rate": 0.0,
                "avg_cache_time": 0.0
            }
            
            try:
                cache_stats_query = """
                    SELECT 
                        COUNT(*) as total_cache_ops,
                        SUM(CASE WHEN operation = 'hit' THEN 1 ELSE 0 END) as cache_hits,
                        SUM(CASE WHEN operation = 'miss' THEN 1 ELSE 0 END) as cache_misses,
                        AVG(response_time_ms) as avg_cache_time
                    FROM cache_logs
                    WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s HOUR)
                """
                cache_data_result = execute_query(cache_stats_query, (hours,))
                if cache_data_result and len(cache_data_result) > 0:
                    cache_data = cache_data_result[0]
                    total_cache_ops = cache_data.get('total_cache_ops', 0) or 0
                    cache_hits = cache_data.get('cache_hits', 0) or 0
                    cache_hit_rate = (cache_hits / total_cache_ops * 100) if total_cache_ops > 0 else 0
                    cache_stats = {
                        "total_operations": int(total_cache_ops),
                        "cache_hits": int(cache_hits),
                        "cache_misses": int(cache_data.get('cache_misses', 0) or 0),
                        "cache_hit_rate": round(cache_hit_rate, 2),
                        "avg_cache_time": float(cache_data.get('avg_cache_time', 0) or 0)
                    }
            except Exception as cache_error:
                # Cache logs table doesn't exist or error - use defaults
                print(f"Note: Cache logs not available: {str(cache_error)}")
            
            # Get system metrics (CPU, RAM, Bandwidth) from system_metrics table
            system_metrics_query = """
                SELECT 
                    cpu_usage,
                    ram_usage,
                    ram_used_mb,
                    ram_total_mb,
                    bandwidth_in_mb,
                    bandwidth_out_mb,
                    bandwidth_total_mb,
                    created_at
                FROM system_metrics
                WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s HOUR)
                ORDER BY created_at ASC
            """
            
            system_metrics = execute_query(system_metrics_query, (hours,))
            
            # Get current system metrics (most recent)
            current_system_query = """
                SELECT 
                    cpu_usage,
                    ram_usage,
                    ram_used_mb,
                    ram_total_mb,
                    bandwidth_in_mb,
                    bandwidth_out_mb,
                    bandwidth_total_mb
                FROM system_metrics
                ORDER BY created_at DESC
                LIMIT 1
            """
            
            current_system = execute_query(current_system_query)
            current_system_data = current_system[0] if current_system and len(current_system) > 0 else {}
            
            # Format system metrics time series
            system_time_series = []
            for sm in system_metrics:
                created_at = sm.get('created_at')
                if isinstance(created_at, datetime):
                    time_str = created_at.strftime('%Y-%m-%d %H:00:00')
                else:
                    time_str = str(created_at)
                
                system_time_series.append({
                    "time": time_str,
                    "cpu_usage": float(sm.get('cpu_usage', 0) or 0),
                    "ram_usage": float(sm.get('ram_usage', 0) or 0),
                    "ram_used_mb": float(sm.get('ram_used_mb', 0) or 0),
                    "ram_total_mb": float(sm.get('ram_total_mb', 0) or 0),
                    "bandwidth_in_mb": float(sm.get('bandwidth_in_mb', 0) or 0),
                    "bandwidth_out_mb": float(sm.get('bandwidth_out_mb', 0) or 0),
                    "bandwidth_total_mb": float(sm.get('bandwidth_total_mb', 0) or 0)
                })
            
            response = jsonify({
                "success": True,
                "time_series": [
                    {
                        "time": m.get('time_bucket', ''),
                        "request_count": int(m.get('request_count', 0) or 0),
                        "avg_response_time": float(m.get('avg_response_time', 0) or 0),
                        "max_response_time": float(m.get('max_response_time', 0) or 0),
                        "min_response_time": float(m.get('min_response_time', 0) or 0),
                        "error_count": int(m.get('error_count', 0) or 0),
                        "success_count": int(m.get('success_count', 0) or 0),
                        "client_error_count": int(m.get('client_error_count', 0) or 0),
                        "server_error_count": int(m.get('server_error_count', 0) or 0)
                    }
                    for m in metrics
                ],
                "current": {
                    "request_count": int(current.get('request_count', 0) or 0),
                    "avg_response_time": float(current.get('avg_response_time', 0) or 0),
                    "error_count": int(current.get('error_count', 0) or 0),
                    "success_count": int(current.get('success_count', 0) or 0)
                },
                "top_endpoints": [
                    {
                        "endpoint": e.get('endpoint', ''),
                        "method": e.get('method', ''),
                        "request_count": int(e.get('request_count', 0) or 0),
                        "avg_response_time": float(e.get('avg_response_time', 0) or 0),
                        "error_count": int(e.get('error_count', 0) or 0)
                    }
                    for e in top_endpoints
                ],
                "cache_stats": cache_stats,
                "system_metrics": {
                    "time_series": system_time_series,
                    "current": {
                        "cpu_usage": float(current_system_data.get('cpu_usage', 0) or 0),
                        "ram_usage": float(current_system_data.get('ram_usage', 0) or 0),
                        "ram_used_mb": float(current_system_data.get('ram_used_mb', 0) or 0),
                        "ram_total_mb": float(current_system_data.get('ram_total_mb', 0) or 0),
                        "bandwidth_in_mb": float(current_system_data.get('bandwidth_in_mb', 0) or 0),
                        "bandwidth_out_mb": float(current_system_data.get('bandwidth_out_mb', 0) or 0),
                        "bandwidth_total_mb": float(current_system_data.get('bandwidth_total_mb', 0) or 0)
                    }
                }
            })
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
            
        except Exception as e:
            print(f"Error fetching application metrics: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching application metrics: {str(e)}")
    
    @app.route("/api/admin/metrics/collect-app", methods=["POST", "OPTIONS"])
    def collect_app_metrics():
        """Collect and store frontend application-specific metrics (CPU, RAM, Bandwidth)"""
        # Handle OPTIONS request for CORS preflight
        if request.method == "OPTIONS":
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        
        try:
            data = request.get_json()
            if not data:
                response = jsonify({
                    "success": False,
                    "error": "No data provided"
                })
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response, 400
            
            # Extract metrics from request
            cpu_usage = float(data.get('cpu_usage', 0))
            ram_usage = float(data.get('ram_usage', 0))
            ram_used_mb = float(data.get('ram_used_mb', 0))
            ram_total_mb = float(data.get('ram_total_mb', 0))
            bandwidth_in_mb = float(data.get('bandwidth_in_mb', 0))
            bandwidth_out_mb = float(data.get('bandwidth_out_mb', 0))
            bandwidth_total_mb = float(data.get('bandwidth_total_mb', 0))
            
            # Validate values
            cpu_usage = max(0, min(100, cpu_usage))
            ram_usage = max(0, min(100, ram_usage))
            ram_used_mb = max(0, ram_used_mb)
            ram_total_mb = max(0, ram_total_mb)
            bandwidth_in_mb = max(0, bandwidth_in_mb)
            bandwidth_out_mb = max(0, bandwidth_out_mb)
            bandwidth_total_mb = max(0, bandwidth_total_mb)
            
            # Create application_metrics table if it doesn't exist
            create_app_metrics_table_query = """
                CREATE TABLE IF NOT EXISTS application_metrics_frontend (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    cpu_usage DECIMAL(5, 2) NOT NULL COMMENT 'Frontend application CPU usage percentage',
                    ram_usage DECIMAL(5, 2) NOT NULL COMMENT 'Frontend application RAM usage percentage',
                    ram_used_mb DECIMAL(10, 2) NOT NULL COMMENT 'Frontend application RAM used in MB',
                    ram_total_mb DECIMAL(10, 2) NOT NULL COMMENT 'Frontend application total RAM in MB',
                    bandwidth_in_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Frontend application bandwidth in (MB)',
                    bandwidth_out_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Frontend application bandwidth out (MB)',
                    bandwidth_total_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Frontend application total bandwidth (MB)',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_created_at (created_at),
                    INDEX idx_created_at_desc (created_at DESC)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            try:
                execute_update(create_app_metrics_table_query)
            except Exception as table_error:
                print(f"Warning: Could not create application_metrics_frontend table: {str(table_error)}")
                traceback.print_exc()
            
            # Insert metrics
            insert_query = """
                INSERT INTO application_metrics_frontend 
                (cpu_usage, ram_usage, ram_used_mb, ram_total_mb, bandwidth_in_mb, bandwidth_out_mb, bandwidth_total_mb)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            execute_update(insert_query, (
                cpu_usage, ram_usage, ram_used_mb, ram_total_mb,
                bandwidth_in_mb, bandwidth_out_mb, bandwidth_total_mb
            ))
            
            response = jsonify({
                "success": True,
                "message": "Metrics collected successfully"
            })
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Exception as e:
            error_msg = str(e)
            print(f"Error collecting app metrics: {error_msg}")
            traceback.print_exc()
            response = jsonify({
                "success": False,
                "error": f"Error collecting metrics: {error_msg}"
            })
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 500
