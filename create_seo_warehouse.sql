-- Create SEO Warehouse
CREATE WAREHOUSE IF NOT EXISTS SEO
    WAREHOUSE_SIZE = 'X-SMALL'
    WAREHOUSE_TYPE = 'STANDARD'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 1
    SCALING_POLICY = 'STANDARD'
    COMMENT = 'Warehouse for SEO analysis and data storage';

-- Use the SEO warehouse
USE WAREHOUSE SEO;

-- Create SEO database (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS SEO_DB;

-- Use the SEO database
USE DATABASE SEO_DB;

-- Create SEO schema
CREATE SCHEMA IF NOT EXISTS SEO;

-- Use the SEO schema
USE SCHEMA SEO;

-- Create SEOdevoteamdatadriven table
CREATE TABLE IF NOT EXISTS SEOdevoteamdatadriven (
    id NUMBER AUTOINCREMENT PRIMARY KEY,
    analysis_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    page_url STRING,
    page_title STRING,
    google_ranking_position NUMBER,
    search_query STRING,
    local_seo_score NUMBER(3,1),
    content_quality_score NUMBER(3,1),
    technical_seo_score NUMBER(3,1),
    user_experience_score NUMBER(3,1),
    overall_score NUMBER(3,1),
    copenhagen_mentions NUMBER,
    denmark_mentions NUMBER,
    danish_mentions NUMBER,
    snowflake_keyword_count NUMBER,
    contact_info_present BOOLEAN,
    local_address_present BOOLEAN,
    danish_phone_present BOOLEAN,
    alt_text_coverage_percentage NUMBER(5,2),
    cta_count NUMBER,
    forms_count NUMBER,
    headings_count NUMBER,
    images_count NUMBER,
    meta_description_length NUMBER,
    title_length NUMBER,
    canonical_url_present BOOLEAN,
    schema_markup_count NUMBER,
    structured_data_count NUMBER,
    social_tags_count NUMBER,
    load_time_seconds NUMBER(5,3),
    content_size_bytes NUMBER,
    improvement_priority STRING,
    notes STRING,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Create a view for easy access to the latest analysis
CREATE OR REPLACE VIEW v_latest_seo_analysis AS
SELECT 
    page_url,
    page_title,
    google_ranking_position,
    search_query,
    overall_score,
    local_seo_score,
    content_quality_score,
    technical_seo_score,
    user_experience_score,
    analysis_date,
    improvement_priority
FROM SEOdevoteamdatadriven
WHERE analysis_date = (
    SELECT MAX(analysis_date) 
    FROM SEOdevoteamdatadriven
);

-- Grant necessary permissions (adjust as needed)
GRANT USAGE ON WAREHOUSE SEO TO ROLE PUBLIC;
GRANT USAGE ON DATABASE SEO_DB TO ROLE PUBLIC;
GRANT USAGE ON SCHEMA SEO_DB.SEO TO ROLE PUBLIC;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE SEO_DB.SEO.SEOdevoteamdatadriven TO ROLE PUBLIC;
GRANT SELECT ON VIEW SEO_DB.SEO.v_latest_seo_analysis TO ROLE PUBLIC;

-- Insert sample data for testing
INSERT INTO SEOdevoteamdatadriven (
    page_url,
    page_title,
    google_ranking_position,
    search_query,
    local_seo_score,
    content_quality_score,
    technical_seo_score,
    user_experience_score,
    overall_score,
    copenhagen_mentions,
    denmark_mentions,
    danish_mentions,
    snowflake_keyword_count,
    contact_info_present,
    local_address_present,
    danish_phone_present,
    alt_text_coverage_percentage,
    cta_count,
    forms_count,
    headings_count,
    images_count,
    improvement_priority
) VALUES (
    'https://www.devoteam.com/snowflake-elite-partner/',
    'Snowflake Elite Partner: Data & AI | Devoteam',
    4,
    'snowflake consultants copenhagen',
    2.0,
    2.8,
    3.0,
    2.5,
    2.6,
    0,
    3,
    2,
    39,
    FALSE,
    FALSE,
    FALSE,
    25.6,
    3,
    2,
    21,
    78,
    'HIGH - Local SEO optimization needed'
);

-- Show the created table structure
DESCRIBE TABLE SEOdevoteamdatadriven;

-- Show sample data
SELECT * FROM v_latest_seo_analysis;
