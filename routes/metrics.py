"""
Metrics routes
"""
from flask import request, jsonify
import traceback
from database import execute_update


def register_metrics_routes(app):
    """Register metrics routes"""
    
    @app.route("/api/admin/metrics/collect-app", methods=["POST"])
    def collect_app_metrics():
        """Collect and store frontend application-specific metrics (CPU, RAM, Bandwidth)"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({
                    "success": False,
                    "error": "No data provided"
                }), 400
            
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
            
            return jsonify({
                "success": True,
                "message": "Metrics collected successfully"
            })
        except Exception as e:
            error_msg = str(e)
            print(f"Error collecting app metrics: {error_msg}")
            traceback.print_exc()
            return jsonify({
                "success": False,
                "error": f"Error collecting metrics: {error_msg}"
            }), 500
