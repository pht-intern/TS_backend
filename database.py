from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
import os
from pathlib import Path
from dotenv import load_dotenv
import pymysql.cursors
from urllib.parse import quote_plus

# Load environment variables from .env file (for local development)
# In production (cPanel), environment variables are set in cPanel settings
# Get the project root directory (parent of Backend directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)
else:
    # Try loading from current directory as fallback
    load_dotenv()

# Database Configuration
# SECURITY: All credentials MUST come from environment variables
# For production (cPanel): Set all environment variables in cPanel settings
# For local development: Set in .env file in project root
# NO HARDCODED CREDENTIALS - All values must be set via environment variables

MYSQL_USER = os.getenv('DB_USER')
MYSQL_PASSWORD = os.getenv('DB_PASSWORD')
# For cPanel: DB_HOST is usually 'localhost', but can be the database server hostname
# If not set, default to 'localhost' for cPanel compatibility
MYSQL_HOST = os.getenv('DB_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('DB_PORT', '3306'))
MYSQL_DB = os.getenv('DB_NAME')

# Validate that required credentials are set
# We'll validate when actually connecting, but set defaults to None for now
# This allows the app to start even if env vars aren't set (for better error messages)
def validate_db_credentials():
    """Validate database credentials and raise helpful error if missing"""
    missing_vars = []
    if not MYSQL_USER:
        missing_vars.append('DB_USER')
    if not MYSQL_PASSWORD:
        missing_vars.append('DB_PASSWORD')
    if not MYSQL_HOST:
        missing_vars.append('DB_HOST')
    if not MYSQL_DB:
        missing_vars.append('DB_NAME')
    
    if missing_vars:
        # Check if .env file exists for better error message
        env_exists = ENV_FILE.exists()
        error_msg = f"Missing required database environment variables: {', '.join(missing_vars)}.\n"
        if env_exists:
            error_msg += f"Found .env file at {ENV_FILE}, but variables are missing or empty.\n"
            error_msg += "Please check your .env file and ensure all required variables are set."
        else:
            error_msg += f"No .env file found at {ENV_FILE}.\n"
            error_msg += "For local development: Create a .env file in the project root (see .env.example).\n"
            error_msg += "For cPanel production: Set environment variables in cPanel settings."
        raise ValueError(error_msg)

# Build DATABASE_URL if credentials are available, otherwise set to None
# URL-encode username and password to handle special characters
if MYSQL_USER and MYSQL_PASSWORD and MYSQL_HOST and MYSQL_DB:
    # URL-encode credentials to handle special characters in passwords
    encoded_user = quote_plus(str(MYSQL_USER))
    encoded_password = quote_plus(str(MYSQL_PASSWORD))
    encoded_db = quote_plus(str(MYSQL_DB))
    DATABASE_URL = (
        f"mysql+pymysql://{encoded_user}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{encoded_db}"
    )
else:
    DATABASE_URL = None

# Create SQLAlchemy engine (only if DATABASE_URL is set)
# Validate credentials before creating engine
if DATABASE_URL:
    try:
        validate_db_credentials()
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,       # Avoids stale connections
            pool_recycle=3600,        # Recycles connections every hour
            pool_size=10,             # Number of connections to maintain
            max_overflow=20,          # Maximum overflow connections
            pool_timeout=30,          # Timeout for getting connection from pool
            echo=False,               # Set True for SQL debug logs
            connect_args={
                "charset": "utf8mb4",
                "connect_timeout": 10,  # Connection timeout in seconds
                "read_timeout": 30,     # Read timeout in seconds
                "write_timeout": 30     # Write timeout in seconds
            },
            execution_options={
                "isolation_level": "READ COMMITTED"  # Use READ COMMITTED for better consistency with connection pooling
            }
        )
        # Test the connection immediately to catch errors early
        try:
            with engine.connect() as test_conn:
                test_conn.execute(text("SELECT 1"))
            print(f"✓ Database connection successful: {MYSQL_DB}@{MYSQL_HOST}")
        except Exception as conn_error:
            error_msg = str(conn_error)
            print(f"✗ Database connection test failed: {error_msg}")
            # Provide helpful error messages for common cPanel issues
            if "Access denied" in error_msg:
                print("\n" + "="*60)
                print("DATABASE CONNECTION ERROR - Access Denied")
                print("="*60)
                print(f"User: {MYSQL_USER}")
                print(f"Host: {MYSQL_HOST}")
                print(f"Database: {MYSQL_DB}")
                print("\nCommon causes:")
                print("1. Incorrect password - Check DB_PASSWORD in cPanel environment variables")
                print("2. Wrong username - Verify DB_USER matches your cPanel database user")
                print("3. User not granted access - Check database user privileges in cPanel")
                print("4. Wrong host - For cPanel, DB_HOST should usually be 'localhost'")
                print("\nTo fix:")
                print("- Go to cPanel > Environment Variables")
                print("- Verify DB_USER, DB_PASSWORD, DB_HOST, and DB_NAME are set correctly")
                print("- Check cPanel > MySQL Databases to verify user has access to database")
                print("="*60 + "\n")
            elif "Unknown database" in error_msg:
                print(f"\n✗ Database '{MYSQL_DB}' does not exist. Check DB_NAME in environment variables.")
            elif "Can't connect" in error_msg or "Connection refused" in error_msg:
                print(f"\n✗ Cannot connect to MySQL server at {MYSQL_HOST}:{MYSQL_PORT}")
                print("   For cPanel, DB_HOST should usually be 'localhost'")
            engine = None
    except ValueError as e:
        print(f"Database configuration error: {e}")
        engine = None
else:
    engine = None

# Session factory (only if engine is available)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None

# Base class for models
Base = declarative_base()

# Database session dependency for routes
def get_db():
    if SessionLocal is None:
        validate_db_credentials()  # This will raise a helpful error
        raise RuntimeError("Database session factory not initialized. Check environment variables.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================
# HELPER FUNCTIONS FOR RAW SQL QUERIES
# ============================================

def init_db_pool():
    """Initialize database connection (for compatibility)"""
    try:
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"Database connection pool initialized: {MYSQL_DB}@{MYSQL_HOST}")
        return True
    except Exception as e:
        print(f"Error initializing database pool: {e}")
        return False


def close_db_pool():
    """Close database connections (for compatibility)"""
    try:
        engine.dispose()
        print("Database connection pool closed")
    except Exception as e:
        print(f"Error closing database pool: {e}")


def test_connection() -> dict:
    """Test database connection and return detailed status"""
    result = {
        "connected": False,
        "error": None,
        "details": {}
    }
    
    if engine is None:
        result["error"] = "Database engine not initialized. Check environment variables."
        result["details"] = {
            "DB_USER": "✓ Set" if MYSQL_USER else "✗ Missing",
            "DB_PASSWORD": "✓ Set" if MYSQL_PASSWORD else "✗ Missing",
            "DB_HOST": MYSQL_HOST or "✗ Missing",
            "DB_NAME": "✓ Set" if MYSQL_DB else "✗ Missing",
            "DB_PORT": MYSQL_PORT
        }
        return result
    
    try:
        with engine.connect() as conn:
            result_query = conn.execute(text("SELECT 1 as test, DATABASE() as db, USER() as user"))
            row = result_query.fetchone()
            result["connected"] = True
            result["details"] = {
                "database": row.db if row else "Unknown",
                "user": row.user if row else "Unknown",
                "host": MYSQL_HOST,
                "port": MYSQL_PORT
            }
    except Exception as e:
        error_msg = str(e)
        result["error"] = error_msg
        result["details"] = {
            "user": MYSQL_USER or "Not set",
            "host": MYSQL_HOST or "Not set",
            "database": MYSQL_DB or "Not set",
            "port": MYSQL_PORT
        }
        # Add helpful suggestions
        if "Access denied" in error_msg:
            result["suggestion"] = "Check DB_PASSWORD and DB_USER in cPanel environment variables. Verify user has access to database."
        elif "Unknown database" in error_msg:
            result["suggestion"] = f"Database '{MYSQL_DB}' does not exist. Check DB_NAME in environment variables."
        elif "Can't connect" in error_msg:
            result["suggestion"] = f"Cannot reach MySQL server. For cPanel, DB_HOST should usually be 'localhost'."
    
    return result


@contextmanager
def get_db_cursor(commit=True):
    """Context manager for database cursors (for compatibility)"""
    if engine is None:
        validate_db_credentials()  # This will raise a helpful error
        raise RuntimeError("Database engine not initialized. Check environment variables.")
    
    raw_conn = None
    try:
        raw_conn = engine.raw_connection()
        cursor = raw_conn.cursor()
        try:
            yield cursor
            if commit:
                raw_conn.commit()
            else:
                raw_conn.rollback()
        except Exception as e:
            if raw_conn:
                raw_conn.rollback()
            print(f"Database cursor error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise e
        finally:
            if cursor:
                cursor.close()
    except Exception as e:
        if raw_conn:
            raw_conn.rollback()
        raise e
    finally:
        if raw_conn:
            raw_conn.close()


def execute_query(query: str, params: tuple = None) -> list:
    """Execute a SELECT query and return results as list of dicts"""
    if engine is None:
        validate_db_credentials()  # This will raise a helpful error
        raise RuntimeError("Database engine not initialized. Check environment variables.")
    
    # Use raw connection for MySQL-style %s placeholders
    raw_conn = None
    try:
        raw_conn = engine.raw_connection()
        # Set isolation level to READ COMMITTED to see latest committed data immediately
        # This is critical for connection pooling to work correctly with fresh data
        try:
            temp_cursor = raw_conn.cursor()
            temp_cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
            temp_cursor.close()
            raw_conn.commit()
        except:
            pass  # Ignore if setting fails, connection will use default
        # Ensure autocommit is enabled for read queries to see latest data
        raw_conn.autocommit(True)
        # Use DictCursor to automatically return results as dictionaries
        cursor = raw_conn.cursor(pymysql.cursors.DictCursor)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Fetch all results (already as dictionaries with DictCursor)
            rows = cursor.fetchall()
            
            # Convert to list (DictCursor already returns dicts, but ensure it's a list)
            return list(rows) if rows else []
        finally:
            cursor.close()
            # No commit needed for SELECT queries - autocommit handles it
    except Exception as e:
        print(f"Database query error: {str(e)}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        if raw_conn:
            # Reset connection state before returning to pool
            try:
                raw_conn.rollback()  # Clear any transaction state
            except:
                pass
            raw_conn.close()


def execute_update(query: str, params: tuple = None) -> int:
    """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
    if engine is None:
        validate_db_credentials()  # This will raise a helpful error
        raise RuntimeError("Database engine not initialized. Check environment variables.")
    
    # Import validation utilities
    from utils.db_validator import (
        validate_column_count, auto_sanitize_params,
        sanitize_params_for_update
    )
    
    # Use raw connection for MySQL-style %s placeholders
    raw_conn = None
    try:
        # Validate and sanitize parameters before execution
        if params:
            try:
                # First validate column count
                validate_column_count(query, params)
            except ValueError as ve:
                print(f"❌ SQL VALIDATION ERROR: {ve}")
                raise
        
        # Auto-sanitize parameters for common issues
        sanitized_params = auto_sanitize_params(params) if params else None
        
        raw_conn = engine.raw_connection()
        # Explicitly disable autocommit to ensure transaction control
        raw_conn.autocommit(False)
        cursor = raw_conn.cursor()
        try:
            if sanitized_params:
                cursor.execute(query, sanitized_params)
            else:
                cursor.execute(query)
            # Explicitly commit the transaction
            raw_conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows
        except Exception as e:
            if raw_conn:
                raw_conn.rollback()
            error_msg = str(e)
            # Duplicate column (1060) is harmless when running migrations – column already exists; don't log
            if "Duplicate column name" in error_msg or "1060" in error_msg:
                raise e
            print(f"❌ DATABASE UPDATE ERROR: {error_msg}")
            print(f"❌ QUERY: {query[:500]}")  # Truncate long queries
            print(f"❌ PARAMS: {sanitized_params}")
            # Provide helpful error messages for common MySQL errors
            if "Column" in error_msg and "cannot be null" in error_msg:
                print("💡 TIP: A NOT NULL column received NULL. Check your data sanitization.")
            elif "Incorrect integer value" in error_msg or "Incorrect double value" in error_msg:
                print("💡 TIP: Empty string or invalid value sent to numeric column. Use None for NULL values.")
            elif "Data too long" in error_msg or "Data truncated" in error_msg:
                print("💡 TIP: String value exceeds column length. Truncate before inserting.")
            elif "Cannot add or update a child row" in error_msg and "foreign key constraint" in error_msg:
                print("💡 TIP: Foreign key constraint violation. Check that referenced ID exists.")
            elif "Invalid JSON" in error_msg or "JSON text" in error_msg:
                print("💡 TIP: Invalid JSON sent to JSON column. Use json.dumps() for Python objects.")
            import traceback
            traceback.print_exc()
            raise e
        finally:
            cursor.close()
    finally:
        if raw_conn:
            raw_conn.close()


def execute_insert(query: str, params: tuple = None) -> int:
    """Execute an INSERT query and return the inserted row ID"""
    if engine is None:
        validate_db_credentials()  # This will raise a helpful error
        raise RuntimeError("Database engine not initialized. Check environment variables.")
    
    # Import validation utilities
    from utils.db_validator import (
        validate_column_count, auto_sanitize_params,
        sanitize_params_for_insert
    )
    
    # Use raw connection for MySQL-style %s placeholders
    raw_conn = None
    try:
        # Validate and sanitize parameters before execution
        if params:
            try:
                # First validate column count
                validate_column_count(query, params)
            except ValueError as ve:
                print(f"❌ SQL VALIDATION ERROR: {ve}")
                raise
        
        # Auto-sanitize parameters for common issues
        sanitized_params = auto_sanitize_params(params) if params else None
        
        raw_conn = engine.raw_connection()
        # Explicitly disable autocommit to ensure transaction control
        raw_conn.autocommit(False)
        cursor = raw_conn.cursor()
        try:
            if sanitized_params:
                cursor.execute(query, sanitized_params)
            else:
                cursor.execute(query)
            # Explicitly commit the transaction
            raw_conn.commit()
            return cursor.lastrowid
        except Exception as e:
            if raw_conn:
                raw_conn.rollback()
            error_msg = str(e)
            print("❌ MYSQL INSERT ERROR:", error_msg)
            print(f"❌ QUERY: {query[:500]}")  # Truncate long queries
            print(f"❌ PARAMS: {sanitized_params}")
            
            # Provide helpful error messages for common MySQL errors
            if "Column" in error_msg and "cannot be null" in error_msg:
                print("💡 TIP: A NOT NULL column received NULL. Check your data sanitization.")
            elif "Incorrect integer value" in error_msg or "Incorrect double value" in error_msg:
                print("💡 TIP: Empty string or invalid value sent to numeric column. Use None for NULL values.")
            elif "Data too long" in error_msg or "Data truncated" in error_msg:
                print("💡 TIP: String value exceeds column length. Truncate before inserting.")
            elif "Cannot add or update a child row" in error_msg and "foreign key constraint" in error_msg:
                print("💡 TIP: Foreign key constraint violation. Check that referenced ID exists.")
            elif "Invalid JSON" in error_msg or "JSON text" in error_msg:
                print("💡 TIP: Invalid JSON sent to JSON column. Use json.dumps() for Python objects.")
            
            import traceback
            traceback.print_exc()
            raise
        finally:
            cursor.close()
    finally:
        if raw_conn:
            raw_conn.close()
