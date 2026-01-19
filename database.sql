-- Tirumakudalu Properties Database Schema
-- This SQL script creates all necessary tables for the real estate property management system
-- Note: Admin user is managed in a separate database

-- ============================================
-- SEPARATE PROPERTY TABLES FOR DIFFERENT CATEGORIES
-- This section creates tables for residential properties and plot properties
-- ============================================

-- ============================================
-- RESIDENTIAL PROPERTIES TABLE
-- For: Builder Floor, House/Villa, Apartments
-- ============================================
CREATE TABLE IF NOT EXISTS residential_properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(250) NOT NULL,
    locality VARCHAR(250) NOT NULL,
    property_name VARCHAR(250) NOT NULL,
    unit_type VARCHAR(50) NOT NULL CHECK (unit_type IN ('rk', 'bhk', '4plus')),
    bedrooms INT NOT NULL, -- 0 for RK, 1-3 for BHK, 4+ for 4+BHK
    bathrooms DECIMAL(3, 1) DEFAULT 0 COMMENT 'Number of bathrooms',
    buildup_area DECIMAL(10, 2) NOT NULL COMMENT 'Buildup area in square feet',
    carpet_area DECIMAL(10, 2) NOT NULL COMMENT 'Carpet area in square feet',
    super_built_up_area DECIMAL(10, 2) NULL COMMENT 'Super built-up area in square feet',
    price DECIMAL(12, 2) NOT NULL,
    price_text VARCHAR(500) NULL, -- Original price text
    price_negotiable TINYINT(1) DEFAULT 0,
    price_includes_registration TINYINT(1) DEFAULT 0,
    type VARCHAR(50) NOT NULL CHECK (type IN ('builder_floor', 'house', 'villa', 'apartment')),
    status VARCHAR(20) NOT NULL CHECK (status IN ('sale', 'rent', 'resale', 'new')),
    property_status VARCHAR(50) NULL, -- resale, new, ready_to_move, under_construction
    description TEXT,
    location_link TEXT NULL COMMENT 'Google Maps location link',
    directions TEXT NULL COMMENT 'Directions to the property',
    length DECIMAL(10, 2) NULL COMMENT 'Property length in feet',
    breadth DECIMAL(10, 2) NULL COMMENT 'Property breadth in feet',
    builder VARCHAR(250) NULL COMMENT 'Builder/Developer name',
    configuration VARCHAR(250) NULL COMMENT 'Property configuration details',
    total_flats INT NULL COMMENT 'Total number of flats in the building',
    total_floors INT NULL COMMENT 'Total number of floors in the building',
    total_acres DECIMAL(10, 2) NULL COMMENT 'Total area in acres (for large projects)',
    is_featured TINYINT(1) DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_city (city),
    INDEX idx_locality (locality),
    INDEX idx_type (type),
    INDEX idx_status (status),
    INDEX idx_property_status (property_status),
    INDEX idx_is_active (is_active),
    INDEX idx_is_featured (is_featured),
    INDEX idx_price (price),
    INDEX idx_created_at (created_at),
    INDEX idx_builder (builder)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- PLOT PROPERTIES TABLE
-- For: Plots
-- ============================================
CREATE TABLE IF NOT EXISTS plot_properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(250) NOT NULL,
    locality VARCHAR(250) NOT NULL,
    project_name VARCHAR(250) NOT NULL,
    plot_area DECIMAL(10, 2) NOT NULL COMMENT 'Plot area in square feet',
    plot_length DECIMAL(10, 2) NOT NULL COMMENT 'Plot length in feet',
    plot_breadth DECIMAL(10, 2) NOT NULL COMMENT 'Plot breadth in feet',
    price DECIMAL(12, 2) NOT NULL,
    price_text VARCHAR(500) NULL, -- Original price text
    price_negotiable TINYINT(1) DEFAULT 0,
    price_includes_registration TINYINT(1) DEFAULT 0,
    status VARCHAR(20) NOT NULL CHECK (status IN ('sale', 'rent', 'resale', 'new')),
    property_status VARCHAR(50) NULL, -- resale, new, ready_to_move, under_construction
    description TEXT,
    location_link TEXT NULL COMMENT 'Google Maps location link',
    directions TEXT NULL COMMENT 'Directions to the property',
    builder VARCHAR(250) NULL COMMENT 'Builder/Developer name',
    total_acres DECIMAL(10, 2) NULL COMMENT 'Total area in acres (for large projects)',
    is_featured TINYINT(1) DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_city (city),
    INDEX idx_locality (locality),
    INDEX idx_status (status),
    INDEX idx_property_status (property_status),
    INDEX idx_is_active (is_active),
    INDEX idx_is_featured (is_featured),
    INDEX idx_price (price),
    INDEX idx_created_at (created_at),
    INDEX idx_builder (builder)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- PROPERTY FEATURES TABLE
-- Unified table for all property features (residential and plot)
-- ============================================
CREATE TABLE IF NOT EXISTS property_features (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_category VARCHAR(50) NOT NULL CHECK (property_category IN ('residential', 'plot')),
    property_id INT NOT NULL,
    feature_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(property_category, property_id, feature_name),
    INDEX idx_property_category (property_category),
    INDEX idx_property_id (property_id),
    INDEX idx_property_category_id (property_category, property_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Note: Foreign key constraints cannot be applied directly since property_id can reference
-- either residential_properties or plot_properties depending on property_category.
-- Application logic should ensure referential integrity.



-- ============================================
-- RESIDENTIAL PROPERTY IMAGES TABLE
-- Unified table for all residential property images (project, floorplan, masterplan)
-- ============================================
CREATE TABLE IF NOT EXISTS residential_property_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    image_url TEXT NOT NULL,
    image_category VARCHAR(50) NOT NULL DEFAULT 'project' CHECK (image_category IN ('project', 'floorplan', 'masterplan')),
    image_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES residential_properties(id) ON DELETE CASCADE,
    INDEX idx_property_id (property_id),
    INDEX idx_image_category (image_category),
    INDEX idx_image_order (image_order),
    INDEX idx_property_category (property_id, image_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- PLOT PROPERTY IMAGES TABLE
-- Unified table for all plot property images (project, floorplan, masterplan)
-- ============================================
CREATE TABLE IF NOT EXISTS plot_property_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    image_url TEXT NOT NULL,
    image_category VARCHAR(50) NOT NULL DEFAULT 'project' CHECK (image_category IN ('project', 'floorplan', 'masterplan')),
    image_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES plot_properties(id) ON DELETE CASCADE,
    INDEX idx_property_id (property_id),
    INDEX idx_image_category (image_category),
    INDEX idx_image_order (image_order),
    INDEX idx_property_category (property_id, image_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- PARTNERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS partners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) NOT NULL UNIQUE,
    logo_url TEXT,
    website_url VARCHAR(500),
    is_active TINYINT(1) DEFAULT 1,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================
-- TESTIMONIALS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_name VARCHAR(250) NOT NULL,
    client_email VARCHAR(250),
    client_phone VARCHAR(20),
    service_type VARCHAR(100),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    message TEXT NOT NULL,
    is_approved TINYINT(1) DEFAULT 0,
    is_featured TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================
-- CONTACT INQUIRIES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS contact_inquiries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    email VARCHAR(250) NOT NULL,
    subject VARCHAR(250),
    message TEXT NOT NULL,
    phone VARCHAR(20),
    property_id INT,
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'read', 'replied', 'closed')),
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================
-- USERS TABLE (for admin authentication)
-- ============================================
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
);

-- ============================================
-- VISITOR INFO TABLE (for popup modal)
-- ============================================
CREATE TABLE IF NOT EXISTS visitor_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    looking_for TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- LOGS TABLE (for tracking activities)
-- ============================================
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
);

-- ============================================
-- APP METRICS PASSWORD TABLE (for securing app-metrics page)
-- ============================================
CREATE TABLE IF NOT EXISTS app_metrics_password (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert App Metrics Password
-- Password: ShRushti@12$2026
-- This password is hashed using bcrypt

INSERT INTO app_metrics_password (password_hash) 
VALUES ('$2b$12$LL0H7CmvuCz2a/mdynj8buqtdGwZDLBV93wD.z7/mm6bSsSzB3rYC');

-- Note: If a password already exists, you can update it instead:
-- UPDATE app_metrics_password SET password_hash = '$2b$12$LL0H7CmvuCz2a/mdynj8buqtdGwZDLBV93wD.z7/mm6bSsSzB3rYC', updated_at = NOW() WHERE id = (SELECT id FROM (SELECT id FROM app_metrics_password ORDER BY id DESC LIMIT 1) AS t);



-- ============================================
-- SYSTEM METRICS TABLE (for monitoring CPU, RAM, bandwidth)
-- Permanent storage for graphs and historical data
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TEMPORARY METRICS TABLE (for stat cards auto-refresh)
-- Temporary storage for real-time stat cards that refresh every 60 seconds
-- Old data is automatically cleaned up (keeps only last 5 minutes)
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- APPLICATION METRICS TABLE (for API endpoint tracking)
-- Tracks API endpoint performance metrics including response times, status codes, and errors
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- APPLICATION METRICS FRONTEND TABLE (for frontend application metrics)
-- Tracks frontend application performance metrics (CPU, RAM, bandwidth)
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- BLOGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS blogs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    excerpt TEXT,
    content LONGTEXT,
    category VARCHAR(100),
    tags JSON,
    image_url LONGTEXT,
    author VARCHAR(250) DEFAULT 'Tirumakudalu Properties',
    views INT DEFAULT 0,
    is_featured TINYINT(1) DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_is_active (is_active),
    INDEX idx_is_featured (is_featured),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- SCHEDULED VISITS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS scheduled_visits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    visitor_name VARCHAR(250) NOT NULL,
    visitor_email VARCHAR(250) NOT NULL,
    visitor_phone VARCHAR(20) NOT NULL,
    property_id INT NULL COMMENT 'Property ID (can be residential or plot property)',
    property_category VARCHAR(50) NULL COMMENT 'Property category: residential or plot',
    visit_date DATE NOT NULL COMMENT 'Scheduled visit date',
    visit_time TIME NOT NULL COMMENT 'Scheduled visit time',
    visit_status VARCHAR(50) DEFAULT 'scheduled' CHECK (visit_status IN ('scheduled', 'confirmed', 'completed', 'cancelled', 'rescheduled')),
    visit_type VARCHAR(50) NULL COMMENT 'Type of visit: site_visit, virtual_tour, consultation, etc.',
    additional_notes TEXT NULL COMMENT 'Additional notes or requirements',
    admin_notes TEXT NULL COMMENT 'Internal admin notes',
    reminder_sent TINYINT(1) DEFAULT 0 COMMENT 'Whether reminder email was sent',
    confirmed_at TIMESTAMP NULL COMMENT 'When the visit was confirmed',
    completed_at TIMESTAMP NULL COMMENT 'When the visit was completed',
    cancelled_at TIMESTAMP NULL COMMENT 'When the visit was cancelled',
    cancelled_reason TEXT NULL COMMENT 'Reason for cancellation',
    ip_address VARCHAR(45) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_visitor_email (visitor_email),
    INDEX idx_visitor_phone (visitor_phone),
    INDEX idx_property_id (property_id),
    INDEX idx_visit_date (visit_date),
    INDEX idx_visit_status (visit_status),
    INDEX idx_created_at (created_at),
    INDEX idx_visit_date_status (visit_date, visit_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Note: Run Backend/setup_admin.py to generate proper password hash
-- This is a placeholder - the setup script will update it with a proper bcrypt hash
INSERT IGNORE INTO users (email, password_hash, full_name, role) VALUES
('seshvasu56@gmail.com', '$2b$12$nUmm3/n2kk8NbDHK1tAQCuFb/Mlv9MQf1DQpa6YZap4aSe.NVN6R6', 'Admin User', 'admin');

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Indexes for contact_inquiries table
CREATE INDEX idx_contact_inquiries_status ON contact_inquiries(status);
CREATE INDEX idx_contact_inquiries_created_at ON contact_inquiries(created_at);

-- Indexes for visitor_info table
CREATE INDEX idx_visitor_info_created_at ON visitor_info(created_at);

-- Indexes for logs table
CREATE INDEX idx_logs_log_type ON logs(log_type);
CREATE INDEX idx_logs_created_at ON logs(created_at);
CREATE INDEX idx_logs_action ON logs(action);

-- Indexes for blogs table
CREATE INDEX idx_blogs_category ON blogs(category);
CREATE INDEX idx_blogs_is_active ON blogs(is_active);
CREATE INDEX idx_blogs_is_featured ON blogs(is_featured);
CREATE INDEX idx_blogs_created_at ON blogs(created_at);

-- Indexes for partners table
CREATE INDEX idx_partners_is_active ON partners(is_active);
CREATE INDEX idx_partners_display_order ON partners(display_order);
CREATE INDEX idx_partners_active_order ON partners(is_active, display_order);

-- Indexes for testimonials table
CREATE INDEX idx_testimonials_is_approved ON testimonials(is_approved);
CREATE INDEX idx_testimonials_is_featured ON testimonials(is_featured);
CREATE INDEX idx_testimonials_approved_featured ON testimonials(is_approved, is_featured);
CREATE INDEX idx_testimonials_created_at ON testimonials(created_at);

-- Indexes for scheduled_visits table
CREATE INDEX idx_scheduled_visits_visitor_email ON scheduled_visits(visitor_email);
CREATE INDEX idx_scheduled_visits_visitor_phone ON scheduled_visits(visitor_phone);
CREATE INDEX idx_scheduled_visits_property_id ON scheduled_visits(property_id);
CREATE INDEX idx_scheduled_visits_visit_date ON scheduled_visits(visit_date);
CREATE INDEX idx_scheduled_visits_visit_status ON scheduled_visits(visit_status);
CREATE INDEX idx_scheduled_visits_created_at ON scheduled_visits(created_at);
CREATE INDEX idx_scheduled_visits_visit_date_status ON scheduled_visits(visit_date, visit_status);

-- ============================================
-- CITIES TABLE (for city activation management)
-- ============================================
CREATE TABLE IF NOT EXISTS cities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    state VARCHAR(250) NOT NULL,
    is_active TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_city_state (name, state),
    INDEX idx_name (name),
    INDEX idx_state (state),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- CATEGORIES TABLE (for property categories)
-- ============================================
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(250) NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- UNIT TYPES TABLE (for property unit types)
-- ============================================
CREATE TABLE IF NOT EXISTS unit_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(250) NOT NULL,
    bedrooms INT NOT NULL DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_bedrooms (bedrooms),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- ============================================
-- INITIAL DATA (OPTIONAL - SEED DATA)
-- ============================================

-- Insert sample partners (all 28 partners)
-- Note: logo_url paths use full server paths for c-panel production environment
INSERT IGNORE INTO partners (name, logo_url, website_url, display_order) VALUES
('ADARSH BUILDERS', '/home/tirumakudaluprop/public_html/images/logos/adarsh-logo.png', 'https://www.adarshdevelopers.com/', 1),
('CHAITANYA BUILDERS', '/home/tirumakudaluprop/public_html/images/logos/chaithanya-logo.png', 'https://www.chaithanya.com/', 2),
('PURAVANKARA BUILDERS', '/home/tirumakudaluprop/public_html/images/logos/purvankara-logo.svg', 'https://www.chaithanya.com/', 3),
('PROVIDENT', '/home/tirumakudaluprop/public_html/images/logos/provident-logo.webp', 'https://www.providenthousing.com/', 4),
('MANTRI BUILDERS', '/home/tirumakudaluprop/public_html/images/logos/mantri-logo.webp', 'https://mantri.in/', 5),
('ELEGANCE INFRA', '/home/tirumakudaluprop/public_html/images/logos/elegance-logo.png', 'https://eleganceinfra.com/', 6),
('PRESTIGE CONSTRUCTIONS', '/home/tirumakudaluprop/public_html/images/logos/prestige-logo.svg', 'https://www.prestigeconstructions.com/', 7),
('SOBHA BUILDERS', '/home/tirumakudaluprop/public_html/images/logos/sobha-logo.jpg', 'https://www.sobha.com/', 8),
('TOTAL ENVIRONMENT', '/home/tirumakudaluprop/public_html/images/logos/totalenvironment-logo.webp', 'https://www.totalenvironmentindia.com/', 9),
('BRIGADE ENTERPRISES', '/home/tirumakudaluprop/public_html/images/logos/brigade-logo.svg', 'https://www.prestigeconstructions.com/', 10),
('FLOW REALTY', '/home/tirumakudaluprop/public_html/images/logos/flow-logo.png', 'https://flowrealty.in/', 11),
('XANADU REALTY', '/home/tirumakudaluprop/public_html/images/logos/xanadu_logo.svg', 'https://www.xanadu.in/', 12),
('PHOENIX BUILDERS', '/home/tirumakudaluprop/public_html/images/logos/phoenix-logo.webp', 'https://www.phoenixbuilders.com/', 13),
('KARLE INFRA', '/home/tirumakudaluprop/public_html/images/logos/Karle-Infra-logo.png', 'https://karleinfra.com/', 14),
('SALARPURIA SATTVA BUILDERS', '/home/tirumakudaluprop/public_html/images/logos/sattva_logo.png', 'https://sattvagroup.com/', 15),
('SHAPOORJEE PALLONJI BUILDERS', '/home/tirumakudaluprop/public_html/images/logos/shapoorji-logo.svg', 'https://shapoorjirealestate.com/', 16),
('TATA HOUSING', '/home/tirumakudaluprop/public_html/images/logos/tata-logo.jpg', 'https://www.tata.com/business/tata-housing', 17),
('MAHINDRA LIFE SPACE', '/home/tirumakudaluprop/public_html/images/logos/mahindra_logo.webp', 'https://www.mahindralifespaces.com/', 18),
('SHRI RAM PROPERTIES', '/home/tirumakudaluprop/public_html/images/logos/shriram-logo.png', 'https://www.shriramproperties.com/', 19),
('VAISHNAVI GROUP', '/home/tirumakudaluprop/public_html/images/logos/vaishnavi_logo.jpg', 'https://www.vaishnavigroup.com/', 20),
('CENTURY REAL ESTATE', '/home/tirumakudaluprop/public_html/images/logos/century-logo.png', 'https://www.centuryrealestate.in/', 21),
('L & T REALTY', '/home/tirumakudaluprop/public_html/images/logos/L&T-logo.webp', 'https://www.lntrealty.com/', 22),
('NAMBIAR BUILDERS', '/home/tirumakudaluprop/public_html/images/logos/nambiar-logo.svg', 'https://nambiarbuilders.com/', 23),
('FORTIUS INFRA', '/home/tirumakudaluprop/public_html/images/logos/fortius-logo.png', 'https://www.fortiusinfra.com/', 24),
('EMBASSY BUILDERS', '/home/tirumakudaluprop/public_html/images/logos/embassy-logo.png', 'https://www.embassyprojects.in/', 25),
('KONCEPT AMBIENCE', '/home/tirumakudaluprop/public_html/images/logos/Koncept-logo.svg', 'https://konceptambience.com/', 26),
('VALMARK', '/home/tirumakudaluprop/public_html/images/logos/valmark-logo.webp', 'https://www.valmark.in/', 27),
('SVAMITVA BUILDERS', '/home/tirumakudaluprop/public_html/images/logos/Svamitva-Logo.png', 'https://svamitva.com/', 28);




