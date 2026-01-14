"""
Setup functions for database initialization and admin user creation
"""
import os
from database import execute_query, execute_update
from utils.auth import get_password_hash


def setup_admin_user():
    """Create or update admin user with hashed password"""
    try:
        # Create users table
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(255),
                role VARCHAR(50) DEFAULT 'admin' CHECK (role IN ('admin', 'user')),
                is_active TINYINT(1) DEFAULT 1,
                last_login TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """
        try:
            execute_update(create_table_query)
        except Exception as e:
            print(f"Note: Users table creation: {str(e)}")
        
        # Create visitor_info table
        create_visitor_table_query = """
            CREATE TABLE IF NOT EXISTS visitor_info (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                looking_for TEXT,
                ip_address VARCHAR(45),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        try:
            execute_update(create_visitor_table_query)
            print("✓ Visitor info table created/verified")
        except Exception as e:
            print(f"Note: Visitor info table creation: {str(e)}")
        
        # Create logs table
        create_logs_table_query = """
            CREATE TABLE IF NOT EXISTS logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                log_type VARCHAR(50) NOT NULL,
                action VARCHAR(100) NOT NULL,
                description TEXT,
                user_email VARCHAR(255),
                ip_address VARCHAR(45),
                user_agent TEXT,
                metadata JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_log_type (log_type),
                INDEX idx_created_at (created_at),
                INDEX idx_action (action)
            )
        """
        try:
            execute_update(create_logs_table_query)
            print("✓ Logs table created/verified")
        except Exception as e:
            print(f"Note: Logs table creation: {str(e)}")
        
        # Create blogs table
        create_blogs_table_query = """
            CREATE TABLE IF NOT EXISTS blogs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                excerpt TEXT,
                content LONGTEXT,
                category VARCHAR(100),
                tags JSON,
                image_url LONGTEXT,
                author VARCHAR(255) DEFAULT 'Tirumakudalu Properties',
                views INT DEFAULT 0,
                is_featured TINYINT(1) DEFAULT 0,
                is_active TINYINT(1) DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_category (category),
                INDEX idx_is_active (is_active),
                INDEX idx_is_featured (is_featured),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        try:
            execute_update(create_blogs_table_query)
            print("✓ Blogs table created/verified")
        except Exception as e:
            print(f"Note: Blogs table creation: {str(e)}")
        
        # Create system_metrics table (permanent storage for graphs)
        create_system_metrics_table_query = """
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cpu_usage DECIMAL(5, 2) NOT NULL COMMENT 'CPU usage percentage',
                ram_usage DECIMAL(5, 2) NOT NULL COMMENT 'RAM usage percentage',
                ram_used_mb DECIMAL(10, 2) NOT NULL COMMENT 'RAM used in MB',
                ram_total_mb DECIMAL(10, 2) NOT NULL COMMENT 'Total RAM in MB',
                bandwidth_in_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth in (MB)',
                bandwidth_out_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth out (MB)',
                bandwidth_total_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Total bandwidth (MB)',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_created_at (created_at),
                INDEX idx_created_at_desc (created_at DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        try:
            execute_update(create_system_metrics_table_query)
            print("✓ System metrics table created/verified")
        except Exception as e:
            print(f"Note: System metrics table creation: {str(e)}")
        
        # Create temporary_metrics table (temporary storage for stat cards)
        create_temp_metrics_table_query = """
            CREATE TABLE IF NOT EXISTS temporary_metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cpu_usage DECIMAL(5, 2) NOT NULL COMMENT 'CPU usage percentage',
                ram_usage DECIMAL(5, 2) NOT NULL COMMENT 'RAM usage percentage',
                ram_used_mb DECIMAL(10, 2) NOT NULL COMMENT 'RAM used in MB',
                ram_total_mb DECIMAL(10, 2) NOT NULL COMMENT 'Total RAM in MB',
                bandwidth_in_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth in (MB)',
                bandwidth_out_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth out (MB)',
                bandwidth_total_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Total bandwidth (MB)',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_created_at (created_at),
                INDEX idx_created_at_desc (created_at DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        try:
            execute_update(create_temp_metrics_table_query)
            print("✓ Temporary metrics table created/verified")
        except Exception as e:
            print(f"Note: Temporary metrics table creation: {str(e)}")
        
        # Get admin credentials from environment
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")
        
        if not email:
            print("Warning: ADMIN_EMAIL not set. Skipping admin user setup.")
            return
        
        if not password:
            print("Warning: ADMIN_PASSWORD not set. Skipping admin user setup.")
            return
        
        password_hash = get_password_hash(password)
        
        users = execute_query("SELECT id FROM users WHERE email = %s", (email,))
        
        if users and len(users) > 0:
            update_query = "UPDATE users SET password_hash = %s, is_active = 1 WHERE email = %s"
            execute_update(update_query, (password_hash, email))
            print(f"✓ Admin user updated: {email}")
        else:
            insert_query = "INSERT INTO users (email, password_hash, full_name, role, is_active) VALUES (%s, %s, %s, %s, %s)"
            execute_update(insert_query, (email, password_hash, "Admin User", "admin", True))
            print(f"✓ Admin user created: {email}")
        
        print(f"  Admin user configured - Email: {email}")
    except Exception as e:
        print(f"Error setting up admin user: {str(e)}")
