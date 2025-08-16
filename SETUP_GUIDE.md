# 🚀 Complete SEO Data Upload Setup Guide

This guide will walk you through the entire process of uploading SEO analysis data to Snowflake.

## 📋 Prerequisites Checklist

- [ ] Snowflake account access
- [ ] Python 3.7+ installed
- [ ] Required packages installed (`snowflake-connector-python`, `pandas`)

## 🔧 Step-by-Step Setup

### Step 1: Configure Snowflake Connection

**Option A: Using Configuration File (Recommended)**

1. Copy the template file:
   ```bash
   cp snowflake_config_template.py snowflake_config.py
   ```

2. Edit `snowflake_config.py` and replace the placeholder values:
   ```python
   SNOWFLAKE_CONFIG = {
       'user': 'your_actual_username',
       'password': 'your_actual_password',
       'account': 'your_actual_account',  # e.g., 'xy12345.us-east-1'
       'warehouse': 'SEO',
       'database': 'SEO_DB',
       'schema': 'SEO'
   }
   ```

**Option B: Using Environment Variables**

```bash
export SNOWFLAKE_USER=your_username
export SNOWFLAKE_PASSWORD=your_password
export SNOWFLAKE_ACCOUNT=your_account
```

### Step 2: Test Connection

Run the connection test:
```bash
python3 test_snowflake_connection.py
```

**Expected Output:**
```
🔍 Testing Snowflake connection...
📋 Connecting to account: your_account
👤 User: your_username
🏢 Warehouse: SEO
🗄️ Database: SEO_DB
📁 Schema: SEO
✅ Successfully connected to Snowflake!
❄️ Snowflake version: 8.5.2
✅ SEO warehouse found
✅ SEO_DB database found
🎉 Connection test successful!
```

### Step 3: Create Snowflake Infrastructure

1. Open your Snowflake web console
2. Navigate to the SQL worksheet
3. Copy and paste the entire contents of `create_seo_warehouse.sql`
4. Execute the script

**Expected Output:**
- Warehouse 'SEO' created
- Database 'SEO_DB' created
- Schema 'SEO' created
- Table 'SEOdevoteamdatadriven' created
- View 'v_latest_seo_analysis' created
- Sample data inserted

### Step 4: Upload SEO Data

Run the upload script:
```bash
python3 upload_seo_data.py
```

**Expected Output:**
```
🚀 Starting SEO data upload to Snowflake...
📋 Prepared 3 records for upload
✅ Successfully uploaded 3 records to Snowflake
📊 Total records in table: 4
📈 Latest analysis data:
   - https://www.devoteam.com/snowflake-elite-partner/: Position 4, Score 2.6
   - https://www.devoteam.com/: Position None, Score 2.6
   - https://www.devoteam.com/contact/: Position None, Score 2.3
✅ Upload process completed!
```

## 📊 Verify the Upload

### Query 1: Check Latest Analysis
```sql
SELECT * FROM v_latest_seo_analysis;
```

### Query 2: View All Data
```sql
SELECT 
    page_url,
    google_ranking_position,
    overall_score,
    local_seo_score,
    improvement_priority
FROM SEOdevoteamdatadriven
ORDER BY analysis_date DESC;
```

### Query 3: Focus on Local SEO Issues
```sql
SELECT 
    page_url,
    copenhagen_mentions,
    denmark_mentions,
    local_seo_score,
    improvement_priority
FROM SEOdevoteamdatadriven
WHERE local_seo_score < 3.0;
```

## 🛠️ Troubleshooting

### Connection Issues

**Error: "Invalid credentials"**
- Double-check username and password
- Verify account identifier format
- Ensure user has proper permissions

**Error: "Warehouse not found"**
- Run the SQL script first to create the warehouse
- Check warehouse name spelling

**Error: "Database not found"**
- Run the SQL script first to create the database
- Verify database name

### Data Upload Issues

**Error: "Table not found"**
- Ensure the SQL script was executed completely
- Check table name spelling

**Error: "Permission denied"**
- Verify user has INSERT permissions on the table
- Check role assignments

## 📈 Next Steps

1. **Monitor Progress**: Run regular analysis and upload new data
2. **Track Improvements**: Compare scores over time
3. **Generate Reports**: Create dashboards from the data
4. **Automate**: Set up scheduled analysis and uploads

## 🔐 Security Best Practices

- Never commit credentials to version control
- Use environment variables in production
- Consider using Snowflake key pair authentication
- Regularly rotate passwords

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your Snowflake account status
3. Ensure all prerequisites are met
4. Test the connection before uploading data
