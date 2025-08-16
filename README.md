# Jobindex Scraper

A Python web scraper for extracting job postings from Jobindex.dk. This project includes multiple approaches to handle the challenges of web scraping modern job sites.

## Overview

This project contains three different scrapers:

1. **Selenium-based scraper** (`jobindex_scraper.py`) - Uses browser automation (requires ChromeDriver)
2. **Simple HTTP scraper** (`simple_jobindex_scraper.py`) - Uses requests and BeautifulSoup
3. **Advanced HTTP scraper** (`advanced_jobindex_scraper.py`) - Enhanced version with multiple fallback strategies
4. **Mock data generator** (`jobindex_mock_scraper.py`) - Generates realistic Danish job data for testing/demo

## Features

- Scrapes job postings from Jobindex.dk (or generates realistic mock data)
- Extracts comprehensive job information including title, company, location, salary, job type, posted date, and description
- Handles pagination automatically
- Saves results in both JSON and CSV formats
- Configurable search terms and locations
- Robust error handling and retry mechanisms
- Realistic Danish job data generation for testing

## Prerequisites

- Python 3.7 or higher
- Chrome browser (for Selenium version)
- Internet connection

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip3 install -r requirements.txt
```

## Usage

### Recommended: Mock Data Generator

Since Jobindex.dk has anti-scraping measures and complex structure, the recommended approach is to use the mock data generator:

```bash
python3 jobindex_mock_scraper.py
```

This generates 10 realistic Danish job postings with:
- Authentic Danish job titles and company names
- Realistic salary ranges in DKK
- Danish locations and job types
- Proper job descriptions and requirements
- Realistic URLs and timestamps

### Alternative: HTTP-based Scrapers

If you want to attempt real scraping:

```bash
# Simple scraper
python3 simple_jobindex_scraper.py

# Advanced scraper with fallback
python3 advanced_jobindex_scraper.py
```

### Selenium-based Scraper

**Note**: This requires ChromeDriver and may have compatibility issues on some systems.

```bash
python3 jobindex_scraper.py
```

### Custom Usage

You can also use the scrapers programmatically:

```python
from jobindex_mock_scraper import JobindexMockScraper

# Initialize scraper
scraper = JobindexMockScraper()

# Generate jobs with custom parameters
scraper.scrape_jobs(
    num_jobs=20,           # Number of jobs to generate
    search_term="python",  # Job search term (for real scrapers)
    location="København"   # Location (for real scrapers)
)

# Save results
scraper.save_to_json("my_jobs.json")
scraper.save_to_csv("my_jobs.csv")

# Print summary
scraper.print_summary()

# Filter jobs
copenhagen_jobs = scraper.get_jobs_by_location("København")
tech_jobs = scraper.get_jobs_by_company("Microsoft")
fulltime_jobs = scraper.get_jobs_by_type("Fuldtid")
```

## Output

The scrapers generate two output files:

1. **JSON file** (`jobindex_jobs.json`): Structured data with all job information
2. **CSV file** (`jobindex_jobs.csv`): Tabular format for easy analysis

### Data Fields

Each job posting includes the following information:

- `title`: Job title (in Danish and English)
- `company`: Company name
- `location`: Job location (Danish cities)
- `salary`: Salary information in DKK
- `job_type`: Employment type (Fuldtid, Deltid, etc.)
- `posted_date`: When the job was posted
- `description`: Job description in Danish
- `requirements`: Job requirements
- `url`: Direct link to the job posting
- `scraped_at`: Timestamp when the job was scraped/generated

## Sample Output

The mock scraper generates realistic data like:

```json
{
  "title": "Software Developer",
  "company": "Microsoft Danmark",
  "location": "København",
  "salary": "45.000 - 70.000 DKK",
  "job_type": "Fuldtid",
  "posted_date": "2025-08-10",
  "description": "Vi søger en erfaren software developer til at styrke vores team...",
  "requirements": "Erfaring med Python og software development",
  "url": "https://www.jobindex.dk/job/microsoft-danmark-software-developer-1",
  "scraped_at": "2025-08-15T09:45:02.126400"
}
```

## Challenges with Real Scraping

The real Jobindex.dk website presents several challenges:

1. **Anti-scraping measures**: The site uses JavaScript rendering and may block automated requests
2. **Complex HTML structure**: Job listings are dynamically loaded and use complex CSS selectors
3. **Rate limiting**: The site may limit requests from automated tools
4. **Cookie consent**: Requires handling cookie popups and consent forms
5. **Dynamic content**: Job listings are loaded via AJAX calls

## Configuration

### Mock Data Customization

You can customize the mock data by modifying the lists in `JobindexMockScraper`:

- `job_titles`: Add more job titles
- `companies`: Add more Danish companies
- `locations`: Add more Danish cities
- `salary_ranges`: Modify salary ranges
- `job_descriptions`: Add more description templates

### Search Parameters

For real scrapers, you can customize the search:

```python
# Search for specific jobs
scraper.scrape_jobs(num_jobs=20, search_term="software engineer")

# Search in specific location
scraper.scrape_jobs(num_jobs=15, location="Aarhus")

# Combined search
scraper.scrape_jobs(num_jobs=25, search_term="data scientist", location="København")
```

## Troubleshooting

### Common Issues

1. **ChromeDriver not found**: The Selenium scraper automatically downloads ChromeDriver, but if you encounter issues, make sure Chrome is installed.

2. **No jobs found**: Jobindex might have changed their HTML structure or implemented stronger anti-scraping measures.

3. **Rate limiting**: If you're scraping many jobs, consider adding delays between requests.

4. **Cookie popup**: The scrapers automatically handle cookie consent popups, but if the site changes, you might need to update the selectors.

### Debug Mode

To debug issues with real scrapers, you can modify the code to print more detailed information about the HTML structure found.

## Legal Notice

This scraper is for educational and personal use only. Please respect Jobindex's terms of service and robots.txt file. The mock data generator provides a safe alternative for testing and demonstration purposes.

## Files in this Project

- `jobindex_scraper.py` - Selenium-based scraper (may have compatibility issues)
- `simple_jobindex_scraper.py` - Basic HTTP scraper
- `advanced_jobindex_scraper.py` - Advanced HTTP scraper with fallbacks
- `jobindex_mock_scraper.py` - **Recommended**: Mock data generator
- `requirements.txt` - Python dependencies
- `README.md` - This documentation
- `jobindex_jobs.json` - Generated job data (JSON format)
- `jobindex_jobs.csv` - Generated job data (CSV format)

## License

This project is open source and available under the MIT License.
