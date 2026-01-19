"""
Flask Application for Tirumakudalu Properties
Streamlined main API server - routes are organized in separate modules
"""
import time
print("APP BOOT TIME:", time.time())

from flask import Flask, request, url_for, jsonify, send_file, abort, make_response
from flask_cors import CORS
import os
from pathlib import Path
from dotenv import load_dotenv
import threading

# Load environment variables
from config import PROJECT_ROOT, ENV_FILE, FRONTEND_DIR
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)
else:
    load_dotenv()

from database import (
    init_db_pool, test_connection, execute_update
)
from utils.setup import setup_admin_user
from utils.helpers import get_client_ip

# Get debug mode from environment
DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"

# Initialize Flask app with frontend directory as static folder
# This allows Flask to serve static files from the frontend directory
app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path='')

# Session configuration
SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32).hex())
app.config['SECRET_KEY'] = SECRET_KEY

# Session cookie configuration for cross-origin support (cPanel production)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE_FORCE'] = False

# For local development (HTTP), use Lax instead of None
if DEBUG_MODE and not os.getenv("FORCE_HTTPS", "False").lower() == "true":
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False

# Cache busting configuration
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year

def static_versioned(endpoint, **values):
    """Automatically append version parameter to static file URLs"""
    if endpoint == 'static':
        filename = values.get('filename')
        if filename:
            static_dir = os.path.join(os.path.dirname(__file__), 'static')
            file_path = os.path.join(static_dir, filename)
            if os.path.exists(file_path):
                values['v'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.context_processor
def override_url_for():
    """Override url_for to automatically version static files"""
    return dict(url_for=static_versioned)

# CORS configuration
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins_str == "*":
    if not DEBUG_MODE:
        print("WARNING: CORS is set to allow all origins. For production, set ALLOWED_ORIGINS to specific domains.")
        allowed_origins = ["*"]
    else:
        allowed_origins = ["*"]
else:
    allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

CORS(app, 
     origins=allowed_origins if allowed_origins else [],
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "X-Requested-With", "X-Admin-Email"])

# Frontend directory is imported from config module above
# This ensures consistent path handling across all modules

# Initialize database on app startup
print("Starting Tirumakudalu Properties API...")
if init_db_pool():
    if test_connection():
        print("Database connection successful!")
        setup_admin_user()
        # Create application_metrics table if it doesn't exist
        try:
            create_app_metrics_table = """
                CREATE TABLE IF NOT EXISTS application_metrics (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    endpoint VARCHAR(255) NOT NULL COMMENT 'API endpoint path',
                    method VARCHAR(10) NOT NULL COMMENT 'HTTP method',
                    response_time_ms DECIMAL(10, 2) NOT NULL COMMENT 'Response time in milliseconds',
                    status_code INT NOT NULL COMMENT 'HTTP status code',
                    is_error BOOLEAN DEFAULT FALSE COMMENT 'Whether the request resulted in an error',
                    ip_address VARCHAR(45) NULL COMMENT 'Client IP address',
                    user_agent TEXT NULL COMMENT 'User agent string',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_endpoint (endpoint),
                    INDEX idx_method (method),
                    INDEX idx_status_code (status_code),
                    INDEX idx_created_at (created_at),
                    INDEX idx_endpoint_created (endpoint, created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            execute_update(create_app_metrics_table)
            print("Application metrics table ready")
        except Exception as e:
            print(f"Warning: Could not create application_metrics table: {str(e)}")
    else:
        print("Warning: Database connection test failed")
else:
    print("Warning: Database pool initialization failed")

# Application metrics tracking middleware
@app.before_request
def track_request_start():
    """Track request start time for response time calculation"""
    request.start_time = time.time()

@app.after_request
def track_request_metrics(response):
    """Track application metrics for each API request"""
    try:
        # Skip tracking for static files and certain endpoints
        path = request.path
        if (path.startswith('/static/') or 
            path.startswith('/images/') or 
            path.startswith('/favicon') or
            path == '/' or
            'metrics' in path.lower()):
            return response
        
        # Calculate response time
        if hasattr(request, 'start_time'):
            response_time_ms = (time.time() - request.start_time) * 1000
        else:
            response_time_ms = 0
        
        # Get request details
        endpoint = path
        method = request.method
        status_code = response.status_code
        is_error = status_code >= 400
        ip_address = get_client_ip()
        user_agent = request.headers.get('User-Agent', '')[:500]
        
        # Store metrics in database (async in background)
        def store_metrics():
            try:
                query = """
                    INSERT INTO application_metrics 
                    (endpoint, method, response_time_ms, status_code, is_error, ip_address, user_agent)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                execute_update(query, (
                    endpoint, method, response_time_ms, status_code, 
                    is_error, ip_address, user_agent
                ))
            except Exception:
                pass
        
        # Store in background thread
        thread = threading.Thread(target=store_metrics)
        thread.daemon = True
        thread.start()
        
    except Exception:
        pass
    
    return response

# Import all routes
# Routes are organized in separate modules to keep app.py manageable
# Import route modules - they will register routes on the app instance
try:
    # Import route modules - they register routes via register functions
    from routes import auth, health, properties, partners, testimonials, stats, metrics, cities, amenities, unit_types, logs, blogs, inquiries, visitor_info
    auth.register_auth_routes(app)
    health.register_health_routes(app)
    properties.register_properties_routes(app)
    partners.register_partners_routes(app)
    testimonials.register_testimonials_routes(app)
    stats.register_stats_routes(app)
    metrics.register_metrics_routes(app)
    cities.register_cities_routes(app)
    amenities.register_amenities_routes(app)
    unit_types.register_unit_types_routes(app)
    logs.register_logs_routes(app)
    blogs.register_blogs_routes(app)
    inquiries.register_inquiries_routes(app)
    visitor_info.register_visitor_info_routes(app)
    print("✓ Core route modules loaded successfully")
    
    # Import remaining routes from old app.py
    # NOTE: This is a temporary solution to avoid breaking functionality
    # Routes will be gradually moved to separate modules
    print("Loading remaining routes from backup...")
    # Try to find backup file in various locations
    old_app_path = Path(__file__).parent / "app.py.backup"
    if not old_app_path.exists():
        # Try in parent directory documents folder
        old_app_path = Path(__file__).parent.parent / "doccuments" / "app.py.backup"
    if not old_app_path.exists():
        print("Warning: No backup app.py found. Some routes may not be available.")
        old_app_path = None
    
    if old_app_path and old_app_path.exists():
        # Import the old app module and copy route registrations
        # We'll import it and register routes on our app instance
        import importlib.util
        spec = importlib.util.spec_from_file_location("old_app_routes", old_app_path)
        old_app_module = importlib.util.module_from_spec(spec)
        
        # Create a mock Flask app for the old module to use
        # Then we'll copy routes to our app
        class MockApp:
            def route(self, *args, **kwargs):
                def decorator(f):
                    # Register the route on our actual app
                    app.route(*args, **kwargs)(f)
                    return f
                return decorator
        
        # Set up the old module's namespace
        import sys
        old_namespace = {
            'app': MockApp(),
            'Flask': Flask,
            'request': request,
            'jsonify': jsonify,
            'send_file': send_file,
            'abort': abort,
            'make_response': make_response,
            'url_for': url_for,
            'CORS': CORS,
        }
        
        # Import all dependencies into namespace
        from database import get_db_cursor, execute_query, execute_update, execute_insert, test_connection
        from schemas import *
        from models import *
        from utils.helpers import *
        from utils.auth import *
        from utils.email import *
        from utils.cache import *
        import os, json, traceback, threading, time, base64, uuid, csv, io, re
        from datetime import datetime
        from typing import List, Optional, Tuple
        from pathlib import Path
        from pydantic import ValidationError
        
        old_namespace.update({
            'get_db_cursor': get_db_cursor,
            'execute_query': execute_query,
            'execute_update': execute_update,
            'execute_insert': execute_insert,
            'os': os,
            'json': json,
            'traceback': traceback,
            'threading': threading,
            'time': time,
            'base64': base64,
            'uuid': uuid,
            'csv': csv,
            'io': io,
            're': re,
            'datetime': datetime,
            'List': List,
            'Optional': Optional,
            'Tuple': Tuple,
            'Path': Path,
            'FRONTEND_DIR': FRONTEND_DIR,
            'PROJECT_ROOT': PROJECT_ROOT,
        })
        # Import config module paths into namespace
        # This ensures old routes use the same paths as new routes
        from config import FRONTEND_DIR as CONFIG_FRONTEND_DIR, IMAGES_DIR, PROJECT_ROOT as CONFIG_PROJECT_ROOT
        old_namespace['FRONTEND_DIR'] = CONFIG_FRONTEND_DIR
        old_namespace['IMAGES_DIR'] = IMAGES_DIR
        old_namespace['PROJECT_ROOT'] = CONFIG_PROJECT_ROOT
        # For backward compatibility, also set BASE_DIR
        old_namespace['BASE_DIR'] = CONFIG_PROJECT_ROOT
        old_namespace.update(globals())
        
        # Load the old app module (this will register routes via MockApp)
        try:
            spec.loader.exec_module(old_app_module)
            # Routes are now registered on our app via MockApp
            print("✓ Routes from backup app.py loaded successfully")
        except Exception as load_error:
            print(f"Warning: Error loading routes from backup: {load_error}")
            import traceback
            traceback.print_exc()
    else:
        print("Warning: Backup app.py not found. Some routes may not be available.")
        print("Note: Routes should be gradually moved to route modules in backend/routes/")
        
except ImportError as e:
    print(f"Warning: Could not load some route modules: {e}")
    import traceback
    traceback.print_exc()

# Make app available as 'application' for WSGI servers (Passenger, mod_wsgi, etc.)
application = app

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, host="0.0.0.0", port=5000)
