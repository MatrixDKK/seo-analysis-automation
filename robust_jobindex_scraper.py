#!/usr/bin/env python3
"""
Robust Jobindex Scraper
Scrapes actual job postings from Jobindex.dk with better analysis of the site structure
"""

import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import urllib.parse


class RobustJobindexScraper:
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
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        })
    
    def scrape_jobs(self, num_jobs=10, search_term="", location=""):
        """
        Scrape actual job postings from Jobindex
        
        Args:
            num_jobs (int): Number of jobs to scrape
            search_term (str): Job search term
            location (str): Location to search in
        """
        try:
            print(f"Starting to scrape {num_jobs} real job postings from Jobindex...")
            
            # Try different approaches to find job listings
            approaches = [
                self._scrape_from_search_page,
                self._scrape_from_job_categories,
                self._scrape_from_recent_jobs,
                self._scrape_from_company_pages
            ]
            
            jobs_scraped = 0
            
            for approach in approaches:
                if jobs_scraped >= num_jobs:
                    break
                
                try:
                    remaining_jobs = num_jobs - jobs_scraped
                    new_jobs = approach(remaining_jobs, search_term, location)
                    
                    for job in new_jobs:
                        if jobs_scraped >= num_jobs:
                            break
                        
                        # Check if this job is not already scraped
                        if not any(existing_job.get('title') == job.get('title') and 
                                 existing_job.get('company') == job.get('company') 
                                 for existing_job in self.jobs):
                            self.jobs.append(job)
                            jobs_scraped += 1
                            print(f"Scraped job {jobs_scraped}: {job.get('title', 'Unknown')} at {job.get('company', 'Unknown')}")
                    
                    time.sleep(2)  # Be respectful
                    
                except Exception as e:
                    print(f"Error with approach {approach.__name__}: {e}")
                    continue
            
            print(f"Successfully scraped {len(self.jobs)} real jobs")
            
        except Exception as e:
            print(f"Error during scraping: {e}")
    
    def _scrape_from_search_page(self, max_jobs, search_term="", location=""):
        """Scrape from the main search page"""
        jobs = []
        
        # Try different search URLs
        search_urls = [
            f"{self.base_url}/jobsoegning",
            f"{self.base_url}/jobs",
            f"{self.base_url}/stillinger",
            f"{self.base_url}/job",
        ]
        
        for search_url in search_urls:
            if len(jobs) >= max_jobs:
                break
                
            try:
                print(f"Trying search URL: {search_url}")
                
                # Construct parameters
                params = {}
                if search_term:
                    params['q'] = search_term
                if location:
                    params['location'] = location
                
                # Make the request
                response = self.session.get(search_url, params=params, timeout=15)
                response.raise_for_status()
                
                # Parse the HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Save HTML for debugging
                with open(f"debug_page_{len(jobs)}.html", "w", encoding="utf-8") as f:
                    f.write(soup.prettify())
                
                # Look for job listings with more specific patterns
                page_jobs = self._extract_jobs_from_page(soup, max_jobs - len(jobs))
                jobs.extend(page_jobs)
                
                print(f"Found {len(page_jobs)} jobs from {search_url}")
                
            except Exception as e:
                print(f"Error scraping from {search_url}: {e}")
                continue
        
        return jobs
    
    def _scrape_from_job_categories(self, max_jobs, search_term="", location=""):
        """Scrape from specific job category pages"""
        jobs = []
        
        # Common job categories on Jobindex
        categories = [
            "it-software", "administration", "salg-marketing", "undervisning",
            "healthcare", "engineering", "finance", "consulting", "retail",
            "logistics", "media", "legal", "hr", "design", "research"
        ]
        
        for category in categories:
            if len(jobs) >= max_jobs:
                break
                
            try:
                category_url = f"{self.base_url}/job/{category}"
                print(f"Trying category: {category_url}")
                
                response = self.session.get(category_url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                page_jobs = self._extract_jobs_from_page(soup, max_jobs - len(jobs))
                jobs.extend(page_jobs)
                
                print(f"Found {len(page_jobs)} jobs from category {category}")
                time.sleep(1)
                
            except Exception as e:
                print(f"Error scraping category {category}: {e}")
                continue
        
        return jobs
    
    def _scrape_from_recent_jobs(self, max_jobs, search_term="", location=""):
        """Scrape from recent jobs page"""
        jobs = []
        
        try:
            recent_url = f"{self.base_url}/job/nyeste"
            print(f"Trying recent jobs: {recent_url}")
            
            response = self.session.get(recent_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            page_jobs = self._extract_jobs_from_page(soup, max_jobs)
            jobs.extend(page_jobs)
            
            print(f"Found {len(page_jobs)} recent jobs")
            
        except Exception as e:
            print(f"Error scraping recent jobs: {e}")
        
        return jobs
    
    def _scrape_from_company_pages(self, max_jobs, search_term="", location=""):
        """Scrape from company-specific pages"""
        jobs = []
        
        # Try some major Danish companies
        companies = [
            "novo-nordisk", "maersk", "vestas", "carlsberg", "coloplast",
            "chr-hansen", "genmab", "lundbeck", "orsted", "rockwool"
        ]
        
        for company in companies:
            if len(jobs) >= max_jobs:
                break
                
            try:
                company_url = f"{self.base_url}/company/{company}/jobs"
                print(f"Trying company: {company_url}")
                
                response = self.session.get(company_url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                page_jobs = self._extract_jobs_from_page(soup, max_jobs - len(jobs))
                jobs.extend(page_jobs)
                
                print(f"Found {len(page_jobs)} jobs from company {company}")
                time.sleep(1)
                
            except Exception as e:
                print(f"Error scraping company {company}: {e}")
                continue
        
        return jobs
    
    def _extract_jobs_from_page(self, soup, max_jobs):
        """Extract jobs from a single page with improved selectors"""
        jobs = []
        
        # First, let's analyze the page structure
        print("Analyzing page structure...")
        
        # Look for common job listing patterns
        potential_job_elements = []
        
        # Method 1: Look for job-specific CSS classes
        job_selectors = [
            '[class*="job"]', '[class*="stilling"]', '[class*="position"]',
            '[class*="listing"]', '[class*="card"]', '[class*="item"]',
            '[data-testid*="job"]', '[data-testid*="listing"]',
            'article', '.result', '.search-result'
        ]
        
        for selector in job_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"Found {len(elements)} elements with selector: {selector}")
                potential_job_elements.extend(elements)
        
        # Method 2: Look for job links
        job_links = soup.find_all('a', href=re.compile(r'/job/|/stilling/|/position/|/vacancy/'))
        print(f"Found {len(job_links)} job links")
        
        # Method 3: Look for elements containing job-related text
        job_text_patterns = [
            r'\b(job|stilling|position|vacancy|ansættelse)\b',
            r'\b(software|developer|engineer|analyst|manager)\b',
            r'\b(fuldtid|deltid|kontrakt|freelance)\b'
        ]
        
        for pattern in job_text_patterns:
            elements = soup.find_all(text=re.compile(pattern, re.IGNORECASE))
            for element in elements:
                if element.parent and element.parent not in potential_job_elements:
                    potential_job_elements.append(element.parent)
        
        # Method 4: Look for salary information
        salary_elements = soup.find_all(text=re.compile(r'\d+\.?\d*\s*(kr|dkk|kroner)', re.IGNORECASE))
        for element in salary_elements:
            if element.parent and element.parent not in potential_job_elements:
                potential_job_elements.append(element.parent)
        
        # Remove duplicates and limit
        unique_elements = []
        seen = set()
        for element in potential_job_elements:
            element_id = id(element)
            if element_id not in seen:
                seen.add(element_id)
                unique_elements.append(element)
        
        print(f"Found {len(unique_elements)} unique potential job elements")
        
        # Extract job data from elements
        for element in unique_elements[:max_jobs]:
            job_data = self._extract_job_data_from_element(element)
            if job_data and job_data.get('title'):
                jobs.append(job_data)
        
        # If we didn't find enough jobs from elements, try extracting from links
        if len(jobs) < max_jobs:
            remaining = max_jobs - len(jobs)
            for link in job_links[:remaining]:
                job_data = self._extract_job_data_from_link(link)
                if job_data and job_data.get('title'):
                    jobs.append(job_data)
        
        return jobs
    
    def _extract_job_data_from_element(self, element):
        """Extract job data from a page element"""
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
            
            # Extract title from various possible locations
            title_candidates = []
            
            # Look for headings
            headings = element.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for heading in headings:
                text = heading.get_text(strip=True)
                if text and len(text) > 5 and len(text) < 100:
                    title_candidates.append(text)
            
            # Look for links that might be job titles
            links = element.find_all('a')
            for link in links:
                text = link.get_text(strip=True)
                href = link.get('href', '')
                if text and len(text) > 5 and len(text) < 100 and ('/job/' in href or '/stilling/' in href):
                    title_candidates.append(text)
                    if href and not job_data['url']:
                        if href.startswith('/'):
                            job_data['url'] = self.base_url + href
                        else:
                            job_data['url'] = href
            
            # Look for strong/bold text that might be titles
            strong_elements = element.find_all(['strong', 'b'])
            for strong in strong_elements:
                text = strong.get_text(strip=True)
                if text and len(text) > 5 and len(text) < 100:
                    title_candidates.append(text)
            
            # Select the best title candidate
            if title_candidates:
                # Prefer longer, more descriptive titles
                job_data['title'] = max(title_candidates, key=len)
            
            # Extract company name
            company_patterns = [
                r'\b(company|firma|virksomhed|employer)\b',
                r'\b(inc|corp|ltd|aps|as)\b',
                r'\b(danmark|denmark)\b'
            ]
            
            all_text = element.get_text()
            for pattern in company_patterns:
                matches = re.findall(pattern, all_text, re.IGNORECASE)
                if matches:
                    # Try to extract company name from context
                    lines = all_text.split('\n')
                    for line in lines:
                        if any(match.lower() in line.lower() for match in matches):
                            company = line.strip()
                            if company and len(company) > 2 and company != job_data['title']:
                                job_data['company'] = company
                                break
            
            # Extract location
            location_patterns = [
                r'\b(københavn|aarhus|odense|aalborg|esbjerg|randers|kolding|horsens|vejle|roskilde|herning|silkeborg)\b',
                r'\b(copenhagen|denmark|danish)\b'
            ]
            
            for pattern in location_patterns:
                matches = re.findall(pattern, all_text, re.IGNORECASE)
                if matches:
                    job_data['location'] = matches[0].title()
                    break
            
            # Extract salary
            salary_patterns = [
                r'(\d+\.?\d*)\s*(kr|dkk|kroner)',
                r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*(kr|dkk|kroner)',
                r'(løn|salary|compensation)'
            ]
            
            for pattern in salary_patterns:
                matches = re.findall(pattern, all_text, re.IGNORECASE)
                if matches:
                    if isinstance(matches[0], tuple):
                        job_data['salary'] = f"{matches[0][0]} - {matches[0][1]} {matches[0][2].upper()}"
                    else:
                        job_data['salary'] = f"{matches[0]} {matches[1].upper()}"
                    break
            
            # Extract job type
            job_type_patterns = [
                r'\b(fuldtid|full.?time)\b',
                r'\b(deltid|part.?time)\b',
                r'\b(kontrakt|contract)\b',
                r'\b(freelance|freelancer)\b',
                r'\b(praktik|internship)\b'
            ]
            
            for pattern in job_type_patterns:
                matches = re.findall(pattern, all_text, re.IGNORECASE)
                if matches:
                    job_data['job_type'] = matches[0].title()
                    break
            
            # Extract posted date
            date_patterns = [
                r'(\d{1,2})\.(\d{1,2})\.(\d{2,4})',
                r'(\d{4})-(\d{1,2})-(\d{1,2})',
                r'(i dag|today|yesterday|sidste uge)'
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, all_text, re.IGNORECASE)
                if matches:
                    job_data['posted_date'] = str(matches[0])
                    break
            
            # Extract description (first few lines of text)
            lines = [line.strip() for line in all_text.split('\n') if line.strip()]
            if lines:
                # Skip the title line and take next few lines as description
                desc_lines = [line for line in lines if line != job_data['title']][:3]
                if desc_lines:
                    job_data['description'] = ' '.join(desc_lines)
            
            # If no URL found, try to find any link in the element
            if not job_data['url']:
                all_links = element.find_all('a', href=True)
                for link in all_links:
                    href = link.get('href')
                    if href and ('job' in href.lower() or 'stilling' in href.lower()):
                        if href.startswith('/'):
                            job_data['url'] = self.base_url + href
                        else:
                            job_data['url'] = href
                        break
            
            return job_data if job_data['title'] else None
            
        except Exception as e:
            print(f"Error extracting job data from element: {e}")
            return None
    
    def _extract_job_data_from_link(self, link):
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
            if title and len(title) > 3:
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
            
            # Try to extract additional info from parent elements
            parent = link.parent
            if parent:
                parent_text = parent.get_text()
                
                # Look for company name
                company_patterns = [r'\b(inc|corp|ltd|aps|as)\b', r'\b(danmark|denmark)\b']
                for pattern in company_patterns:
                    matches = re.findall(pattern, parent_text, re.IGNORECASE)
                    if matches:
                        lines = parent_text.split('\n')
                        for line in lines:
                            if any(match.lower() in line.lower() for match in matches):
                                company = line.strip()
                                if company and company != title:
                                    job_data['company'] = company
                                    break
                
                # Look for location
                location_patterns = [r'\b(københavn|aarhus|odense|aalborg)\b']
                for pattern in location_patterns:
                    matches = re.findall(pattern, parent_text, re.IGNORECASE)
                    if matches:
                        job_data['location'] = matches[0].title()
                        break
            
            return job_data if job_data['title'] else None
            
        except Exception as e:
            print(f"Error extracting job data from link: {e}")
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
            for i, job in enumerate(self.jobs[:5], 1):
                print(f"{i}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
                print(f"   Location: {job.get('location', 'N/A')}")
                print(f"   Salary: {job.get('salary', 'N/A')}")
                print(f"   Type: {job.get('job_type', 'N/A')}")
                print(f"   URL: {job.get('url', 'N/A')}")
                print()


def main():
    """Main function to run the scraper"""
    print("Starting Robust Jobindex Scraper...")
    
    # Initialize scraper
    scraper = RobustJobindexScraper()
    
    # Scrape 10 jobs
    scraper.scrape_jobs(num_jobs=10)
    
    # Save results
    scraper.save_to_json()
    scraper.save_to_csv()
    
    # Print summary
    scraper.print_summary()


if __name__ == "__main__":
    main()



