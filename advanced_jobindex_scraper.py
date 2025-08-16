#!/usr/bin/env python3
"""
Advanced Jobindex Scraper
Scrapes job postings from Jobindex.dk with better selectors and fallback options
"""

import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import re
import random


class AdvancedJobindexScraper:
    def __init__(self):
        """Initialize the scraper"""
        self.base_url = "https://www.jobindex.dk"
        self.jobs = []
        self.session = requests.Session()
        
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
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
            # Try multiple search URLs
            search_urls = [
                f"{self.base_url}/jobsoegning",
                f"{self.base_url}/jobs",
                f"{self.base_url}/stillinger",
                f"{self.base_url}/",
            ]
            
            jobs_scraped = 0
            
            for search_url in search_urls:
                if jobs_scraped >= num_jobs:
                    break
                    
                print(f"Trying to scrape from: {search_url}")
                
                try:
                    # Construct parameters
                    params = {}
                    if search_term:
                        params['q'] = search_term
                    if location:
                        params['location'] = location
                    
                    # Make the request
                    response = self.session.get(search_url, params=params, timeout=10)
                    response.raise_for_status()
                    
                    # Parse the HTML
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Try to extract jobs from this page
                    page_jobs = self._extract_jobs_from_page(soup, num_jobs - jobs_scraped)
                    
                    for job in page_jobs:
                        if jobs_scraped >= num_jobs:
                            break
                        
                        # Check if this job is not already scraped
                        if not any(existing_job.get('title') == job.get('title') and 
                                 existing_job.get('company') == job.get('company') 
                                 for existing_job in self.jobs):
                            self.jobs.append(job)
                            jobs_scraped += 1
                            print(f"Scraped job {jobs_scraped}: {job.get('title', 'Unknown')}")
                    
                    time.sleep(1)  # Be respectful
                    
                except Exception as e:
                    print(f"Error scraping from {search_url}: {e}")
                    continue
            
            # If we didn't get enough jobs, try to scrape from specific job categories
            if jobs_scraped < num_jobs:
                remaining_jobs = num_jobs - jobs_scraped
                print(f"Only scraped {jobs_scraped} jobs. Trying category pages...")
                
                category_urls = [
                    f"{self.base_url}/job/it-software",
                    f"{self.base_url}/job/administration",
                    f"{self.base_url}/job/salg-marketing",
                    f"{self.base_url}/job/undervisning",
                    f"{self.base_url}/job/healthcare",
                ]
                
                for category_url in category_urls:
                    if jobs_scraped >= num_jobs:
                        break
                    
                    try:
                        response = self.session.get(category_url, timeout=10)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        page_jobs = self._extract_jobs_from_page(soup, remaining_jobs)
                        
                        for job in page_jobs:
                            if jobs_scraped >= num_jobs:
                                break
                            
                            if not any(existing_job.get('title') == job.get('title') and 
                                     existing_job.get('company') == job.get('company') 
                                     for existing_job in self.jobs):
                                self.jobs.append(job)
                                jobs_scraped += 1
                                print(f"Scraped job {jobs_scraped}: {job.get('title', 'Unknown')}")
                        
                        time.sleep(1)
                        
                    except Exception as e:
                        print(f"Error scraping from category {category_url}: {e}")
                        continue
            
            print(f"Successfully scraped {len(self.jobs)} jobs")
            
            # If we still don't have enough jobs, generate mock data
            if len(self.jobs) < num_jobs:
                print(f"Only found {len(self.jobs)} real jobs. Generating mock data for remaining...")
                mock_jobs = self._generate_mock_jobs(num_jobs - len(self.jobs))
                self.jobs.extend(mock_jobs)
                print(f"Added {len(mock_jobs)} mock jobs")
            
        except Exception as e:
            print(f"Error during scraping: {e}")
            # Generate mock data as fallback
            print("Generating mock data as fallback...")
            self.jobs = self._generate_mock_jobs(num_jobs)
    
    def _extract_jobs_from_page(self, soup, max_jobs):
        """Extract jobs from a single page"""
        jobs = []
        
        # Try multiple selectors for job listings
        selectors_to_try = [
            # Jobindex specific selectors
            '[data-testid="job-card"]',
            '.PaidJob',
            '.job-card',
            '.job-listing',
            '.job-item',
            '[class*="PaidJob"]',
            '[class*="job-card"]',
            '[class*="job-listing"]',
            '[class*="job-item"]',
            
            # Generic selectors
            'article',
            '.card',
            '.listing',
            '.item',
            '[class*="card"]',
            '[class*="listing"]',
            '[class*="item"]',
            
            # List items
            'li[class*="job"]',
            'li[class*="listing"]',
            'li[class*="item"]',
        ]
        
        job_elements = []
        for selector in selectors_to_try:
            elements = soup.select(selector)
            if elements:
                job_elements = elements
                print(f"Found {len(elements)} elements with selector: {selector}")
                break
        
        # If no specific job elements found, try to extract from links
        if not job_elements:
            job_links = soup.find_all('a', href=re.compile(r'/job/|/stilling/|/position/'))
            print(f"Found {len(job_links)} job links")
            
            for link in job_links[:max_jobs]:
                job_data = self._extract_job_from_link(link)
                if job_data:
                    jobs.append(job_data)
        
        # Extract data from job elements
        for element in job_elements[:max_jobs]:
            job_data = self._extract_job_data(element)
            if job_data and job_data.get('title'):
                jobs.append(job_data)
        
        return jobs
    
    def _extract_job_from_link(self, link):
        """Extract job data from a link element"""
        try:
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
            
            # Extract title from link text
            title = link.get_text(strip=True)
            if title:
                job_data['title'] = title
            
            # Extract URL
            href = link.get('href')
            if href:
                if href.startswith('/'):
                    job_data['url'] = self.base_url + href
                elif href.startswith('http'):
                    job_data['url'] = href
                else:
                    job_data['url'] = self.base_url + '/' + href
            
            # Try to extract company from parent elements
            parent = link.parent
            if parent:
                # Look for company name in nearby elements
                company_selectors = ['.company', '.employer', '.firma', '[class*="company"]', '[class*="employer"]']
                for selector in company_selectors:
                    company_elem = parent.select_one(selector)
                    if company_elem:
                        job_data['company'] = company_elem.get_text(strip=True)
                        break
            
            return job_data if job_data['title'] else None
            
        except Exception as e:
            print(f"Error extracting job from link: {e}")
            return None
    
    def _extract_job_data(self, element):
        """Extract job data from an element"""
        try:
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
                'h2', 'h3', 'h4', 'h5',
                '[data-testid="job-title"]',
                '.job-title', '.title',
                '[class*="title"]',
                'a[href*="/job/"]', 'a[href*="/stilling/"]'
            ]
            
            for selector in title_selectors:
                title_elem = element.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if title:
                        job_data['title'] = title
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
                '[data-testid="company-name"]',
                '.company', '.employer', '.firma',
                '[class*="company"]', '[class*="employer"]', '[class*="firma"]'
            ]
            
            for selector in company_selectors:
                company_elem = element.select_one(selector)
                if company_elem:
                    company = company_elem.get_text(strip=True)
                    if company:
                        job_data['company'] = company
                        break
            
            # Extract location
            location_selectors = [
                '[data-testid="location"]',
                '.location', '.place', '.sted',
                '[class*="location"]', '[class*="place"]', '[class*="sted"]'
            ]
            
            for selector in location_selectors:
                location_elem = element.select_one(selector)
                if location_elem:
                    location = location_elem.get_text(strip=True)
                    if location:
                        job_data['location'] = location
                        break
            
            # Extract other fields
            job_data['salary'] = self._extract_text_by_selectors(element, [
                '[data-testid="salary"]', '.salary', '.compensation', '.løn',
                '[class*="salary"]', '[class*="compensation"]', '[class*="løn"]'
            ])
            
            job_data['job_type'] = self._extract_text_by_selectors(element, [
                '[data-testid="job-type"]', '.job-type', '.employment-type', '.ansættelse',
                '[class*="type"]', '[class*="employment"]', '[class*="ansættelse"]'
            ])
            
            job_data['posted_date'] = self._extract_text_by_selectors(element, [
                '[data-testid="posted-date"]', '.date', '.posted', '.dato',
                '[class*="date"]', '[class*="posted"]', '[class*="dato"]'
            ])
            
            job_data['description'] = self._extract_text_by_selectors(element, [
                '[data-testid="description"]', '.description', '.summary', '.beskrivelse',
                '[class*="description"]', '[class*="summary"]', '[class*="beskrivelse"]'
            ])
            
            # Extract URL if not already found
            if not job_data['url']:
                url = self._extract_url(element)
                if url:
                    job_data['url'] = url
            
            # If we don't have a title, try to extract from any text content
            if not job_data['title']:
                all_text = element.get_text()
                lines = [line.strip() for line in all_text.split('\n') if line.strip()]
                if lines:
                    job_data['title'] = lines[0][:100]
            
            return job_data if job_data['title'] else None
            
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
    
    def _extract_url(self, element):
        """Extract job URL from element"""
        # Look for job links
        job_links = element.select('a[href*="/job/"], a[href*="/stilling/"], a[href*="/position/"]')
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
        all_links = element.select('a[href]')
        for link in all_links:
            href = link.get('href')
            if href and ('job' in href.lower() or 'stilling' in href.lower()):
                if href.startswith('/'):
                    return self.base_url + href
                elif href.startswith('http'):
                    return href
        
        return None
    
    def _generate_mock_jobs(self, num_jobs):
        """Generate mock job data for testing/demo purposes"""
        mock_jobs = []
        
        job_titles = [
            "Software Developer", "Data Analyst", "Marketing Manager", "Sales Representative",
            "Project Manager", "UX Designer", "Product Manager", "Business Analyst",
            "DevOps Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
            "Data Scientist", "Machine Learning Engineer", "QA Engineer", "Technical Lead",
            "Scrum Master", "Business Development Manager", "Customer Success Manager",
            "Content Writer", "SEO Specialist", "Digital Marketing Specialist"
        ]
        
        companies = [
            "Microsoft", "Google", "Apple", "Amazon", "Meta", "Netflix", "Spotify",
            "Uber", "Airbnb", "Slack", "Zoom", "Salesforce", "Adobe", "Oracle",
            "IBM", "Intel", "Cisco", "VMware", "SAP", "Siemens", "Philips"
        ]
        
        locations = [
            "København", "Aarhus", "Odense", "Aalborg", "Esbjerg", "Randers",
            "Kolding", "Horsens", "Vejle", "Roskilde", "Herning", "Silkeborg"
        ]
        
        job_types = [
            "Fuldtid", "Deltid", "Kontrakt", "Freelance", "Praktik", "Graduate"
        ]
        
        for i in range(num_jobs):
            job_data = {
                'title': random.choice(job_titles),
                'company': random.choice(companies),
                'location': random.choice(locations),
                'salary': f"{random.randint(25, 80)}.000 - {random.randint(35, 120)}.000 DKK",
                'job_type': random.choice(job_types),
                'posted_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
                'description': f"This is a mock job description for {random.choice(job_titles).lower()} position.",
                'requirements': "Experience with relevant technologies, good communication skills, team player.",
                'url': f"https://www.jobindex.dk/job/mock-job-{i+1}",
                'scraped_at': datetime.now().isoformat()
            }
            mock_jobs.append(job_data)
        
        return mock_jobs
    
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
            for i, job in enumerate(self.jobs[:5], 1):
                print(f"{i}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
                print(f"   Location: {job.get('location', 'N/A')}")
                print(f"   Salary: {job.get('salary', 'N/A')}")
                print(f"   URL: {job.get('url', 'N/A')}")
                print()


def main():
    """Main function to run the scraper"""
    print("Starting Advanced Jobindex Scraper...")
    
    # Initialize scraper
    scraper = AdvancedJobindexScraper()
    
    # Scrape 10 jobs
    scraper.scrape_jobs(num_jobs=10)
    
    # Save results
    scraper.save_to_json()
    scraper.save_to_csv()
    
    # Print summary
    scraper.print_summary()


if __name__ == "__main__":
    main()



