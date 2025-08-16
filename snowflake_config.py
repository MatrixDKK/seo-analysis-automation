# Snowflake Configuration
# Update these values with your actual Snowflake credentials

SNOWFLAKE_CONFIG = {
    'user': 'mollerhoj',
    'password': 'Mollerhoj12344!',
    'account': 'iooooic-wm88724',
    'warehouse': 'SEO',
    'database': 'SEO_DB',
    'schema': 'SEO'
}

# Alternative: Use environment variables
# Set these environment variables instead of hardcoding credentials:
# export SNOWFLAKE_USER=your_username
# export SNOWFLAKE_PASSWORD=your_password
# export SNOWFLAKE_ACCOUNT=your_account

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


