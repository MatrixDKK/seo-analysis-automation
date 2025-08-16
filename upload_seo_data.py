#!/usr/bin/env python3

import snowflake.connector
import pandas as pd
from datetime import datetime
import json

from snowflake_config import get_snowflake_config

def connect_to_snowflake():
    """Connect to Snowflake using configuration"""
    try:
        config = get_snowflake_config()
        conn = snowflake.connector.connect(
            user=config['user'],
            password=config['password'],
            account=config['account'],
            warehouse=config['warehouse'],
            database=config['database'],
            schema=config['schema']
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        print("Please update snowflake_config.py with your credentials or set environment variables")
        return None

def prepare_seo_data():
    """Prepare the SEO analysis data for upload"""
    
    # Data from our analysis
    seo_data = [
        {
            'page_url': 'https://www.devoteam.com/snowflake-elite-partner/',
            'page_title': 'Snowflake Elite Partner: Data & AI | Devoteam',
            'google_ranking_position': 4,
            'search_query': 'snowflake consultants copenhagen',
            'local_seo_score': 2.0,
            'content_quality_score': 2.8,
            'technical_seo_score': 3.0,
            'user_experience_score': 2.5,
            'overall_score': 2.6,
            'copenhagen_mentions': 0,
            'denmark_mentions': 3,
            'danish_mentions': 2,
            'snowflake_keyword_count': 39,
            'contact_info_present': False,
            'local_address_present': False,
            'danish_phone_present': False,
            'alt_text_coverage_percentage': 25.6,
            'cta_count': 3,
            'forms_count': 2,
            'headings_count': 21,
            'images_count': 78,
            'meta_description_length': 150,
            'title_length': 45,
            'canonical_url_present': True,
            'schema_markup_count': 1,
            'structured_data_count': 1,
            'social_tags_count': 13,
            'load_time_seconds': 1.13,
            'content_size_bytes': 277554,
            'improvement_priority': 'HIGH - Local SEO optimization needed',
            'notes': 'Primary weakness: No Copenhagen-specific content or local contact information'
        },
        {
            'page_url': 'https://www.devoteam.com/',
            'page_title': 'Devoteam - AI-driven Tech Consulting',
            'google_ranking_position': None,  # Not specifically analyzed for this query
            'search_query': 'snowflake consultants copenhagen',
            'local_seo_score': 2.0,
            'content_quality_score': 2.8,
            'technical_seo_score': 3.0,
            'user_experience_score': 2.5,
            'overall_score': 2.6,
            'copenhagen_mentions': 0,
            'denmark_mentions': 2,
            'danish_mentions': 2,
            'snowflake_keyword_count': 0,
            'contact_info_present': False,
            'local_address_present': False,
            'danish_phone_present': False,
            'alt_text_coverage_percentage': 49.2,
            'cta_count': 3,
            'forms_count': 2,
            'headings_count': 11,
            'images_count': 126,
            'meta_description_length': 120,
            'title_length': 35,
            'canonical_url_present': True,
            'schema_markup_count': 0,
            'structured_data_count': 1,
            'social_tags_count': 11,
            'load_time_seconds': 0.04,
            'content_size_bytes': 323779,
            'improvement_priority': 'HIGH - Local SEO optimization needed',
            'notes': 'Homepage lacks Copenhagen-specific content and local contact information'
        },
        {
            'page_url': 'https://www.devoteam.com/contact/',
            'page_title': 'Contact Devoteam',
            'google_ranking_position': None,  # Not specifically analyzed for this query
            'search_query': 'snowflake consultants copenhagen',
            'local_seo_score': 2.0,
            'content_quality_score': 2.0,
            'technical_seo_score': 3.0,
            'user_experience_score': 2.0,
            'overall_score': 2.3,
            'copenhagen_mentions': 0,
            'denmark_mentions': 2,
            'danish_mentions': 2,
            'snowflake_keyword_count': 0,
            'contact_info_present': False,
            'local_address_present': False,
            'danish_phone_present': False,
            'alt_text_coverage_percentage': 18.2,
            'cta_count': 2,
            'forms_count': 2,
            'headings_count': 1,
            'images_count': 22,
            'meta_description_length': 80,
            'title_length': 18,
            'canonical_url_present': True,
            'schema_markup_count': 0,
            'structured_data_count': 1,
            'social_tags_count': 13,
            'load_time_seconds': 1.54,
            'content_size_bytes': 174545,
            'improvement_priority': 'HIGH - Content and local SEO improvements needed',
            'notes': 'Contact page has minimal content and lacks local contact information'
        }
    ]
    
    return seo_data

def upload_to_snowflake(conn, data):
    """Upload SEO data to Snowflake table"""
    try:
        cursor = conn.cursor()
        
        # Insert data into the table
        insert_query = """
        INSERT INTO SEOdevoteamdatadriven (
            page_url, page_title, google_ranking_position, search_query,
            local_seo_score, content_quality_score, technical_seo_score, user_experience_score, overall_score,
            copenhagen_mentions, denmark_mentions, danish_mentions, snowflake_keyword_count,
            contact_info_present, local_address_present, danish_phone_present,
            alt_text_coverage_percentage, cta_count, forms_count, headings_count, images_count,
            meta_description_length, title_length, canonical_url_present,
            schema_markup_count, structured_data_count, social_tags_count,
            load_time_seconds, content_size_bytes, improvement_priority, notes
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        for record in data:
            cursor.execute(insert_query, (
                record['page_url'],
                record['page_title'],
                record['google_ranking_position'],
                record['search_query'],
                record['local_seo_score'],
                record['content_quality_score'],
                record['technical_seo_score'],
                record['user_experience_score'],
                record['overall_score'],
                record['copenhagen_mentions'],
                record['denmark_mentions'],
                record['danish_mentions'],
                record['snowflake_keyword_count'],
                record['contact_info_present'],
                record['local_address_present'],
                record['danish_phone_present'],
                record['alt_text_coverage_percentage'],
                record['cta_count'],
                record['forms_count'],
                record['headings_count'],
                record['images_count'],
                record['meta_description_length'],
                record['title_length'],
                record['canonical_url_present'],
                record['schema_markup_count'],
                record['structured_data_count'],
                record['social_tags_count'],
                record['load_time_seconds'],
                record['content_size_bytes'],
                record['improvement_priority'],
                record['notes']
            ))
        
        conn.commit()
        print(f"✅ Successfully uploaded {len(data)} records to Snowflake")
        
        # Verify the upload
        cursor.execute("SELECT COUNT(*) FROM SEOdevoteamdatadriven")
        total_records = cursor.fetchone()[0]
        print(f"📊 Total records in table: {total_records}")
        
        # Show latest analysis
        cursor.execute("SELECT * FROM v_latest_seo_analysis")
        latest_data = cursor.fetchall()
        print(f"\n📈 Latest analysis data:")
        for row in latest_data:
            print(f"   - {row[0]}: Position {row[2]}, Score {row[4]}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error uploading data: {e}")
        conn.rollback()

def main():
    print("🚀 Starting SEO data upload to Snowflake...")
    
    # Connect to Snowflake
    conn = connect_to_snowflake()
    if not conn:
        print("❌ Failed to connect to Snowflake. Please check your credentials.")
        return
    
    # Prepare data
    seo_data = prepare_seo_data()
    print(f"📋 Prepared {len(seo_data)} records for upload")
    
    # Upload data
    upload_to_snowflake(conn, seo_data)
    
    # Close connection
    conn.close()
    print("✅ Upload process completed!")

if __name__ == "__main__":
    main()
