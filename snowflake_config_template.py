# Snowflake Configuration Template
# Copy this file to snowflake_config.py and fill in your actual credentials

SNOWFLAKE_CONFIG = {
    'user': 'YOUR_SNOWFLAKE_USERNAME',  # Replace with your actual username
    'password': 'YOUR_SNOWFLAKE_PASSWORD',  # Replace with your actual password
    'account': 'YOUR_SNOWFLAKE_ACCOUNT',  # Replace with your account (e.g., 'xy12345.us-east-1')
    'warehouse': 'SEO',
    'database': 'SEO_DB',
    'schema': 'SEO'
}

import os

def get_snowflake_config():
    """Get Snowflake configuration from environment variables or config"""
    return {
        'user': os.getenv('SNOWFLAKE_USER', SNOWFLAKE_CONFIG['user']),
        'password': os.getenv('SNOWFLAKE_PASSWORD', SNOWFLAKE_CONFIG['password']),
        'account': os.getenv('SNOWFLAKE_ACCOUNT', SNOWFLAKE_CONFIG['account']),
        'warehouse': SNOWFLAKE_CONFIG['warehouse'],
        'database': SNOWFLAKE_CONFIG['database'],
        'schema': SNOWFLAKE_CONFIG['schema']
    }
