#!/usr/bin/env python3

import snowflake.connector
import sys

def test_connection():
    """Test Snowflake connection"""
    print("🔍 Testing Snowflake connection...")
    
    try:
        # Try to import the config
        from snowflake_config import get_snowflake_config
        config = get_snowflake_config()
        
        # Check if credentials are still placeholder values
        if 'YOUR_SNOWFLAKE_USERNAME' in config['user'] or 'YOUR_SNOWFLAKE_PASSWORD' in config['password']:
            print("❌ Please update snowflake_config.py with your actual credentials")
            print("   Copy snowflake_config_template.py to snowflake_config.py and fill in your details")
            return False
        
        print(f"📋 Connecting to account: {config['account']}")
        print(f"👤 User: {config['user']}")
        print(f"🏢 Warehouse: {config['warehouse']}")
        print(f"🗄️ Database: {config['database']}")
        print(f"📁 Schema: {config['schema']}")
        
        # Attempt connection
        conn = snowflake.connector.connect(
            user=config['user'],
            password=config['password'],
            account=config['account'],
            warehouse=config['warehouse'],
            database=config['database'],
            schema=config['schema']
        )
        
        print("✅ Successfully connected to Snowflake!")
        
        # Test basic query
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()[0]
        print(f"❄️ Snowflake version: {version}")
        
        # Test if warehouse exists
        cursor.execute("SHOW WAREHOUSES LIKE 'SEO'")
        warehouses = cursor.fetchall()
        if warehouses:
            print("✅ SEO warehouse found")
        else:
            print("⚠️ SEO warehouse not found - you may need to run the SQL script first")
        
        # Test if database exists
        cursor.execute("SHOW DATABASES LIKE 'SEO_DB'")
        databases = cursor.fetchall()
        if databases:
            print("✅ SEO_DB database found")
        else:
            print("⚠️ SEO_DB database not found - you may need to run the SQL script first")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Connection test successful! You can now run the upload script.")
        return True
        
    except ImportError:
        print("❌ snowflake_config.py not found")
        print("   Please copy snowflake_config_template.py to snowflake_config.py and update with your credentials")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("   1. Check your Snowflake credentials")
        print("   2. Verify your account identifier format (e.g., 'xy12345.us-east-1')")
        print("   3. Ensure your user has proper permissions")
        print("   4. Check if your Snowflake account is accessible")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
