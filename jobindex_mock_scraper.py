#!/usr/bin/env python3
"""
Jobindex Mock Scraper
Generates realistic Danish job postings for demonstration purposes
"""

import json
import pandas as pd
from datetime import datetime, timedelta
import random


class JobindexMockScraper:
    def __init__(self):
        """Initialize the mock scraper"""
        self.jobs = []
        
        # Danish job titles
        self.job_titles = [
            "Software Developer", "Softwareudvikler", "Programmør", "Systemudvikler",
            "Data Analyst", "Dataanalytiker", "Business Analyst", "Forretningsanalytiker",
            "Marketing Manager", "Marketingchef", "Digital Marketing Specialist", "Digital Marketing Specialist",
            "Sales Representative", "Salgsrepræsentant", "Account Manager", "Account Manager",
            "Project Manager", "Projektleder", "Scrum Master", "Scrum Master",
            "UX Designer", "UX Designer", "UI Designer", "UI Designer",
            "Product Manager", "Produktchef", "Product Owner", "Product Owner",
            "DevOps Engineer", "DevOps Engineer", "System Administrator", "Systemadministrator",
            "Frontend Developer", "Frontend Udvikler", "Backend Developer", "Backend Udvikler",
            "Full Stack Developer", "Full Stack Udvikler", "Mobile Developer", "Mobiludvikler",
            "Data Scientist", "Data Scientist", "Machine Learning Engineer", "Machine Learning Engineer",
            "QA Engineer", "Test Engineer", "Test Engineer", "QA Engineer",
            "Technical Lead", "Tech Lead", "Senior Developer", "Senior Udvikler",
            "Business Development Manager", "Business Development Manager", "Customer Success Manager", "Customer Success Manager",
            "Content Writer", "Indholdsskribent", "SEO Specialist", "SEO Specialist",
            "HR Manager", "HR Chef", "Recruiter", "Rekrutteringskonsulent",
            "Financial Analyst", "Finansanalytiker", "Accountant", "Revisor",
            "Legal Counsel", "Advokat", "Compliance Officer", "Compliance Officer"
        ]
        
        # Danish companies
        self.companies = [
            "Microsoft Danmark", "Google Denmark", "Apple Denmark", "Amazon Denmark",
            "Meta Denmark", "Netflix Denmark", "Spotify Denmark", "Uber Denmark",
            "Airbnb Denmark", "Slack Denmark", "Zoom Denmark", "Salesforce Denmark",
            "Adobe Denmark", "Oracle Denmark", "IBM Denmark", "Intel Denmark",
            "Cisco Denmark", "VMware Denmark", "SAP Denmark", "Siemens Denmark",
            "Philips Denmark", "Novo Nordisk", "Vestas", "Maersk",
            "Carlsberg", "Coloplast", "Chr. Hansen", "Genmab",
            "Lundbeck", "Orsted", "Rockwool", "FLSmidth",
            "ISS", "TDC Group", "Danske Bank", "Nordea",
            "Jyske Bank", "Sydbank", "Arbejdernes Landsbank", "Nykredit",
            "PFA", "ATP", "PensionDanmark", "Sampension",
            "Copenhagen Business School", "Technical University of Denmark", "University of Copenhagen", "Aarhus University"
        ]
        
        # Danish locations
        self.locations = [
            "København", "Aarhus", "Odense", "Aalborg", "Esbjerg", "Randers",
            "Kolding", "Horsens", "Vejle", "Roskilde", "Herning", "Silkeborg",
            "Næstved", "Fredericia", "Viborg", "Køge", "Holstebro", "Taastrup",
            "Slagelse", "Hilleroed", "Albertslund", "Hvidovre", "Horsholm", "Glostrup"
        ]
        
        # Danish job types
        self.job_types = [
            "Fuldtid", "Deltid", "Kontrakt", "Freelance", "Praktik", "Graduate",
            "Full-time", "Part-time", "Contract", "Internship", "Trainee"
        ]
        
        # Danish salary ranges (monthly in DKK)
        self.salary_ranges = [
            "25.000 - 35.000 DKK", "30.000 - 45.000 DKK", "35.000 - 50.000 DKK",
            "40.000 - 60.000 DKK", "45.000 - 70.000 DKK", "50.000 - 80.000 DKK",
            "60.000 - 90.000 DKK", "70.000 - 100.000 DKK", "80.000 - 120.000 DKK",
            "90.000 - 140.000 DKK", "100.000 - 160.000 DKK"
        ]
        
        # Job descriptions
        self.job_descriptions = [
            "Vi søger en erfaren {role} til at styrke vores team. Du vil være ansvarlig for {responsibility} og arbejde tæt sammen med vores kunder og kolleger.",
            "Som {role} hos os får du mulighed for at arbejde med spændende projekter og være med til at forme fremtidens løsninger inden for {field}.",
            "Vi har brug for en {role} der kan hjælpe os med at udvikle og implementere innovative løsninger. Du vil være en del af et dynamisk team med fokus på {focus}.",
            "Som {role} vil du være ansvarlig for {responsibility} og sikre, at vores produkter leverer den bedste brugeroplevelse til vores kunder.",
            "Vi søger en {role} der kan styrke vores {department} team. Du vil arbejde med {technology} og være med til at drive vores digitale transformation fremad.",
            "Som {role} hos os får du mulighed for at arbejde med de nyeste teknologier og være med til at udvikle løsninger der gør en forskel for vores kunder.",
            "Vi har brug for en {role} der kan hjælpe os med at optimere vores processer og implementere bedste praksis inden for {field}.",
            "Som {role} vil du være en del af vores {department} team og arbejde med spændende projekter der har reel indflydelse på vores forretning."
        ]
        
        # Job requirements
        self.job_requirements = [
            "Erfaring med {technology} og {field}",
            "Stærke kommunikationsevner og teamarbejde",
            "Selvstændig og resultatorienteret",
            "Gode analytiske færdigheder",
            "Erfaring med agile metoder",
            "Fleksibilitet og tilpasningsevne",
            "Gode engelske færdigheder",
            "Relevant uddannelse eller erfaring",
            "Kundeorienteret tilgang",
            "Problemløsningsevner og kreativitet"
        ]
        
        # Technologies and fields
        self.technologies = [
            "Python", "Java", "JavaScript", "React", "Angular", "Vue.js",
            "Node.js", "C#", ".NET", "PHP", "Ruby", "Go",
            "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud",
            "SQL", "MongoDB", "PostgreSQL", "Redis", "Elasticsearch",
            "Git", "Jenkins", "Jira", "Confluence", "Slack"
        ]
        
        self.fields = [
            "software development", "web development", "mobile development",
            "data analysis", "machine learning", "artificial intelligence",
            "cloud computing", "cybersecurity", "devops",
            "digital marketing", "e-commerce", "fintech",
            "healthcare", "education", "finance", "logistics"
        ]
        
        self.departments = [
            "Development", "Engineering", "IT", "Digital", "Technology",
            "Marketing", "Sales", "Customer Success", "Product", "Design",
            "Data", "Analytics", "Business Intelligence", "Operations"
        ]
    
    def scrape_jobs(self, num_jobs=10, search_term="", location=""):
        """
        Generate mock job postings
        
        Args:
            num_jobs (int): Number of jobs to generate
            search_term (str): Job search term (not used in mock)
            location (str): Location filter (not used in mock)
        """
        print(f"Generating {num_jobs} realistic Danish job postings...")
        
        for i in range(num_jobs):
            job_data = self._generate_job_posting(i + 1)
            self.jobs.append(job_data)
            print(f"Generated job {i + 1}: {job_data['title']} at {job_data['company']}")
        
        print(f"Successfully generated {len(self.jobs)} job postings")
    
    def _generate_job_posting(self, job_id):
        """Generate a single realistic job posting"""
        # Select random elements
        title = random.choice(self.job_titles)
        company = random.choice(self.companies)
        location = random.choice(self.locations)
        job_type = random.choice(self.job_types)
        salary = random.choice(self.salary_ranges)
        
        # Generate realistic dates
        posted_date = datetime.now() - timedelta(days=random.randint(1, 30))
        
        # Generate description and requirements
        technology = random.choice(self.technologies)
        field = random.choice(self.fields)
        department = random.choice(self.departments)
        
        description_template = random.choice(self.job_descriptions)
        description = description_template.format(
            role=title.lower(),
            responsibility=f"udvikling af {field} løsninger",
            field=field,
            focus=technology,
            technology=technology,
            department=department
        )
        
        requirements_template = random.choice(self.job_requirements)
        requirements = requirements_template.format(
            technology=technology,
            field=field
        )
        
        # Generate realistic URL
        url = f"https://www.jobindex.dk/job/{company.lower().replace(' ', '-')}-{title.lower().replace(' ', '-')}-{job_id}"
        
        job_data = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'job_type': job_type,
            'posted_date': posted_date.strftime('%Y-%m-%d'),
            'description': description,
            'requirements': requirements,
            'url': url,
            'scraped_at': datetime.now().isoformat()
        }
        
        return job_data
    
    def save_to_json(self, filename="jobindex_jobs.json"):
        """Save generated jobs to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, ensure_ascii=False, indent=2)
        print(f"Jobs saved to {filename}")
    
    def save_to_csv(self, filename="jobindex_jobs.csv"):
        """Save generated jobs to CSV file"""
        df = pd.DataFrame(self.jobs)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Jobs saved to {filename}")
    
    def print_summary(self):
        """Print a summary of generated jobs"""
        print(f"\n=== JOB GENERATION SUMMARY ===")
        print(f"Total jobs generated: {len(self.jobs)}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.jobs:
            print(f"\nSample jobs:")
            for i, job in enumerate(self.jobs[:5], 1):
                print(f"{i}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
                print(f"   Location: {job.get('location', 'N/A')}")
                print(f"   Salary: {job.get('salary', 'N/A')}")
                print(f"   Type: {job.get('job_type', 'N/A')}")
                print(f"   Posted: {job.get('posted_date', 'N/A')}")
                print(f"   URL: {job.get('url', 'N/A')}")
                print()
    
    def get_jobs_by_location(self, location):
        """Filter jobs by location"""
        return [job for job in self.jobs if location.lower() in job['location'].lower()]
    
    def get_jobs_by_company(self, company):
        """Filter jobs by company"""
        return [job for job in self.jobs if company.lower() in job['company'].lower()]
    
    def get_jobs_by_type(self, job_type):
        """Filter jobs by type"""
        return [job for job in self.jobs if job_type.lower() in job['job_type'].lower()]


def main():
    """Main function to run the mock scraper"""
    print("Starting Jobindex Mock Scraper...")
    
    # Initialize scraper
    scraper = JobindexMockScraper()
    
    # Generate 10 jobs
    scraper.scrape_jobs(num_jobs=10)
    
    # Save results
    scraper.save_to_json()
    scraper.save_to_csv()
    
    # Print summary
    scraper.print_summary()
    
    # Demonstrate filtering
    print("\n=== FILTERING EXAMPLES ===")
    copenhagen_jobs = scraper.get_jobs_by_location("København")
    print(f"Jobs in København: {len(copenhagen_jobs)}")
    
    tech_jobs = scraper.get_jobs_by_company("Microsoft")
    print(f"Jobs at Microsoft: {len(tech_jobs)}")
    
    fulltime_jobs = scraper.get_jobs_by_type("Fuldtid")
    print(f"Full-time jobs: {len(fulltime_jobs)}")


if __name__ == "__main__":
    main()



