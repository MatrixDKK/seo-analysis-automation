#!/usr/bin/env python3

import snowflake.connector
from snowflake_config import get_snowflake_config

def create_snowflake_infrastructure():
    """Create the Snowflake warehouse, database, schema, and table"""
    
    print("🏗️ Creating Snowflake infrastructure...")
    
    try:
        # Connect to Snowflake
        config = get_snowflake_config()
        conn = snowflake.connector.connect(
            user=config['user'],
            password=config['password'],
            account=config['account']
        )
        
        cursor = conn.cursor()
        
        # Create warehouse
        print("📦 Creating SEO warehouse...")
        cursor.execute("""
        CREATE WAREHOUSE IF NOT EXISTS SEO
            WAREHOUSE_SIZE = 'X-SMALL'
            WAREHOUSE_TYPE = 'STANDARD'
            AUTO_SUSPEND = 300
            AUTO_RESUME = TRUE
            COMMENT = 'Warehouse for SEO analysis and data storage'
        """)
        print("✅ SEO warehouse created successfully")
        
        # Use the SEO warehouse
        cursor.execute("USE WAREHOUSE SEO")
        
        # Create database
        print("🗄️ Creating SEO_DB database...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS SEO_DB")
        print("✅ SEO_DB database created successfully")
        
        # Use the database
        cursor.execute("USE DATABASE SEO_DB")
        
        # Create schema
        print("📁 Creating SEO schema...")
        cursor.execute("CREATE SCHEMA IF NOT EXISTS SEO")
        print("✅ SEO schema created successfully")
        
        # Use the schema
        cursor.execute("USE SCHEMA SEO")
        
        # Create table
        print("📊 Creating SEOdevoteamdatadriven table...")
        cursor.execute("""
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
        )
        """)
        print("✅ SEOdevoteamdatadriven table created successfully")
        
        # Create view
        print("👁️ Creating v_latest_seo_analysis view...")
        cursor.execute("""
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
        )
        """)
        print("✅ v_latest_seo_analysis view created successfully")
        
        # Grant permissions
        print("🔐 Setting up permissions...")
        cursor.execute("GRANT USAGE ON WAREHOUSE SEO TO ROLE PUBLIC")
        cursor.execute("GRANT USAGE ON DATABASE SEO_DB TO ROLE PUBLIC")
        cursor.execute("GRANT USAGE ON SCHEMA SEO_DB.SEO TO ROLE PUBLIC")
        cursor.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE SEO_DB.SEO.SEOdevoteamdatadriven TO ROLE PUBLIC")
        cursor.execute("GRANT SELECT ON VIEW SEO_DB.SEO.v_latest_seo_analysis TO ROLE PUBLIC")
        print("✅ Permissions set up successfully")
        
        # Insert sample data
        print("📝 Inserting sample data...")
        cursor.execute("""
        INSERT INTO SEOdevoteamdatadriven (
            page_url, page_title, google_ranking_position, search_query,
            local_seo_score, content_quality_score, technical_seo_score, user_experience_score, overall_score,
            copenhagen_mentions, denmark_mentions, danish_mentions, snowflake_keyword_count,
            contact_info_present, local_address_present, danish_phone_present,
            alt_text_coverage_percentage, cta_count, forms_count, headings_count, images_count,
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
        )
        """)
        print("✅ Sample data inserted successfully")
        
        # Verify the setup
        print("\n🔍 Verifying setup...")
        cursor.execute("SELECT COUNT(*) FROM SEOdevoteamdatadriven")
        count = cursor.fetchone()[0]
        print(f"📊 Total records in table: {count}")
        
        cursor.execute("SELECT * FROM v_latest_seo_analysis")
        latest_data = cursor.fetchall()
        print(f"📈 Latest analysis data:")
        for row in latest_data:
            print(f"   - {row[0]}: Position {row[2]}, Score {row[4]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Snowflake infrastructure created successfully!")
        print("✅ You can now run the upload script: python3 upload_seo_data.py")
        
    except Exception as e:
        print(f"❌ Error creating infrastructure: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_snowflake_infrastructure()
