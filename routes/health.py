"""
Health check and basic routes
"""
from flask import jsonify, make_response
from datetime import datetime
from database import test_connection
from utils.cache import inject_versioned_urls
from config import FRONTEND_DIR


def register_health_routes(app):
    """Register health check and basic routes"""
    
    @app.route("/", methods=["GET"])
    def root():
        """Serve the main index page with cache-busted static files"""
        index_path = FRONTEND_DIR / "index.html"
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            html_content = inject_versioned_urls(html_content, FRONTEND_DIR)
            
            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        return jsonify({
            "message": "Tirumakudalu Properties API",
            "version": "1.0.0",
            "status": "running"
        })
    
    @app.route("/index.html", methods=["GET"])
    def index_page_html():
        """Serve the index page (with .html extension) with cache-busted static files"""
        index_path = FRONTEND_DIR / "index.html"
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            html_content = inject_versioned_urls(html_content, FRONTEND_DIR)
            
            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        from utils.helpers import abort_with_message
        abort_with_message(404, "Page not found")
    
    @app.route("/api", methods=["GET"])
    def api_root():
        """API root endpoint"""
        return jsonify({
            "message": "Tirumakudalu Properties API",
            "version": "1.0.0",
            "status": "running"
        })
    
    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint"""
        db_status = test_connection()
        return jsonify({
            "status": "healthy" if db_status.get("connected", False) else "unhealthy",
            "database": "connected" if db_status.get("connected", False) else "disconnected",
            "timestamp": datetime.now().isoformat()
        })
    
    @app.route("/api/db/test", methods=["GET"])
    def test_db_connection():
        """Test database connection and return detailed diagnostics"""
        try:
            from database import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB, MYSQL_PORT, ENV_FILE
            
            env_status = {
                "DB_USER": "✓ Set" if MYSQL_USER else "✗ Missing",
                "DB_PASSWORD": "✓ Set" if MYSQL_PASSWORD else "✗ Missing",
                "DB_HOST": MYSQL_HOST or "✗ Missing",
                "DB_NAME": "✓ Set" if MYSQL_DB else "✗ Missing",
                "DB_PORT": MYSQL_PORT
            }
            
            env_file_exists = ENV_FILE.exists() if ENV_FILE else False
            
            db_status = test_connection()
            if db_status.get("connected", False):
                return jsonify({
                    "success": True,
                    "connected": True,
                    "message": "Database connection successful",
                    "details": db_status.get("details", {}),
                    "environment_status": env_status,
                    "env_file_exists": env_file_exists,
                    "env_file_path": str(ENV_FILE) if ENV_FILE else None,
                    "timestamp": datetime.now().isoformat()
                })
            else:
                return jsonify({
                    "success": False,
                    "connected": False,
                    "error": db_status.get("error", "Unknown error"),
                    "details": db_status.get("details", {}),
                    "environment_status": env_status,
                    "env_file_exists": env_file_exists,
                    "env_file_path": str(ENV_FILE) if ENV_FILE else None,
                    "suggestion": db_status.get("suggestion", "Check database configuration"),
                    "help": "For local development: Create a .env file in the project root (see .env.example). For cPanel: Set environment variables in cPanel settings.",
                    "timestamp": datetime.now().isoformat()
                }), 500
        except Exception as e:
            return jsonify({
                "success": False,
                "connected": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }), 500
