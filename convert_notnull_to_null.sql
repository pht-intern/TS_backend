-- ============================================
-- SQL Script to Convert NOT NULL Values to NULL
-- Based on doccuments/database.sql schema
-- ============================================
-- This script contains:
-- 1. ALTER TABLE statements to modify columns from NOT NULL to NULL
-- 2. UPDATE statements to set all existing values to NULL
-- All UPDATE queries use WHERE id > 0 to satisfy MySQL safe update mode
-- ============================================

-- ============================================
-- RESIDENTIAL PROPERTIES TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE residential_properties 
    MODIFY COLUMN city VARCHAR(250) NULL,
    MODIFY COLUMN locality VARCHAR(250) NULL,
    MODIFY COLUMN property_name VARCHAR(250) NULL,
    MODIFY COLUMN unit_type VARCHAR(50) NULL,
    MODIFY COLUMN bedrooms INT NULL,
    MODIFY COLUMN buildup_area DECIMAL(10, 2) NULL,
    MODIFY COLUMN carpet_area DECIMAL(10, 2) NULL,
    MODIFY COLUMN price DECIMAL(12, 2) NULL,
    MODIFY COLUMN type VARCHAR(50) NULL,
    MODIFY COLUMN status VARCHAR(20) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE residential_properties 
SET 
    city = NULL,
    locality = NULL,
    property_name = NULL,
    unit_type = NULL,
    bedrooms = NULL,
    buildup_area = NULL,
    carpet_area = NULL,
    price = NULL,
    type = NULL,
    status = NULL
WHERE id > 0;

-- ============================================
-- PLOT PROPERTIES TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE plot_properties 
    MODIFY COLUMN city VARCHAR(250) NULL,
    MODIFY COLUMN locality VARCHAR(250) NULL,
    MODIFY COLUMN project_name VARCHAR(250) NULL,
    MODIFY COLUMN plot_area DECIMAL(10, 2) NULL,
    MODIFY COLUMN plot_length DECIMAL(10, 2) NULL,
    MODIFY COLUMN plot_breadth DECIMAL(10, 2) NULL,
    MODIFY COLUMN price DECIMAL(12, 2) NULL,
    MODIFY COLUMN status VARCHAR(20) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE plot_properties 
SET 
    city = NULL,
    locality = NULL,
    project_name = NULL,
    plot_area = NULL,
    plot_length = NULL,
    plot_breadth = NULL,
    price = NULL,
    status = NULL
WHERE id > 0;

-- ============================================
-- PROPERTY FEATURES TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE property_features 
    MODIFY COLUMN property_category VARCHAR(50) NULL,
    MODIFY COLUMN property_id INT NULL,
    MODIFY COLUMN feature_name VARCHAR(100) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE property_features 
SET 
    property_category = NULL,
    property_id = NULL,
    feature_name = NULL
WHERE id > 0;

-- ============================================
-- RESIDENTIAL PROPERTY IMAGES TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE residential_property_images 
    MODIFY COLUMN property_id INT NULL,
    MODIFY COLUMN image_url TEXT NULL,
    MODIFY COLUMN image_category VARCHAR(50) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE residential_property_images 
SET 
    property_id = NULL,
    image_url = NULL,
    image_category = NULL
WHERE id > 0;

-- ============================================
-- PLOT PROPERTY IMAGES TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE plot_property_images 
    MODIFY COLUMN property_id INT NULL,
    MODIFY COLUMN image_url TEXT NULL,
    MODIFY COLUMN image_category VARCHAR(50) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE plot_property_images 
SET 
    property_id = NULL,
    image_url = NULL,
    image_category = NULL
WHERE id > 0;

-- ============================================
-- PARTNERS TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE partners 
    MODIFY COLUMN name VARCHAR(250) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE partners 
SET name = NULL
WHERE id > 0;

-- ============================================
-- TESTIMONIALS TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE testimonials 
    MODIFY COLUMN client_name VARCHAR(250) NULL,
    MODIFY COLUMN message TEXT NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE testimonials 
SET 
    client_name = NULL,
    message = NULL
WHERE id > 0;

-- ============================================
-- CONTACT INQUIRIES TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE contact_inquiries 
    MODIFY COLUMN name VARCHAR(250) NULL,
    MODIFY COLUMN email VARCHAR(250) NULL,
    MODIFY COLUMN message TEXT NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE contact_inquiries 
SET 
    name = NULL,
    email = NULL,
    message = NULL
WHERE id > 0;

-- ============================================
-- USERS TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE users 
    MODIFY COLUMN email VARCHAR(255) NULL,
    MODIFY COLUMN password_hash VARCHAR(255) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE users 
SET 
    email = NULL,
    password_hash = NULL
WHERE id > 0;

-- ============================================
-- VISITOR INFO TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE visitor_info 
    MODIFY COLUMN full_name VARCHAR(255) NULL,
    MODIFY COLUMN email VARCHAR(255) NULL,
    MODIFY COLUMN phone VARCHAR(20) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE visitor_info 
SET 
    full_name = NULL,
    email = NULL,
    phone = NULL
WHERE id > 0;

-- ============================================
-- LOGS TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE logs 
    MODIFY COLUMN log_type VARCHAR(50) NULL,
    MODIFY COLUMN action VARCHAR(100) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE logs 
SET 
    log_type = NULL,
    action = NULL
WHERE id > 0;

-- ============================================
-- APP METRICS PASSWORD TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE app_metrics_password 
    MODIFY COLUMN password_hash VARCHAR(255) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE app_metrics_password 
SET password_hash = NULL
WHERE id > 0;

-- ============================================
-- SYSTEM METRICS TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE system_metrics 
    MODIFY COLUMN cpu_usage DECIMAL(5, 2) NULL,
    MODIFY COLUMN ram_usage DECIMAL(5, 2) NULL,
    MODIFY COLUMN ram_used_mb DECIMAL(10, 2) NULL,
    MODIFY COLUMN ram_total_mb DECIMAL(10, 2) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE system_metrics 
SET 
    cpu_usage = NULL,
    ram_usage = NULL,
    ram_used_mb = NULL,
    ram_total_mb = NULL
WHERE id > 0;

-- ============================================
-- TEMPORARY METRICS TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE temporary_metrics 
    MODIFY COLUMN cpu_usage DECIMAL(5, 2) NULL,
    MODIFY COLUMN ram_usage DECIMAL(5, 2) NULL,
    MODIFY COLUMN ram_used_mb DECIMAL(10, 2) NULL,
    MODIFY COLUMN ram_total_mb DECIMAL(10, 2) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE temporary_metrics 
SET 
    cpu_usage = NULL,
    ram_usage = NULL,
    ram_used_mb = NULL,
    ram_total_mb = NULL
WHERE id > 0;

-- ============================================
-- APPLICATION METRICS TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE application_metrics 
    MODIFY COLUMN endpoint VARCHAR(255) NULL,
    MODIFY COLUMN method VARCHAR(10) NULL,
    MODIFY COLUMN response_time_ms DECIMAL(10, 2) NULL,
    MODIFY COLUMN status_code INT NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE application_metrics 
SET 
    endpoint = NULL,
    method = NULL,
    response_time_ms = NULL,
    status_code = NULL
WHERE id > 0;

-- ============================================
-- APPLICATION METRICS FRONTEND TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE application_metrics_frontend 
    MODIFY COLUMN cpu_usage DECIMAL(5, 2) NULL,
    MODIFY COLUMN ram_usage DECIMAL(5, 2) NULL,
    MODIFY COLUMN ram_used_mb DECIMAL(10, 2) NULL,
    MODIFY COLUMN ram_total_mb DECIMAL(10, 2) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE application_metrics_frontend 
SET 
    cpu_usage = NULL,
    ram_usage = NULL,
    ram_used_mb = NULL,
    ram_total_mb = NULL
WHERE id > 0;

-- ============================================
-- BLOGS TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE blogs 
    MODIFY COLUMN title VARCHAR(250) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE blogs 
SET title = NULL
WHERE id > 0;

-- ============================================
-- SCHEDULED VISITS TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE scheduled_visits 
    MODIFY COLUMN visitor_name VARCHAR(250) NULL,
    MODIFY COLUMN visitor_email VARCHAR(250) NULL,
    MODIFY COLUMN visitor_phone VARCHAR(20) NULL,
    MODIFY COLUMN visit_date DATE NULL,
    MODIFY COLUMN visit_time TIME NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE scheduled_visits 
SET 
    visitor_name = NULL,
    visitor_email = NULL,
    visitor_phone = NULL,
    visit_date = NULL,
    visit_time = NULL
WHERE id > 0;

-- ============================================
-- CITIES TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE cities 
    MODIFY COLUMN name VARCHAR(250) NULL,
    MODIFY COLUMN state VARCHAR(250) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE cities 
SET 
    name = NULL,
    state = NULL
WHERE id > 0;

-- ============================================
-- CATEGORIES TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE categories 
    MODIFY COLUMN name VARCHAR(100) NULL,
    MODIFY COLUMN display_name VARCHAR(250) NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE categories 
SET 
    name = NULL,
    display_name = NULL
WHERE id > 0;

-- ============================================
-- UNIT TYPES TABLE
-- ============================================

-- Step 1: Alter table to allow NULL values
ALTER TABLE unit_types 
    MODIFY COLUMN name VARCHAR(50) NULL,
    MODIFY COLUMN display_name VARCHAR(250) NULL,
    MODIFY COLUMN bedrooms INT NULL;

-- Step 2: Update all non-null values to NULL (using PRIMARY KEY in WHERE)
UPDATE unit_types 
SET 
    name = NULL,
    display_name = NULL,
    bedrooms = NULL
WHERE id > 0;
