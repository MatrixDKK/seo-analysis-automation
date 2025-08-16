# SEO Data Upload to Snowflake

This guide will help you upload the SEO analysis data to your Snowflake warehouse.

## 📋 Prerequisites

1. **Snowflake Account**: You need access to a Snowflake account
2. **Python Dependencies**: Install required packages
3. **Warehouse Setup**: Run the SQL script to create the warehouse and table

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
pip install snowflake-connector-python pandas
```

### 2. Configure Snowflake Connection

**Option A: Update Configuration File**
Edit `snowflake_config.py` and replace the placeholder values:
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

**Option B: Set Environment Variables**
```bash
export SNOWFLAKE_USER=your_username
export SNOWFLAKE_PASSWORD=your_password
export SNOWFLAKE_ACCOUNT=your_account
```

### 3. Create Snowflake Infrastructure
Run the SQL script in your Snowflake console:
```sql
-- Copy and paste the contents of create_seo_warehouse.sql
```

### 4. Upload Data
```bash
python3 upload_seo_data.py
```

## 📊 What Gets Uploaded

The script uploads comprehensive SEO analysis data including:

- **Page Information**: URLs, titles, Google rankings
- **SEO Scores**: Local, content, technical, and UX scores
- **Keyword Analysis**: Copenhagen, Denmark, Snowflake mentions
- **Technical Metrics**: Alt text coverage, CTA counts, load times
- **Improvement Priorities**: Specific recommendations

## 🔍 Data Structure

The `SEOdevoteamdatadriven` table contains:
- **32 fields** covering all aspects of SEO analysis
- **3 pages analyzed**: Snowflake partner page, homepage, contact page
- **Historical tracking**: Timestamps for trend analysis

## 📈 Sample Queries

After upload, you can run these queries in Snowflake:

```sql
-- Get latest analysis
SELECT * FROM v_latest_seo_analysis;

-- Track ranking changes
SELECT 
    analysis_date,
    google_ranking_position,
    overall_score
FROM SEOdevoteamdatadriven
WHERE google_ranking_position IS NOT NULL
ORDER BY analysis_date DESC;

-- Focus on local SEO issues
SELECT 
    page_url,
    copenhagen_mentions,
    local_seo_score,
    improvement_priority
FROM SEOdevoteamdatadriven
WHERE local_seo_score < 3.0;
```

## 🛠️ Troubleshooting

**Connection Issues:**
- Verify your Snowflake credentials
- Check that the warehouse, database, and schema exist
- Ensure your account has proper permissions

**Data Issues:**
- The script includes sample data from our analysis
- You can modify the `prepare_seo_data()` function to add more records
- Each upload creates new records with timestamps

## 📝 Next Steps

1. **Monitor Progress**: Run regular analysis and upload new data
2. **Track Improvements**: Compare scores over time
3. **Generate Reports**: Create dashboards from the data
4. **Automate**: Set up scheduled analysis and uploads

## 🔐 Security Notes

- Never commit credentials to version control
- Use environment variables for production
- Consider using Snowflake key pair authentication for better security
