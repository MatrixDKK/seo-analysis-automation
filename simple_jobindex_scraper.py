#!/usr/bin/env python3
"""
Simple Jobindex Scraper
Scrapes job postings from Jobindex.dk using requests and BeautifulSoup
"""

import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re


class SimpleJobindexScraper:
    def __init__(self):
        """Initialize the scraper"""
        self.base_url = "https://www.jobindex.dk"
        self.jobs = []
        self.session = requests.Session()
        
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
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
            params = {}
            if search_term:
                params['q'] = search_term
            if location:
                params['location'] = location
            
            print(f"Searching for jobs at: {search_url}")
            if params:
                print(f"Search parameters: {params}")
            
            # Make the request
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find job listings
            jobs_scraped = 0
            page = 1
            
            while jobs_scraped < num_jobs:
                print(f"Scraping page {page}...")
                
                # Try different selectors for job cards
                job_cards = (
                    soup.select("[data-testid='job-card']") or
                    soup.select(".job-card") or
                    soup.select(".job-listing") or
                    soup.select("[class*='job']") or
                    soup.select("article") or
                    soup.select(".PaidJob") or
                    soup.select("[class*='PaidJob']") or
                    soup.select(".job-item") or
                    soup.select("[class*='job-item']")
                )
                
                if not job_cards:
                    # Try alternative selectors
                    job_cards = (
                        soup.select("div[class*='job']") or
                        soup.select("div[class*='listing']") or
                        soup.select("div[class*='card']") or
                        soup.select("li[class*='job']") or
                        soup.select("div[class*='result']")
                    )
                
                if not job_cards:
                    print("No job cards found. Trying to extract from page structure...")
                    # Try to extract any job-related information from the page
                    job_cards = self._extract_jobs_from_page_structure(soup)
                
                if not job_cards:
                    print("No job listings found on this page")
                    break
                
                print(f"Found {len(job_cards)} potential job cards on page {page}")
                
                for card in job_cards:
                    if jobs_scraped >= num_jobs:
                        break
                    
                    try:
                        job_data = self._extract_job_data(card)
                        if job_data and job_data.get('title'):
                            # Check if this job is not already scraped
                            if not any(job.get('title') == job_data['title'] and 
                                     job.get('company') == job_data['company'] 
                                     for job in self.jobs):
                                self.jobs.append(job_data)
                                jobs_scraped += 1
                                print(f"Scraped job {jobs_scraped}: {job_data.get('title', 'Unknown')}")
                    except Exception as e:
                        print(f"Error extracting job data: {e}")
                        continue
                
                # Try to go to next page
                if jobs_scraped < num_jobs:
                    next_url = self._find_next_page(soup)
                    if next_url:
                        print(f"Going to next page: {next_url}")
                        response = self.session.get(next_url)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.content, 'html.parser')
                        page += 1
                        time.sleep(2)  # Be respectful with delays
                    else:
                        print("No next page found")
                        break
                else:
                    break
            
            print(f"Successfully scraped {len(self.jobs)} jobs")
            
        except Exception as e:
            print(f"Error during scraping: {e}")
    
    def _extract_jobs_from_page_structure(self, soup):
        """Extract job information from page structure when specific selectors fail"""
        job_cards = []
        
        # Look for any elements that might contain job information
        potential_jobs = []
        
        # Look for links that might be job postings
        job_links = soup.find_all('a', href=re.compile(r'/job/|/stilling/|/position/'))
        for link in job_links:
            # Create a simple div to represent this job
            job_div = soup.new_tag('div')
            job_div.append(link)
            potential_jobs.append(job_div)
        
        # Look for elements with job-related text
        job_text_elements = soup.find_all(text=re.compile(r'stilling|job|position|ansættelse', re.IGNORECASE))
        for text_elem in job_text_elements:
            if text_elem.parent:
                potential_jobs.append(text_elem.parent)
        
        return potential_jobs[:20]  # Limit to avoid too many false positives
    
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
            
            # Extract title - try multiple approaches
            title = self._extract_text_by_selectors(card, [
                'h2', 'h3', 'h4', '[data-testid="job-title"]', '.job-title', '.title',
                '[class*="title"]', 'a[href*="/job/"]', 'a[href*="/stilling/"]'
            ])
            if title:
                job_data['title'] = title
            
            # Extract company
            company = self._extract_text_by_selectors(card, [
                '[data-testid="company-name"]', '.company', '.employer',
                '[class*="company"]', '[class*="employer"]', '.firma', '[class*="firma"]'
            ])
            if company:
                job_data['company'] = company
            
            # Extract location
            location = self._extract_text_by_selectors(card, [
                '[data-testid="location"]', '.location', '.place',
                '[class*="location"]', '[class*="place"]', '.sted', '[class*="sted"]'
            ])
            if location:
                job_data['location'] = location
            
            # Extract salary
            salary = self._extract_text_by_selectors(card, [
                '[data-testid="salary"]', '.salary', '.compensation',
                '[class*="salary"]', '[class*="compensation"]', '.løn', '[class*="løn"]'
            ])
            if salary:
                job_data['salary'] = salary
            
            # Extract job type
            job_type = self._extract_text_by_selectors(card, [
                '[data-testid="job-type"]', '.job-type', '.employment-type',
                '[class*="type"]', '[class*="employment"]', '.ansættelse', '[class*="ansættelse"]'
            ])
            if job_type:
                job_data['job_type'] = job_type
            
            # Extract posted date
            posted_date = self._extract_text_by_selectors(card, [
                '[data-testid="posted-date"]', '.date', '.posted',
                '[class*="date"]', '[class*="posted"]', '.dato', '[class*="dato"]'
            ])
            if posted_date:
                job_data['posted_date'] = posted_date
            
            # Extract description
            description = self._extract_text_by_selectors(card, [
                '[data-testid="description"]', '.description', '.summary',
                '[class*="description"]', '[class*="summary"]', '.beskrivelse', '[class*="beskrivelse"]'
            ])
            if description:
                job_data['description'] = description
            
            # Extract URL
            url = self._extract_url(card)
            if url:
                job_data['url'] = url
            
            # If we don't have a title, try to extract from any text content
            if not job_data['title']:
                # Look for any text that might be a job title
                all_text = card.get_text()
                lines = [line.strip() for line in all_text.split('\n') if line.strip()]
                if lines:
                    # Take the first non-empty line as potential title
                    job_data['title'] = lines[0][:100]  # Limit length
            
            return job_data
            
        except Exception as e:
            print(f"Error extracting job data: {e}")
            return None
    
    def _extract_text_by_selectors(self, element, selectors):
        """Extract text using multiple selectors"""
        for selector in selectors:
            try:
                elem = element.select_one(selector)
                if elem:
                    text = elem.get_text(strip=True)
                    if text:
                        return text
            except:
                continue
        return None
    
    def _extract_url(self, card):
        """Extract job URL from card"""
        # Look for job links
        job_links = card.select('a[href*="/job/"], a[href*="/stilling/"], a[href*="/position/"]')
        if job_links:
            href = job_links[0].get('href')
            if href:
                if href.startswith('/'):
                    return self.base_url + href
                elif href.startswith('http'):
                    return href
                else:
                    return self.base_url + '/' + href
        
        # Look for any link that might be a job link
        all_links = card.select('a[href]')
        for link in all_links:
            href = link.get('href')
            if href and ('job' in href.lower() or 'stilling' in href.lower()):
                if href.startswith('/'):
                    return self.base_url + href
                elif href.startswith('http'):
                    return href
        
        return None
    
    def _find_next_page(self, soup):
        """Find the next page URL"""
        # Look for next page links
        next_links = soup.find_all('a', text=re.compile(r'næste|next|>', re.IGNORECASE))
        for link in next_links:
            href = link.get('href')
            if href:
                if href.startswith('/'):
                    return self.base_url + href
                elif href.startswith('http'):
                    return href
        
        # Look for pagination
        pagination = soup.select('.pagination a, .pager a, [class*="pagination"] a, [class*="pager"] a')
        for link in pagination:
            if 'next' in link.get_text().lower() or '>' in link.get_text():
                href = link.get('href')
                if href:
                    if href.startswith('/'):
                        return self.base_url + href
                    elif href.startswith('http'):
                        return href
        
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
    print("Starting Simple Jobindex Scraper...")
    
    # Initialize scraper
    scraper = SimpleJobindexScraper()
    
    # Scrape 10 jobs
    scraper.scrape_jobs(num_jobs=10)
    
    # Save results
    scraper.save_to_json()
    scraper.save_to_csv()
    
    # Print summary
    scraper.print_summary()


if __name__ == "__main__":
    main()



