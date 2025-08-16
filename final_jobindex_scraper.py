#!/usr/bin/env python3
"""
Final Jobindex Scraper
Extracts actual job postings from Jobindex.dk by parsing embedded JSON data
"""

import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re


class FinalJobindexScraper:
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
    
    def _fetch_job_details(self, job_url):
        """Fetch detailed job information from individual job URL"""
        try:
            response = self.session.get(job_url, headers=self.session.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for contact information in the detailed job description
                job_text = soup.get_text()
                
                # Enhanced email patterns for detailed descriptions
                email_patterns = [
                    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                    r'(email|e-mail|mail):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(kontakt|contact):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(ansøg|apply|application):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(hr|personal|recruitment):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(send|email|mail)\s+til\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(kontakt|contact)\s+os\s+på\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(spørgsmål|questions):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(yderligere|further)\s+information:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(for\s+mere\s+info|for\s+more\s+info):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(ansøgningsfrist|deadline):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(søg\s+jobbet|apply\s+for\s+position):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(kontaktperson|contact person|ansøgningsansvarlig):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(manager|leder|chef):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(ansøg til|apply to|send ansøgning til):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                    r'(jobansøgning|job application):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
                ]
                
                for pattern in email_patterns:
                    matches = re.findall(pattern, job_text, re.IGNORECASE)
                    if matches:
                        for match in matches:
                            if isinstance(match, tuple):
                                for part in match:
                                    if '@' in part:
                                        return part.strip()
                            else:
                                if '@' in match:
                                    return match.strip()
                
                return ""
            else:
                return ""
        except Exception as e:
            print(f"Error fetching job details: {e}")
            return ""

    def scrape_jobs_with_detailed_contact_search(self, num_jobs=20):
        """Scrape jobs and search for contact info in detailed descriptions"""
        print(f"Starting detailed contact search for {num_jobs} jobs...")
        
        # First get the basic job list
        self.scrape_jobs(num_jobs, "")
        
        # Now fetch detailed information for each job
        jobs_with_emails = []
        
        for i, job in enumerate(self.jobs[:num_jobs], 1):
            print(f"Checking job {i}/{num_jobs}: {job.get('title', 'Unknown')}")
            
            job_url = job.get('url', '')
            if job_url:
                # Fetch detailed job description
                contact_email = self._fetch_job_details(job_url)
                if contact_email:
                    job['contact_email'] = contact_email
                    jobs_with_emails.append(job)
                    print(f"  ✅ Found email: {contact_email}")
                else:
                    print(f"  ❌ No email found")
            
            # Small delay to be respectful
            time.sleep(1)
        
        print(f"Found {len(jobs_with_emails)} jobs with contact emails in detailed descriptions")
        return jobs_with_emails

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
                            print(f"Scraped job {jobs_scraped}: {job.get('title', 'Unknown')} at {job.get('company', 'Unknown')}")
                    
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
            # Handle case where result might be a string
            if isinstance(result, str):
                return None
            
            job_info = {
                'tid': result.get('tid', ''),
                'title': result.get('headline', ''),
                'company': result.get('company', {}).get('name', '') if isinstance(result.get('company'), dict) else '',
                'company_id': result.get('company', {}).get('id', '') if isinstance(result.get('company'), dict) else '',
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
            if result.get('company') and isinstance(result['company'], dict):
                company = result['company']
                job_info['company_url'] = company.get('homeurl', '')
                job_info['company_logo'] = company.get('logo', '')
                job_info['company_profile_url'] = company.get('companyprofile_url', '')
            
            # Extract salary, job type, and contact info from HTML if available
            if result.get('html'):
                html_content = result['html']
                job_info['salary'] = self._extract_salary_from_html(html_content)
                job_info['job_type'] = self._extract_job_type_from_html(html_content)
                job_info['contact_person'] = self._extract_contact_person_from_html(html_content)
                job_info['contact_email'] = self._extract_contact_email_from_html(html_content)
            
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
    
    def _extract_contact_person_from_html(self, html_content):
        """Extract contact person from HTML content"""
        try:
            if not html_content:
                return ""
            
            # Parse HTML to extract text
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text()
            
            # Look for contact person patterns
            contact_patterns = [
                r'(kontakt|contact|ansøg|apply|application):\s*([A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+)',
                r'(kontaktperson|contact person|ansøgningsansvarlig):\s*([A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+)',
                r'(hr|personal|recruitment|talent):\s*([A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+)',
                r'(manager|leder|chef):\s*([A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+)',
                r'(for yderligere information|for more information|spørgsmål|questions):\s*([A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+)',
                r'(kontakt|contact)\s+([A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+)',
                r'([A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+)\s+(kontakt|contact|hr|personal)',
                r'(ansøg til|apply to|send ansøgning til):\s*([A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+)',
                r'(søg jobbet|apply for this position):\s*([A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+)',
                r'(jobansøgning|job application):\s*([A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+)'
            ]
            
            for pattern in contact_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    for match in matches:
                        if isinstance(match, tuple):
                            # Return the name part from tuple
                            for part in match:
                                if re.match(r'^[A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+$', part):
                                    return part.strip()
                        else:
                            # Single match
                            if re.match(r'^[A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+$', match):
                                return match.strip()
            
            # Look for email patterns that might indicate a contact person
            email_pattern = r'([a-zA-Z0-9._%+-]+)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            email_matches = re.findall(email_pattern, text)
            for email in email_matches:
                # If email looks like a name (contains dots or underscores)
                if '.' in email or '_' in email:
                    # Try to extract name from email
                    name_part = email.split('@')[0]
                    if '.' in name_part:
                        name_parts = name_part.split('.')
                        if len(name_parts) >= 2:
                            # Convert to proper name format
                            first_name = name_parts[0].capitalize()
                            last_name = name_parts[1].capitalize()
                            return f"{first_name} {last_name}"
            
            return ""
            
        except Exception as e:
            print(f"Error extracting contact person: {e}")
            return ""
    
    def _extract_contact_email_from_html(self, html_content):
        """Extract contact email from HTML content - enhanced version"""
        try:
            if not html_content:
                return ""
            
            # Parse HTML to extract text and links
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Look for email links first
            email_links = soup.find_all('a', href=re.compile(r'^mailto:'))
            for link in email_links:
                email = link.get('href', '').replace('mailto:', '')
                if '@' in email:
                    return email.strip()
            
            # Look for email patterns in text - more comprehensive patterns
            email_patterns = [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(email|e-mail|mail):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(kontakt|contact):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(ansøg|apply|application):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(hr|personal|recruitment):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(send|email|mail)\s+til\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(send|email|mail)\s+to\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(kontakt|contact)\s+os\s+på\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(kontakt|contact)\s+us\s+at\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(spørgsmål|questions):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(yderligere|further)\s+information:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(for\s+mere\s+info|for\s+more\s+info):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(ansøgningsfrist|deadline):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'(søg\s+jobbet|apply\s+for\s+position):\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            ]
            
            text = soup.get_text()
            for pattern in email_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    for match in matches:
                        if isinstance(match, tuple):
                            # Return the email part from tuple
                            for part in match:
                                if '@' in part:
                                    return part.strip()
                        else:
                            # Single match
                            if '@' in match:
                                return match.strip()
            
            # Look for email in href attributes
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '')
                if '@' in href and 'mailto:' not in href:
                    # Extract email from href
                    email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', href)
                    if email_match:
                        return email_match.group(1)
            
            # Look for company contact emails in the text
            company_email_patterns = [
                r'(info|kontakt|contact|hr|jobs|careers|recruitment|ansøg|apply)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                r'[a-zA-Z0-9._%+-]+@(company|firma|virksomhed|corp|inc|as|aps|a\/s)\.[a-zA-Z]{2,}',
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(dk|com|net|org|eu)',
                r'(firstname|lastname|name)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                r'([a-zA-Z]+)\.([a-zA-Z]+)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            ]
            
            for pattern in company_email_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    for match in matches:
                        if isinstance(match, tuple):
                            # Combine tuple parts
                            email = ''.join(match) + '@' + match[0] if len(match) >= 2 else match[0]
                        else:
                            email = match
                        if '@' in email:
                            return email.strip()
            
            # Look for emails in any script tags or data attributes
            scripts = soup.find_all('script')
            for script in scripts:
                script_text = script.get_text()
                email_matches = re.findall(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', script_text)
                if email_matches:
                    return email_matches[0].strip()
            
            # Look for emails in data attributes
            elements_with_data = soup.find_all(attrs={"data-email": True})
            for element in elements_with_data:
                email = element.get('data-email')
                if email and '@' in email:
                    return email.strip()
            
            return ""
            
        except Exception as e:
            print(f"Error extracting contact email: {e}")
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
                'contact_person': '',
                'contact_email': '',
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
            
            # Extract contact info from card HTML
            card_html = str(card)
            job_info['contact_person'] = self._extract_contact_person_from_html(card_html)
            job_info['contact_email'] = self._extract_contact_email_from_html(card_html)
            
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
                'contact_person': '',
                'contact_email': '',
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
            
            # Extract contact info from element HTML
            element_html = str(element)
            job_info['contact_person'] = self._extract_contact_person_from_html(element_html)
            job_info['contact_email'] = self._extract_contact_email_from_html(element_html)
            
            return job_info if job_info['title'] else None
            
        except Exception as e:
            print(f"Error extracting job from element: {e}")
            return None
    
    def save_to_json(self, filename="final_jobindex_jobs.json"):
        """Save scraped jobs to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, ensure_ascii=False, indent=2)
        print(f"Jobs saved to {filename}")
    
    def save_to_csv(self, filename="final_jobindex_jobs.csv"):
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
                'contact_person': job.get('contact_person', ''),
                'contact_email': job.get('contact_email', ''),
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
        print(f"\n=== FINAL JOB SCRAPING SUMMARY ===")
        print(f"Total jobs scraped: {len(self.jobs)}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.jobs:
            print(f"\nSample jobs:")
            for i, job in enumerate(self.jobs[:5], 1):
                print(f"{i}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
                print(f"   Location: {job.get('location', 'N/A')}")
                print(f"   Posted: {job.get('posted_date', 'N/A')}")
                print(f"   Contact: {job.get('contact_person', 'N/A')}")
                print(f"   Email: {job.get('contact_email', 'N/A')}")
                print(f"   URL: {job.get('url', 'N/A')}")
                print(f"   TID: {job.get('tid', 'N/A')}")
                print()


def main():
    """Main function to run the scraper"""
    print("Starting Comprehensive Jobindex Scraper for ALL Jobs with 'data' and Contact Emails...")
    
    # Initialize scraper
    scraper = FinalJobindexScraper()
    
    # Scrape jobs with "data" in the search term - no artificial limits
    print("Scraping jobs with 'data' keyword (comprehensive search)...")
    scraper.scrape_jobs(num_jobs=500, search_term="data")  # Increased limit
    
    # Also try related data terms - no artificial limits
    data_terms = ["data analyst", "data scientist", "data engineer", "data science", "data analytics", "data processing", "data management", "data visualization", "data mining", "data warehouse", "dataanalytiker", "datascientist", "dataengineer"]
    
    for term in data_terms:
        print(f"Scraping jobs with search term: {term} (comprehensive search)")
        scraper.scrape_jobs(num_jobs=200, search_term=term)  # Increased limit
    
    # Remove duplicates based on TID
    unique_jobs = {}
    for job in scraper.jobs:
        tid = job.get('tid', '')
        if tid and tid not in unique_jobs:
            unique_jobs[tid] = job
    
    print(f"Total unique jobs scraped: {len(unique_jobs)}")
    
    # Filter for jobs that contain "data" anywhere in title or description (case insensitive)
    data_jobs = []
    for job in unique_jobs.values():
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        
        # Look for "data" anywhere in the text (including compound words)
        if 'data' in title or 'data' in description:
            data_jobs.append(job)
    
    print(f"Found {len(data_jobs)} jobs containing 'data' keyword (including compound words)")
    
    # Now fetch detailed information for ALL data jobs to find contact emails
    jobs_with_emails = []
    
    print(f"Checking {len(data_jobs)} data jobs for contact emails...")
    
    for i, job in enumerate(data_jobs, 1):
        print(f"Checking data job {i}/{len(data_jobs)}: {job.get('title', 'Unknown')}")
        
        job_url = job.get('url', '')
        if job_url:
            # Fetch detailed job description
            contact_email = scraper._fetch_job_details(job_url)
            if contact_email:
                job['contact_email'] = contact_email
                jobs_with_emails.append(job)
                print(f"  ✅ Found email: {contact_email}")
            else:
                print(f"  ❌ No email found")
        
        # Small delay to be respectful
        time.sleep(0.5)  # Reduced delay for faster processing
    
    # Update scraper jobs to only include data jobs with emails
    scraper.jobs = jobs_with_emails
    
    # Save results
    scraper.save_to_json()
    scraper.save_to_csv()
    
    # Print summary
    scraper.print_summary()
    
    # Print jobs with contact info
    jobs_with_names = [job for job in scraper.jobs if job.get('contact_person')]
    
    print(f"\n=== COMPREHENSIVE DATA JOBS WITH CONTACT EMAILS SUMMARY ===")
    print(f"Total unique jobs scraped: {len(unique_jobs)}")
    print(f"Total data jobs found: {len(data_jobs)}")
    print(f"Data jobs with contact emails: {len(jobs_with_emails)}")
    print(f"Data jobs with contact names: {len(jobs_with_names)}")
    print(f"Success rate: {len(jobs_with_emails)/len(data_jobs)*100:.1f}% of data jobs have contact emails")
    
    if jobs_with_emails:
        print(f"\n=== DATA JOBS WITH CONTACT EMAILS ({len(jobs_with_emails)}) ===")
        for i, job in enumerate(jobs_with_emails, 1):
            print(f"{i}. {job.get('title')} at {job.get('company')}")
            print(f"   Location: {job.get('location')}")
            print(f"   Contact Email: {job.get('contact_email')}")
            print(f"   Contact Person: {job.get('contact_person', 'N/A')}")
            print(f"   URL: {job.get('url', 'N/A')}")
            print()
    else:
        print(f"\n=== NOTE: No data jobs with public contact emails found ===")
        print("This might indicate that data jobs don't typically include contact information.")
        print("You can contact companies directly through their websites or the job application links.")
    
    print(f"\n=== ANALYSIS ===")
    print("The scraper has performed a comprehensive search through data-related job postings.")
    print("This includes compound words like 'dataanalytiker', 'datascientist', etc.")
    print("Contact information is sometimes embedded in job descriptions or application links.")
    print("All scraped jobs have been saved to final_jobindex_jobs.csv for further analysis.")


if __name__ == "__main__":
    main()
