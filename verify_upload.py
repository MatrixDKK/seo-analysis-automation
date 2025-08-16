#!/usr/bin/env python3

import snowflake.connector
from snowflake_config import get_snowflake_config

def verify_upload():
    """Verify the uploaded SEO data and display results"""
    
    print("🔍 Verifying uploaded SEO data...")
    print("=" * 60)
    
    try:
        # Connect to Snowflake
        config = get_snowflake_config()
        conn = snowflake.connector.connect(
            user=config['user'],
            password=config['password'],
            account=config['account'],
            warehouse=config['warehouse'],
            database=config['database'],
            schema=config['schema']
        )
        
        cursor = conn.cursor()
        
        # Get total record count
        cursor.execute("SELECT COUNT(*) FROM SEOdevoteamdatadriven")
        total_records = cursor.fetchone()[0]
        print(f"📊 Total records in table: {total_records}")
        
        # Get latest analysis
        print("\n📈 Latest SEO Analysis Results:")
        print("-" * 40)
        cursor.execute("""
        SELECT 
            page_url,
            page_title,
            google_ranking_position,
            overall_score,
            local_seo_score,
            content_quality_score,
            technical_seo_score,
            user_experience_score,
            improvement_priority
        FROM v_latest_seo_analysis
        ORDER BY overall_score DESC
        """)
        
        results = cursor.fetchall()
        for row in results:
            print(f"\n🌐 Page: {row[0]}")
            print(f"   Title: {row[1]}")
            print(f"   Google Position: {row[2] if row[2] else 'Not ranked'}")
            print(f"   Overall Score: {row[3]}/3.0")
            print(f"   Local SEO: {row[4]}/3.0")
            print(f"   Content Quality: {row[5]}/3.0")
            print(f"   Technical SEO: {row[6]}/3.0")
            print(f"   User Experience: {row[7]}/3.0")
            print(f"   Priority: {row[8]}")
        
        # Get Copenhagen-specific analysis
        print("\n🇩🇰 Copenhagen SEO Analysis:")
        print("-" * 40)
        cursor.execute("""
        SELECT 
            page_url,
            copenhagen_mentions,
            denmark_mentions,
            danish_mentions,
            local_seo_score,
            improvement_priority
        FROM SEOdevoteamdatadriven
        ORDER BY analysis_date DESC
        """)
        
        copenhagen_results = cursor.fetchall()
        for row in copenhagen_results:
            print(f"\n📄 {row[0]}")
            print(f"   Copenhagen mentions: {row[1]}")
            print(f"   Denmark mentions: {row[2]}")
            print(f"   Danish mentions: {row[3]}")
            print(f"   Local SEO score: {row[4]}/3.0")
            print(f"   Priority: {row[5]}")
        
        # Get improvement recommendations
        print("\n🎯 Key Improvement Areas:")
        print("-" * 40)
        cursor.execute("""
        SELECT 
            page_url,
            copenhagen_mentions,
            denmark_mentions,
            contact_info_present,
            local_address_present,
            danish_phone_present,
            alt_text_coverage_percentage
        FROM SEOdevoteamdatadriven
        WHERE analysis_date = (SELECT MAX(analysis_date) FROM SEOdevoteamdatadriven)
        """)
        
        improvements = cursor.fetchall()
        for row in improvements:
            print(f"\n📄 {row[0]}")
            issues = []
            if row[1] == 0:
                issues.append("❌ No Copenhagen mentions")
            if row[2] == 0:
                issues.append("❌ No Denmark mentions")
            if not row[3]:
                issues.append("❌ No contact information")
            if not row[4]:
                issues.append("❌ No local address")
            if not row[5]:
                issues.append("❌ No Danish phone numbers")
            if row[6] < 80:
                issues.append(f"⚠️ Low alt text coverage ({row[6]}%)")
            
            if issues:
                for issue in issues:
                    print(f"   {issue}")
            else:
                print("   ✅ All areas look good!")
        
        # Show historical data
        print("\n📊 Historical Data Summary:")
        print("-" * 40)
        cursor.execute("""
        SELECT 
            analysis_date,
            COUNT(*) as record_count,
            AVG(overall_score) as avg_score,
            AVG(local_seo_score) as avg_local_seo
        FROM SEOdevoteamdatadriven
        GROUP BY analysis_date
        ORDER BY analysis_date DESC
        """)
        
        history = cursor.fetchall()
        for row in history:
            print(f"📅 {row[0]}: {row[1]} records, Avg Score: {row[2]:.1f}, Avg Local SEO: {row[3]:.1f}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Data verification complete!")
        print("\n💡 Next Steps:")
        print("1. Monitor ranking changes over time")
        print("2. Track improvement progress")
        print("3. Focus on local SEO optimization")
        print("4. Add Copenhagen-specific content")
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")

if __name__ == "__main__":
    verify_upload()
