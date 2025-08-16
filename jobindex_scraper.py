#!/usr/bin/env python3
"""
Jobindex Scraper
Scrapes job postings from Jobindex.dk
"""

import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
from datetime import datetime


class JobindexScraper:
    def __init__(self, headless=True):
        """Initialize the scraper with Chrome WebDriver"""
        self.base_url = "https://www.jobindex.dk"
        self.jobs = []
        
        # Setup Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Initialize WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def scrape_jobs(self, num_jobs=10, search_term="", location=""):
        """
        Scrape job postings from Jobindex
        
        Args:
            num_jobs (int): Number of jobs to scrape
            search_term (str): Job search term
            location (str): Location to search in
        """
        try:
            # Construct search URL
            search_url = f"{self.base_url}/jobsoegning"
            if search_term:
                search_url += f"?q={search_term}"
            if location:
                search_url += f"&location={location}"
            
            print(f"Searching for jobs at: {search_url}")
            self.driver.get(search_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Accept cookies if popup appears
            try:
                cookie_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accepter alle') or contains(text(), 'Accept all')]"))
                )
                cookie_button.click()
                time.sleep(2)
            except:
                print("No cookie popup found or already accepted")
            
            jobs_scraped = 0
            page = 1
            
            while jobs_scraped < num_jobs:
                print(f"Scraping page {page}...")
                
                # Wait for job listings to load
                try:
                    self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='job-card'], .job-card, .job-listing"))
                    )
                except:
                    print("No job listings found on this page")
                    break
                
                # Get page source and parse with BeautifulSoup
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # Try different selectors for job cards
                job_cards = (
                    soup.select("[data-testid='job-card']") or
                    soup.select(".job-card") or
                    soup.select(".job-listing") or
                    soup.select("[class*='job']") or
                    soup.select("article")
                )
                
                if not job_cards:
                    print("No job cards found with current selectors")
                    break
                
                print(f"Found {len(job_cards)} job cards on page {page}")
                
                for card in job_cards:
                    if jobs_scraped >= num_jobs:
                        break
                    
                    try:
                        job_data = self._extract_job_data(card)
                        if job_data:
                            self.jobs.append(job_data)
                            jobs_scraped += 1
                            print(f"Scraped job {jobs_scraped}: {job_data.get('title', 'Unknown')}")
                    except Exception as e:
                        print(f"Error extracting job data: {e}")
                        continue
                
                # Try to go to next page
                if jobs_scraped < num_jobs:
                    try:
                        next_button = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Næste') or contains(text(), 'Next')]")
                        if next_button.is_enabled():
                            next_button.click()
                            time.sleep(3)
                            page += 1
                        else:
                            print("No more pages available")
                            break
                    except:
                        print("No next page button found")
                        break
            
            print(f"Successfully scraped {len(self.jobs)} jobs")
            
        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            self.driver.quit()
    
    def _extract_job_data(self, card):
        """Extract job data from a job card"""
        try:
            # Initialize job data
            job_data = {
                'title': '',
                'company': '',
                'location': '',
                'salary': '',
                'job_type': '',
                'posted_date': '',
                'description': '',
                'requirements': '',
                'url': '',
                'scraped_at': datetime.now().isoformat()
            }
            
            # Extract title
            title_selectors = [
                'h2', 'h3', '[data-testid="job-title"]', '.job-title', '.title',
                '[class*="title"]', 'a[href*="/job/"]'
            ]
            for selector in title_selectors:
                title_elem = card.select_one(selector)
                if title_elem:
                    job_data['title'] = title_elem.get_text(strip=True)
                    # Get URL if it's a link
                    if title_elem.name == 'a' and title_elem.get('href'):
                        href = title_elem.get('href')
                        if href.startswith('/'):
                            job_data['url'] = self.base_url + href
                        else:
                            job_data['url'] = href
                    break
            
            # Extract company
            company_selectors = [
                '[data-testid="company-name"]', '.company', '.employer',
                '[class*="company"]', '[class*="employer"]'
            ]
            for selector in company_selectors:
                company_elem = card.select_one(selector)
                if company_elem:
                    job_data['company'] = company_elem.get_text(strip=True)
                    break
            
            # Extract location
            location_selectors = [
                '[data-testid="location"]', '.location', '.place',
                '[class*="location"]', '[class*="place"]'
            ]
            for selector in location_selectors:
                location_elem = card.select_one(selector)
                if location_elem:
                    job_data['location'] = location_elem.get_text(strip=True)
                    break
            
            # Extract salary
            salary_selectors = [
                '[data-testid="salary"]', '.salary', '.compensation',
                '[class*="salary"]', '[class*="compensation"]'
            ]
            for selector in salary_selectors:
                salary_elem = card.select_one(selector)
                if salary_elem:
                    job_data['salary'] = salary_elem.get_text(strip=True)
                    break
            
            # Extract job type
            job_type_selectors = [
                '[data-testid="job-type"]', '.job-type', '.employment-type',
                '[class*="type"]', '[class*="employment"]'
            ]
            for selector in job_type_selectors:
                job_type_elem = card.select_one(selector)
                if job_type_elem:
                    job_data['job_type'] = job_type_elem.get_text(strip=True)
                    break
            
            # Extract posted date
            date_selectors = [
                '[data-testid="posted-date"]', '.date', '.posted',
                '[class*="date"]', '[class*="posted"]'
            ]
            for selector in date_selectors:
                date_elem = card.select_one(selector)
                if date_elem:
                    job_data['posted_date'] = date_elem.get_text(strip=True)
                    break
            
            # Extract description (usually truncated in cards)
            desc_selectors = [
                '[data-testid="description"]', '.description', '.summary',
                '[class*="description"]', '[class*="summary"]'
            ]
            for selector in desc_selectors:
                desc_elem = card.select_one(selector)
                if desc_elem:
                    job_data['description'] = desc_elem.get_text(strip=True)
                    break
            
            # If no URL found, try to find any link in the card
            if not job_data['url']:
                link_elem = card.select_one('a[href*="/job/"]')
                if link_elem and link_elem.get('href'):
                    href = link_elem.get('href')
                    if href.startswith('/'):
                        job_data['url'] = self.base_url + href
                    else:
                        job_data['url'] = href
            
            # Only return if we have at least a title
            if job_data['title']:
                return job_data
            return None
            
        except Exception as e:
            print(f"Error extracting job data: {e}")
            return None
    
    def save_to_json(self, filename="jobindex_jobs.json"):
        """Save scraped jobs to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, ensure_ascii=False, indent=2)
        print(f"Jobs saved to {filename}")
    
    def save_to_csv(self, filename="jobindex_jobs.csv"):
        """Save scraped jobs to CSV file"""
        df = pd.DataFrame(self.jobs)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Jobs saved to {filename}")
    
    def print_summary(self):
        """Print a summary of scraped jobs"""
        print(f"\n=== JOB SCRAPING SUMMARY ===")
        print(f"Total jobs scraped: {len(self.jobs)}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.jobs:
            print(f"\nSample jobs:")
            for i, job in enumerate(self.jobs[:3], 1):
                print(f"{i}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
                print(f"   Location: {job.get('location', 'N/A')}")
                print(f"   URL: {job.get('url', 'N/A')}")
                print()


def main():
    """Main function to run the scraper"""
    print("Starting Jobindex Scraper...")
    
    # Initialize scraper
    scraper = JobindexScraper(headless=False)  # Set to True for headless mode
    
    # Scrape 10 jobs
    scraper.scrape_jobs(num_jobs=10)
    
    # Save results
    scraper.save_to_json()
    scraper.save_to_csv()
    
    # Print summary
    scraper.print_summary()


if __name__ == "__main__":
    main()



