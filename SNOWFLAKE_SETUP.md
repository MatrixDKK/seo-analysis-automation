# Snowflake Job Data Loader Setup

This guide will help you load the scraped job posting data into your Snowflake account.

## 📋 Prerequisites

1. **Snowflake Account**: You need an active Snowflake account
2. **Python Dependencies**: The required packages are already installed
3. **Snowflake Credentials**: Your username, password, and account identifier

## 🔧 Setup Instructions

### Option 1: Using Environment Variables (Recommended)

Set your Snowflake credentials as environment variables:

```bash
export SNOWFLAKE_USER="your_username"
export SNOWFLAKE_PASSWORD="your_password"
export SNOWFLAKE_ACCOUNT="your_account_identifier"
export SNOWFLAKE_WAREHOUSE="COMPUTE_WH"
export SNOWFLAKE_DATABASE="JOBPOSTINGS"
export SNOWFLAKE_SCHEMA="JOBPOSTINGS"
```

### Option 2: Using Local Config File

1. Copy the config template:
   ```bash
   cp snowflake_config.py snowflake_config_local.py
   ```

2. Edit `snowflake_config_local.py` and replace the placeholder values:
   ```python
   SNOWFLAKE_CONFIG = {
       'user': 'your_actual_username',
       'password': 'your_actual_password',
       'account': 'your_actual_account_identifier',
       'warehouse': 'COMPUTE_WH',
       'database': 'JOBPOSTINGS',
       'schema': 'JOBPOSTINGS'
   }
   ```

## 🚀 Running the Loader

Once your credentials are configured, run:

```bash
python3 snowflake_loader.py
```

## 📊 What Will Be Created

The script will create:

- **Database**: `JOBPOSTINGS`
- **Schema**: `JOBPOSTINGS`
- **Table**: `JOBPOSTINGSSCRAPED`

### Table Schema

| Column | Type | Description |
|--------|------|-------------|
| TID | VARCHAR(50) | Job ID from Jobindex |
| TITLE | VARCHAR(500) | Job title |
| COMPANY | VARCHAR(200) | Company name |
| COMPANY_ID | VARCHAR(50) | Company ID |
| LOCATION | VARCHAR(200) | Job location |
| POSTED_DATE | DATE | When job was posted |
| LAST_DATE | DATE | Application deadline |
| DESCRIPTION | TEXT | Job description |
| URL | VARCHAR(1000) | Job application URL |
| SHARE_URL | VARCHAR(1000) | Shareable URL |
| SALARY | VARCHAR(200) | Salary information |
| JOB_TYPE | VARCHAR(100) | Type of employment |
| CONTACT_PERSON | VARCHAR(200) | Contact person name |
| CONTACT_EMAIL | VARCHAR(200) | Contact email |
| IS_ARCHIVED | BOOLEAN | Whether job is archived |
| IS_LOCAL | BOOLEAN | Whether job is local |
| SCRAPED_AT | TIMESTAMP_NTZ | When data was scraped |
| LOADED_AT | TIMESTAMP_NTZ | When data was loaded to Snowflake |

## 🔍 Verifying the Data

After running the loader, you can verify the data in Snowflake:

```sql
-- Check total records
SELECT COUNT(*) FROM JOBPOSTINGS.JOBPOSTINGS.JOBPOSTINGSSCRAPED;

-- View recent job postings
SELECT TITLE, COMPANY, LOCATION, POSTED_DATE 
FROM JOBPOSTINGS.JOBPOSTINGS.JOBPOSTINGSSCRAPED 
ORDER BY POSTED_DATE DESC 
LIMIT 10;

-- Find data analyst jobs in Hovedstaden
SELECT TITLE, COMPANY, LOCATION 
FROM JOBPOSTINGS.JOBPOSTINGS.JOBPOSTINGSSCRAPED 
WHERE LOWER(LOCATION) LIKE '%københavn%' 
   OR LOWER(LOCATION) LIKE '%copenhagen%'
   OR LOWER(LOCATION) LIKE '%frederiksberg%'
   OR LOWER(LOCATION) LIKE '%hovedstaden%'
ORDER BY POSTED_DATE DESC;
```

## 🛠️ Troubleshooting

### Common Issues

1. **Connection Error**: Check your account identifier format (e.g., `xy12345.us-east-1`)
2. **Authentication Error**: Verify your username and password
3. **Warehouse Error**: Ensure your warehouse is running (`ALTER WAREHOUSE COMPUTE_WH RESUME;`)
4. **Permission Error**: Make sure your user has CREATE DATABASE and CREATE SCHEMA privileges

### Getting Your Snowflake Account Identifier

1. Log into your Snowflake account
2. Look at the URL: `https://your-account-identifier.snowflakecomputing.com`
3. The account identifier is the part before `.snowflakecomputing.com`

## 📈 Next Steps

Once the data is loaded, you can:

1. **Create Views**: For easier querying
2. **Set up Data Refresh**: Automate the loading process
3. **Build Dashboards**: Connect to BI tools like Tableau or Power BI
4. **Analyze Trends**: Query for job market insights

## 🔐 Security Notes

- Never commit your actual credentials to version control
- Use environment variables or secure credential management
- Consider using Snowflake's key pair authentication for production


