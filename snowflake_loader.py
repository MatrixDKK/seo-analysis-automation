import snowflake.connector
import pandas as pd
import os
from datetime import datetime
import json

class SnowflakeJobLoader:
    def __init__(self):
        """Initialize Snowflake connection using credentials from get_players.py"""
        # Use the credentials found in get_players.py
        self.conn = snowflake.connector.connect(
            user='mollerhoj',
            password='Mollerhoj12344!',
            account='iooooic-wm88724',
            warehouse='COMPUTE_WH',
            database='JOBPOSTINGS',  # We'll create this new database
            schema='JOBPOSTINGS'     # We'll create this new schema
        )
        self.cursor = self.conn.cursor()
        print("✅ Connected to Snowflake using credentials from get_players.py")
        
    def create_database_and_schema(self):
        """Create database and schema if they don't exist"""
        try:
            # Create database
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS JOBPOSTINGS")
            print("✅ Database JOBPOSTINGS created/verified")
            
            # Use the database
            self.cursor.execute("USE DATABASE JOBPOSTINGS")
            
            # Create schema
            self.cursor.execute("CREATE SCHEMA IF NOT EXISTS JOBPOSTINGS")
            print("✅ Schema JOBPOSTINGS created/verified")
            
            # Use the schema
            self.cursor.execute("USE SCHEMA JOBPOSTINGS")
            
        except Exception as e:
            print(f"❌ Error creating database/schema: {e}")
            raise
    
    def recreate_table_with_new_order(self):
        """Drop and recreate the table with the new column order"""
        try:
            # Drop existing table
            self.cursor.execute("DROP TABLE IF EXISTS JOBPOSTINGSSCRAPED")
            print("✅ Dropped existing table")
            
            # Create table with new column order
            self.create_table()
            
        except Exception as e:
            print(f"❌ Error recreating table: {e}")
            raise

    def create_table(self):
        """Create the jobpostingscraped table"""
        try:
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS JOBPOSTINGSSCRAPED (
                TID VARCHAR(50),
                TITLE VARCHAR(500),
                COMPANY VARCHAR(200),
                COMPANY_ID VARCHAR(50),
                CONTACT_EMAIL VARCHAR(200),
                CONTACT_PERSON VARCHAR(200),
                LOCATION VARCHAR(200),
                POSTED_DATE DATE,
                LAST_DATE DATE,
                DESCRIPTION TEXT,
                URL VARCHAR(1000),
                SHARE_URL VARCHAR(1000),
                SALARY VARCHAR(200),
                JOB_TYPE VARCHAR(100),
                IS_ARCHIVED BOOLEAN,
                IS_LOCAL BOOLEAN,
                SCRAPED_AT TIMESTAMP_NTZ,
                LOADED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            )
            """
            self.cursor.execute(create_table_sql)
            print("✅ Table JOBPOSTINGSSCRAPED created/verified")
            
        except Exception as e:
            print(f"❌ Error creating table: {e}")
            raise
    
    def load_data_from_csv(self, csv_file_path):
        """Load data from CSV file into Snowflake"""
        try:
            # Read CSV file
            df = pd.read_csv(csv_file_path)
            print(f"📊 Loaded {len(df)} records from CSV")
            
            # Convert date columns - handle both string and datetime formats
            try:
                df['posted_date'] = pd.to_datetime(df['posted_date'], errors='coerce').dt.date
            except:
                df['posted_date'] = None
                
            try:
                df['last_date'] = pd.to_datetime(df['last_date'], errors='coerce').dt.date
            except:
                df['last_date'] = None
                
            try:
                df['scraped_at'] = pd.to_datetime(df['scraped_at'], errors='coerce')
            except:
                df['scraped_at'] = None
            
            # Convert boolean columns
            df['is_archived'] = df['is_archived'].map({'True': True, 'False': False, True: True, False: False})
            df['is_local'] = df['is_local'].map({'True': True, 'False': False, True: True, False: False})
            
            # Replace NaN values with None
            df = df.replace({pd.NA: None, pd.NaT: None})
            df = df.where(pd.notnull(df), None)
            
            # Prepare data for insertion
            records = []
            for _, row in df.iterrows():
                # Convert timestamp to string if it exists
                scraped_at = row.get('scraped_at')
                if scraped_at is not None and pd.notna(scraped_at):
                    scraped_at = scraped_at.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    scraped_at = None
                
                # Handle NaN values in each field
                def clean_value(val):
                    if pd.isna(val) or val == 'nan' or val == 'NAN':
                        return None
                    return val
                
                record = (
                    clean_value(row.get('tid', '')),
                    clean_value(row.get('title', '')),
                    clean_value(row.get('company', '')),
                    clean_value(row.get('company_id', '')),
                    clean_value(row.get('contact_email', '')),
                    clean_value(row.get('contact_person', '')),
                    clean_value(row.get('location', '')),
                    clean_value(row.get('posted_date')),
                    clean_value(row.get('last_date')),
                    clean_value(row.get('description', '')),
                    clean_value(row.get('url', '')),
                    clean_value(row.get('share_url', '')),
                    clean_value(row.get('salary', '')),
                    clean_value(row.get('job_type', '')),
                    clean_value(row.get('is_archived')),
                    clean_value(row.get('is_local')),
                    scraped_at
                )
                records.append(record)
            
            # Insert data
            insert_sql = """
            INSERT INTO JOBPOSTINGSSCRAPED (
                TID, TITLE, COMPANY, COMPANY_ID, CONTACT_EMAIL, CONTACT_PERSON, LOCATION, POSTED_DATE, LAST_DATE,
                DESCRIPTION, URL, SHARE_URL, SALARY, JOB_TYPE, IS_ARCHIVED, IS_LOCAL, SCRAPED_AT
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(insert_sql, records)
            self.conn.commit()
            
            print(f"✅ Successfully loaded {len(records)} records into Snowflake")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def verify_data(self):
        """Verify the data was loaded correctly"""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM JOBPOSTINGSSCRAPED")
            count = self.cursor.fetchone()[0]
            print(f"📊 Total records in table: {count}")
            
            self.cursor.execute("""
                SELECT TITLE, COMPANY, LOCATION, POSTED_DATE 
                FROM JOBPOSTINGSSCRAPED 
                ORDER BY POSTED_DATE DESC 
                LIMIT 5
            """)
            
            print("\n📋 Sample records:")
            for row in self.cursor.fetchall():
                print(f"  - {row[0]} at {row[1]} ({row[2]}) - Posted: {row[3]}")
                
        except Exception as e:
            print(f"❌ Error verifying data: {e}")
            raise
    
    def close(self):
        """Close the connection"""
        self.cursor.close()
        self.conn.close()
        print("🔒 Snowflake connection closed")

def main():
    """Main function to load job data into Snowflake"""
    print("🚀 Starting Snowflake Job Data Loader...")
    
    # Check if CSV file exists
    csv_file = "final_jobindex_jobs.csv"
    if not os.path.exists(csv_file):
        print(f"❌ CSV file {csv_file} not found!")
        return
    
    # Initialize loader
    loader = SnowflakeJobLoader()
    
    try:
        # Create database and schema
        loader.create_database_and_schema()
        
        # Recreate table with new column order
        loader.recreate_table_with_new_order()
        
        # Load data
        loader.load_data_from_csv(csv_file)
        
        # Verify data
        loader.verify_data()
        
        print("\n🎉 Job data successfully loaded into Snowflake!")
        print("📍 Database: JOBPOSTINGS")
        print("📍 Schema: JOBPOSTINGS") 
        print("📍 Table: JOBPOSTINGSSCRAPED")
        print("📋 Column order: TID, TITLE, COMPANY, COMPANY_ID, CONTACT_EMAIL, CONTACT_PERSON, LOCATION, ...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        loader.close()

if __name__ == "__main__":
    main()
