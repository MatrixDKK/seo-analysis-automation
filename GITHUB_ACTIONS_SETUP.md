# 🚀 GitHub Actions Setup for Daily SEO Analysis

This guide will help you set up automated daily SEO analysis that runs in the cloud, even when your computer is off.

## 📋 Prerequisites

1. **GitHub Account** (free)
2. **Git repository** for your project
3. **Snowflake credentials** (already configured)

## 🔧 Step-by-Step Setup

### Step 1: Initialize Git Repository (if not already done)

```bash
# Navigate to your project directory
cd /Users/rasmustheilmollerhoj/snowflake_api_loader/jobstuff

# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: SEO analysis automation setup"

# Add your GitHub repository as remote (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

### Step 2: Set Up GitHub Secrets

1. **Go to your GitHub repository**
2. **Navigate to Settings → Secrets and variables → Actions**
3. **Click "New repository secret"**
4. **Add these three secrets:**

   **Secret Name**: `SNOWFLAKE_USER`
   **Secret Value**: `mollerhoj`

   **Secret Name**: `SNOWFLAKE_PASSWORD`
   **Secret Value**: `Mollerhoj12344!`

   **Secret Name**: `SNOWFLAKE_ACCOUNT`
   **Secret Value**: `iooooic-wm88724`

### Step 3: Verify Files Are in Place

Make sure these files are in your repository:
- ✅ `.github/workflows/daily_seo_analysis.yml`
- ✅ `daily_seo_analysis.py`
- ✅ `snowflake_config.py`

### Step 4: Test the Workflow

1. **Go to your GitHub repository**
2. **Click on "Actions" tab**
3. **You should see "Daily SEO Analysis" workflow**
4. **Click on it and then "Run workflow"**
5. **Select the branch (usually "main") and click "Run workflow"**

## ⏰ Schedule Configuration

The workflow is currently set to run **daily at 9:00 AM UTC**. To change the schedule:

### Edit the cron schedule in `.github/workflows/daily_seo_analysis.yml`:

```yaml
on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9:00 AM UTC
```

### Common Schedule Examples:

```yaml
# Daily at 6:00 AM UTC
- cron: '0 6 * * *'

# Every Monday at 9:00 AM UTC
- cron: '0 9 * * 1'

# Every 6 hours
- cron: '0 */6 * * *'

# Weekdays only at 8:00 AM UTC
- cron: '0 8 * * 1-5'
```

### Timezone Conversion:
- **UTC 9:00 AM** = **CET 10:00 AM** (winter) / **CEST 11:00 AM** (summer)
- **UTC 6:00 AM** = **CET 7:00 AM** (winter) / **CEST 8:00 AM** (summer)

## 📊 Monitoring and Results

### View Results:

1. **GitHub Actions Tab**: See workflow runs and logs
2. **Artifacts**: Download analysis results
3. **Snowflake**: Check the `SEOdevoteamdatadriven` table

### Check Snowflake Data:

```sql
-- View latest analysis
SELECT * FROM v_latest_seo_analysis;

-- Track ranking changes over time
SELECT 
    analysis_date,
    page_url,
    google_ranking_position,
    overall_score,
    local_seo_score
FROM SEOdevoteamdatadriven
WHERE google_ranking_position IS NOT NULL
ORDER BY analysis_date DESC;
```

## 🔍 Troubleshooting

### Common Issues:

**1. Workflow fails with "Module not found"**
- ✅ Solution: All required packages are installed in the workflow

**2. Snowflake connection fails**
- ✅ Check that GitHub secrets are set correctly
- ✅ Verify Snowflake credentials are valid

**3. Workflow doesn't run automatically**
- ✅ Check the cron schedule
- ✅ Ensure the repository is public or you have GitHub Pro for private repos

**4. Analysis fails for some pages**
- ✅ The script includes error handling and will continue with other pages
- ✅ Check logs in GitHub Actions for specific errors

### Manual Testing:

You can test the script locally before pushing:

```bash
# Test the analysis script locally
python3 daily_seo_analysis.py

# Check the generated files
ls -la seo_analysis_results.json daily_analysis_log.txt
```

## 📈 What Gets Analyzed Daily

### 1. **Google Ranking Check**
- Search query: "snowflake consultants copenhagen"
- Tracks Devoteam's position in search results

### 2. **Page Analysis** (3 pages)
- https://www.devoteam.com/snowflake-elite-partner/
- https://www.devoteam.com/
- https://www.devoteam.com/contact/

### 3. **SEO Metrics Tracked**
- Local SEO (Copenhagen mentions, contact info)
- Content quality (word count, headings, keywords)
- Technical SEO (meta tags, schema, canonical URLs)
- User experience (alt text, CTAs, forms)
- Performance (load time, content size)

### 4. **Data Stored in Snowflake**
- All analysis results with timestamps
- Historical tracking for trend analysis
- Improvement priorities and notes

## 🎯 Benefits of This Setup

### ✅ **Always Running**
- Works even when your computer is off
- No need to keep your machine running

### ✅ **Free Cloud Computing**
- GitHub Actions provides 2,000 minutes/month free
- Perfect for daily analysis tasks

### ✅ **Automatic Data Collection**
- Consistent daily data collection
- Historical tracking for trends

### ✅ **Easy Monitoring**
- GitHub Actions dashboard shows run status
- Email notifications for failures (optional)

### ✅ **Scalable**
- Easy to add more pages or analysis metrics
- Can be extended for other SEO tasks

## 🔄 Updating the Analysis

### To Add More Pages:
Edit `daily_seo_analysis.py` and add URLs to the `pages_to_analyze` list:

```python
pages_to_analyze = [
    "https://www.devoteam.com/snowflake-elite-partner/",
    "https://www.devoteam.com/",
    "https://www.devoteam.com/contact/",
    "https://www.devoteam.com/services/",  # Add new pages here
    "https://www.devoteam.com/about/"
]
```

### To Change Analysis Frequency:
Edit the cron schedule in `.github/workflows/daily_seo_analysis.yml`

### To Add New Metrics:
Modify the `analyze_page_seo()` method in `daily_seo_analysis.py`

## 📞 Support

If you encounter issues:

1. **Check GitHub Actions logs** for detailed error messages
2. **Verify GitHub secrets** are set correctly
3. **Test locally** first with `python3 daily_seo_analysis.py`
4. **Check Snowflake connection** with `python3 test_snowflake_connection.py`

---

**🎉 Once set up, your SEO analysis will run automatically every day, providing consistent data for tracking Devoteam's SEO improvements!**
