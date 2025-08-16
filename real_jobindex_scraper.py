#!/usr/bin/env python3
"""
Real Jobindex Scraper
Extracts actual job postings from Jobindex.dk by parsing embedded JSON data
"""

import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re


class RealJobindexScraper:
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
        Scrape actual job postings from Jobindex
        
        Args:
            num_jobs (int): Number of jobs to scrape
            search_term (str): Job search term
            location (str): Location to search in
        """
        try:
            print(f"Starting to scrape {num_jobs} real job postings from Jobindex...")
            
            # Try different search URLs
            search_urls = [
                f"{self.base_url}/jobsoegning",
                f"{self.base_url}/job",
            ]
            
            jobs_scraped = 0
            
            for search_url in search_urls:
                if jobs_scraped >= num_jobs:
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
                    
                    # Extract job data from embedded JSON
                    page_jobs = self._extract_jobs_from_json(soup, num_jobs - jobs_scraped)
                    
                    for job in page_jobs:
                        if jobs_scraped >= num_jobs:
                            break
                        
                        # Check if this job is not already scraped
                        if not any(existing_job.get('tid') == job.get('tid') 
                                 for existing_job in self.jobs):
                            self.jobs.append(job)
                            jobs_scraped += 1
                            print(f"Scraped job {jobs_scraped}: {job.get('headline', 'Unknown')} at {job.get('company', {}).get('name', 'Unknown')}")
                    
                    time.sleep(2)  # Be respectful
                    
                except Exception as e:
                    print(f"Error scraping from {search_url}: {e}")
                    continue
            
            print(f"Successfully scraped {len(self.jobs)} real jobs")
            
        except Exception as e:
            print(f"Error during scraping: {e}")
    
    def _extract_jobs_from_json(self, soup, max_jobs):
        """Extract job data from embedded JSON in the page"""
        jobs = []
        
        try:
            # Look for the Stash variable that contains job data
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string and 'Stash' in script.string:
                    # Extract the JSON data from the Stash variable
                    stash_match = re.search(r'var Stash = ({.*?});', script.string, re.DOTALL)
                    if stash_match:
                        stash_data = json.loads(stash_match.group(1))
                        
                        # Look for job search results
                        if 'jobsearch/result_app' in stash_data:
                            job_data = stash_data['jobsearch/result_app']
                            
                            # Extract search response
                            if 'storeData' in job_data and 'searchResponse' in job_data['storeData']:
                                search_response = job_data['storeData']['searchResponse']
                                
                                # Extract results
                                if 'results' in search_response:
                                    results = search_response['results']
                                    
                                    for result in results[:max_jobs]:
                                        job_info = self._parse_job_result(result)
                                        if job_info:
                                            jobs.append(job_info)
                                    
                                    print(f"Found {len(jobs)} jobs from JSON data")
                                    break
            
            # If we didn't find jobs in Stash, try alternative methods
            if not jobs:
                jobs = self._extract_jobs_from_alternative_sources(soup, max_jobs)
        
        except Exception as e:
            print(f"Error extracting jobs from JSON: {e}")
            # Fallback to alternative methods
            jobs = self._extract_jobs_from_alternative_sources(soup, max_jobs)
        
        return jobs
    
    def _parse_job_result(self, result):
        """Parse a single job result from the JSON data"""
        try:
            job_info = {
                'tid': result.get('tid', ''),
                'title': result.get('headline', ''),
                'company': result.get('company', {}).get('name', ''),
                'company_id': result.get('company', {}).get('id', ''),
                'location': result.get('area', ''),
                'addresses': result.get('addresses', []),
                'posted_date': result.get('firstdate', ''),
                'last_date': result.get('lastdate', ''),
                'description': self._extract_description_from_html(result.get('html', '')),
                'url': result.get('url', ''),
                'share_url': result.get('share_url', ''),
                'rating': result.get('rating', {}),
                'is_archived': result.get('is_archived', False),
                'is_local': result.get('is_local', False),
                'scraped_at': datetime.now().isoformat()
            }
            
            # Extract additional information
            if result.get('company'):
                company = result['company']
                job_info['company_url'] = company.get('homeurl', '')
                job_info['company_logo'] = company.get('logo', '')
                job_info['company_profile_url'] = company.get('companyprofile_url', '')
            
            # Extract salary and job type from HTML if available
            if result.get('html'):
                html_content = result['html']
                job_info['salary'] = self._extract_salary_from_html(html_content)
                job_info['job_type'] = self._extract_job_type_from_html(html_content)
            
            return job_info
            
        except Exception as e:
            print(f"Error parsing job result: {e}")
            return None
    
    def _extract_description_from_html(self, html_content):
        """Extract job description from HTML content"""
        try:
            if not html_content:
                return ""
            
            # Parse HTML to extract text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up the text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit length
            if len(text) > 500:
                text = text[:500] + "..."
            
            return text
            
        except Exception as e:
            print(f"Error extracting description: {e}")
            return ""
    
    def _extract_salary_from_html(self, html_content):
        """Extract salary information from HTML content"""
        try:
            if not html_content:
                return ""
            
            # Look for salary patterns
            salary_patterns = [
                r'(\d+\.?\d*)\s*(kr|dkk|kroner)',
                r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*(kr|dkk|kroner)',
                r'(løn|salary|compensation)',
                r'(\d+\.?\d*)\s*(kr|dkk|kroner)\s*pr\.?\s*(måned|mnd|time)'
            ]
            
            for pattern in salary_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                if matches:
                    if isinstance(matches[0], tuple):
                        return f"{matches[0][0]} - {matches[0][1]} {matches[0][2].upper()}"
                    else:
                        return f"{matches[0]} {matches[1].upper()}"
            
            return ""
            
        except Exception as e:
            print(f"Error extracting salary: {e}")
            return ""
    
    def _extract_job_type_from_html(self, html_content):
        """Extract job type from HTML content"""
        try:
            if not html_content:
                return ""
            
            # Look for job type patterns
            job_type_patterns = [
                r'\b(fuldtid|full.?time)\b',
                r'\b(deltid|part.?time)\b',
                r'\b(kontrakt|contract)\b',
                r'\b(freelance|freelancer)\b',
                r'\b(praktik|internship)\b',
                r'\b(studiejob|student job)\b',
                r'\b(graduate|trainee)\b'
            ]
            
            for pattern in job_type_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                if matches:
                    return matches[0].title()
            
            return ""
            
        except Exception as e:
            print(f"Error extracting job type: {e}")
            return ""
    
    def _extract_jobs_from_alternative_sources(self, soup, max_jobs):
        """Extract jobs using alternative methods if JSON extraction fails"""
        jobs = []
        
        try:
            # Look for job cards in the HTML
            job_cards = soup.find_all('div', class_='PaidJob')
            
            for card in job_cards[:max_jobs]:
                job_info = self._extract_job_from_card(card)
                if job_info:
                    jobs.append(job_info)
            
            # If no PaidJob cards found, look for other job-related elements
            if not jobs:
                job_elements = soup.find_all('div', class_='jobsearch-result')
                for element in job_elements[:max_jobs]:
                    job_info = self._extract_job_from_element(element)
                    if job_info:
                        jobs.append(job_info)
        
        except Exception as e:
            print(f"Error extracting jobs from alternative sources: {e}")
        
        return jobs
    
    def _extract_job_from_card(self, card):
        """Extract job information from a job card"""
        try:
            job_info = {
                'tid': '',
                'title': '',
                'company': '',
                'location': '',
                'posted_date': '',
                'description': '',
                'url': '',
                'scraped_at': datetime.now().isoformat()
            }
            
            # Extract title
            title_elem = card.find('h4')
            if title_elem:
                job_info['title'] = title_elem.get_text(strip=True)
                
                # Extract URL from title link
                title_link = title_elem.find('a')
                if title_link:
                    job_info['url'] = title_link.get('href', '')
            
            # Extract company
            company_elem = card.find('div', class_='jix-toolbar-top__company')
            if company_elem:
                job_info['company'] = company_elem.get_text(strip=True)
            
            # Extract location
            area_elem = card.find('span', class_='jix_robotjob--area')
            if area_elem:
                job_info['location'] = area_elem.get_text(strip=True)
            
            # Extract posted date
            date_elem = card.find('time')
            if date_elem:
                job_info['posted_date'] = date_elem.get('datetime', '')
            
            # Extract description
            desc_elem = card.find('p')
            if desc_elem:
                job_info['description'] = desc_elem.get_text(strip=True)
            
            return job_info if job_info['title'] else None
            
        except Exception as e:
            print(f"Error extracting job from card: {e}")
            return None
    
    def _extract_job_from_element(self, element):
        """Extract job information from a job element"""
        try:
            job_info = {
                'tid': '',
                'title': '',
                'company': '',
                'location': '',
                'posted_date': '',
                'description': '',
                'url': '',
                'scraped_at': datetime.now().isoformat()
            }
            
            # Extract basic information from the element
            all_text = element.get_text()
            lines = [line.strip() for line in all_text.split('\n') if line.strip()]
            
            if lines:
                job_info['title'] = lines[0][:100]  # First line as title
            
            # Look for links
            links = element.find_all('a')
            for link in links:
                href = link.get('href', '')
                if '/vis-job/' in href or '/job/' in href:
                    job_info['url'] = href
                    break
            
            return job_info if job_info['title'] else None
            
        except Exception as e:
            print(f"Error extracting job from element: {e}")
            return None
    
    def save_to_json(self, filename="real_jobindex_jobs.json"):
        """Save scraped jobs to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, ensure_ascii=False, indent=2)
        print(f"Jobs saved to {filename}")
    
    def save_to_csv(self, filename="real_jobindex_jobs.csv"):
        """Save scraped jobs to CSV file"""
        # Flatten the data for CSV
        flattened_jobs = []
        for job in self.jobs:
            flat_job = {
                'tid': job.get('tid', ''),
                'title': job.get('title', ''),
                'company': job.get('company', ''),
                'company_id': job.get('company_id', ''),
                'location': job.get('location', ''),
                'posted_date': job.get('posted_date', ''),
                'last_date': job.get('last_date', ''),
                'description': job.get('description', ''),
                'url': job.get('url', ''),
                'share_url': job.get('share_url', ''),
                'salary': job.get('salary', ''),
                'job_type': job.get('job_type', ''),
                'is_archived': job.get('is_archived', False),
                'is_local': job.get('is_local', False),
                'scraped_at': job.get('scraped_at', '')
            }
            flattened_jobs.append(flat_job)
        
        df = pd.DataFrame(flattened_jobs)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Jobs saved to {filename}")
    
    def print_summary(self):
        """Print a summary of scraped jobs"""
        print(f"\n=== REAL JOB SCRAPING SUMMARY ===")
        print(f"Total jobs scraped: {len(self.jobs)}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.jobs:
            print(f"\nSample jobs:")
            for i, job in enumerate(self.jobs[:5], 1):
                print(f"{i}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
                print(f"   Location: {job.get('location', 'N/A')}")
                print(f"   Posted: {job.get('posted_date', 'N/A')}")
                print(f"   URL: {job.get('url', 'N/A')}")
                print(f"   TID: {job.get('tid', 'N/A')}")
                print()


def main():
    """Main function to run the scraper"""
    print("Starting Real Jobindex Scraper...")
    
    # Initialize scraper
    scraper = RealJobindexScraper()
    
    # Scrape 10 jobs
    scraper.scrape_jobs(num_jobs=10)
    
    # Save results
    scraper.save_to_json()
    scraper.save_to_csv()
    
    # Print summary
    scraper.print_summary()


if __name__ == "__main__":
    main()



