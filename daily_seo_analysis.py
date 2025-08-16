#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
import time
import json
import snowflake.connector
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daily_analysis_log.txt'),
        logging.StreamHandler()
    ]
)

class DailySEOAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def check_google_ranking(self, search_query="snowflake consultants copenhagen"):
        """Check Devoteam's Google ranking for the search query"""
        logging.info(f"Checking Google ranking for: {search_query}")
        
        url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            devoteam_position = "Not found in top results"
            
            # Look for Devoteam's specific URL
            devoteam_link = "https://www.devoteam.com/snowflake-elite-partner/"
            all_links = soup.find_all('a', href=True)
            
            for i, link in enumerate(all_links):
                href = link.get('href', '')
                if devoteam_link in href:
                    devoteam_position = i + 1
                    logging.info(f"Found Devoteam at position: {devoteam_position}")
                    break
            
            return {
                'search_query': search_query,
                'position': devoteam_position,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error checking Google ranking: {e}")
            return {
                'search_query': search_query,
                'position': "Error",
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def analyze_page_seo(self, url):
        """Analyze SEO metrics for a specific page"""
        logging.info(f"Analyzing SEO for: {url}")
        
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=10)
            load_time = time.time() - start_time
            
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text().lower()
            
            # Local SEO analysis
            copenhagen_mentions = len(re.findall(r'copenhagen|københavn', text))
            denmark_mentions = len(re.findall(r'denmark|danmark', text))
            danish_mentions = len(re.findall(r'danish|dansk', text))
            
            # Content analysis
            words = text.split()
            snowflake_keywords = sum(1 for word in words if 'snowflake' in word.lower())
            
            # Technical SEO
            title = soup.find('title')
            title_length = len(title.get_text()) if title else 0
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            meta_desc_length = len(meta_desc.get('content', '')) if meta_desc else 0
            
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            canonical_present = bool(canonical)
            
            # User experience
            images = soup.find_all('img')
            alt_text_count = sum(1 for img in images if img.get('alt'))
            alt_text_coverage = (alt_text_count / len(images) * 100) if images else 0
            
            cta_patterns = ['contact', 'get started', 'request', 'consultation', 'free', 'quote']
            cta_count = sum(1 for link in soup.find_all('a') 
                           if any(pattern in link.get_text().lower() for pattern in cta_patterns))
            
            forms = soup.find_all('form')
            forms_count = len(forms)
            
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            headings_count = len(headings)
            
            # Contact information
            phone_patterns = [
                r'\b\d{2}\s\d{2}\s\d{2}\s\d{2}\b',
                r'\b\d{4}\s\d{4}\b',
                r'\+45\s\d{2}\s\d{2}\s\d{2}\s\d{2}'
            ]
            contact_info_present = any(re.search(pattern, text) for pattern in phone_patterns)
            
            address_found = bool(re.search(r'copenhagen|københavn.*\d{4}', text))
            danish_phone_found = bool(re.search(r'\+45', text))
            
            # Calculate scores
            local_seo_score = self.calculate_local_seo_score(
                copenhagen_mentions, denmark_mentions, contact_info_present, address_found
            )
            
            content_score = self.calculate_content_score(
                len(words), headings_count, snowflake_keywords
            )
            
            technical_score = self.calculate_technical_score(
                title_length, meta_desc_length, canonical_present
            )
            
            ux_score = self.calculate_ux_score(
                alt_text_coverage, cta_count, forms_count
            )
            
            overall_score = (local_seo_score + content_score + technical_score + ux_score) / 4
            
            return {
                'url': url,
                'page_title': title.get_text() if title else 'No title',
                'load_time': load_time,
                'content_size': len(response.content),
                'local_seo_score': local_seo_score,
                'content_quality_score': content_score,
                'technical_seo_score': technical_score,
                'user_experience_score': ux_score,
                'overall_score': overall_score,
                'copenhagen_mentions': copenhagen_mentions,
                'denmark_mentions': denmark_mentions,
                'danish_mentions': danish_mentions,
                'snowflake_keyword_count': snowflake_keywords,
                'contact_info_present': contact_info_present,
                'local_address_present': address_found,
                'danish_phone_present': danish_phone_found,
                'alt_text_coverage_percentage': alt_text_coverage,
                'cta_count': cta_count,
                'forms_count': forms_count,
                'headings_count': headings_count,
                'images_count': len(images),
                'meta_description_length': meta_desc_length,
                'title_length': title_length,
                'canonical_url_present': canonical_present,
                'schema_markup_count': len(soup.find_all(attrs={'itemtype': True})),
                'structured_data_count': len(soup.find_all('script', type='application/ld+json')),
                'social_tags_count': len(soup.find_all('meta', attrs={'property': re.compile(r'^og:', re.I)})) + 
                                   len(soup.find_all('meta', attrs={'name': re.compile(r'^twitter:', re.I)})),
                'improvement_priority': self.get_improvement_priority(overall_score, local_seo_score),
                'notes': self.generate_notes(copenhagen_mentions, contact_info_present, alt_text_coverage)
            }
            
        except Exception as e:
            logging.error(f"Error analyzing {url}: {e}")
            return {
                'url': url,
                'error': str(e),
                'overall_score': 0,
                'local_seo_score': 0,
                'content_quality_score': 0,
                'technical_seo_score': 0,
                'user_experience_score': 0
            }
    
    def calculate_local_seo_score(self, copenhagen_mentions, denmark_mentions, contact_info, address):
        """Calculate local SEO score"""
        score = 1.0  # Base score
        
        if copenhagen_mentions > 0:
            score += 0.5
        if denmark_mentions > 0:
            score += 0.5
        if contact_info:
            score += 0.5
        if address:
            score += 0.5
            
        return min(score, 3.0)
    
    def calculate_content_score(self, word_count, headings_count, snowflake_keywords):
        """Calculate content quality score"""
        score = 1.0
        
        if word_count > 500:
            score += 0.5
        if headings_count >= 3:
            score += 0.5
        if snowflake_keywords > 0:
            score += 0.5
        if word_count > 1000:
            score += 0.5
            
        return min(score, 3.0)
    
    def calculate_technical_score(self, title_length, meta_desc_length, canonical_present):
        """Calculate technical SEO score"""
        score = 1.0
        
        if title_length > 10:
            score += 0.5
        if meta_desc_length > 50:
            score += 0.5
        if canonical_present:
            score += 0.5
        if title_length > 30 and title_length < 60:
            score += 0.5
            
        return min(score, 3.0)
    
    def calculate_ux_score(self, alt_text_coverage, cta_count, forms_count):
        """Calculate user experience score"""
        score = 1.0
        
        if alt_text_coverage > 80:
            score += 0.5
        if cta_count >= 3:
            score += 0.5
        if forms_count > 0:
            score += 0.5
        if alt_text_coverage > 50:
            score += 0.5
            
        return min(score, 3.0)
    
    def get_improvement_priority(self, overall_score, local_seo_score):
        """Determine improvement priority"""
        if local_seo_score < 2.0:
            return "HIGH - Local SEO optimization needed"
        elif overall_score < 2.5:
            return "MEDIUM - General SEO improvements needed"
        else:
            return "LOW - Minor optimizations"
    
    def generate_notes(self, copenhagen_mentions, contact_info, alt_text_coverage):
        """Generate improvement notes"""
        notes = []
        if copenhagen_mentions == 0:
            notes.append("No Copenhagen mentions found")
        if not contact_info:
            notes.append("Missing local contact information")
        if alt_text_coverage < 80:
            notes.append(f"Low alt text coverage ({alt_text_coverage:.1f}%)")
        
        return "; ".join(notes) if notes else "All areas look good"

def upload_to_snowflake(data):
    """Upload analysis data to Snowflake"""
    try:
        from snowflake_config import get_snowflake_config
        config = get_snowflake_config()
        
        conn = snowflake.connector.connect(
            user=config['user'],
            password=config['password'],
            account=config['account'],
            warehouse=config['warehouse'],
            database=config['database'],
            schema=config['schema']
        )
        
        cursor = conn.cursor()
        
        # Insert ranking data
        if 'ranking' in data:
            ranking = data['ranking']
            
            # Handle ranking position properly
            position = ranking.get('position')
            if isinstance(position, str) and ('Not found' in position or 'Error' in position):
                position = None
            elif isinstance(position, str) and position.isdigit():
                position = int(position)
            
            cursor.execute("""
            INSERT INTO SEOdevoteamdatadriven (
                page_url, page_title, google_ranking_position, search_query,
                local_seo_score, content_quality_score, technical_seo_score, user_experience_score, overall_score,
                copenhagen_mentions, denmark_mentions, danish_mentions, snowflake_keyword_count,
                contact_info_present, local_address_present, danish_phone_present,
                alt_text_coverage_percentage, cta_count, forms_count, headings_count, images_count,
                meta_description_length, title_length, canonical_url_present,
                schema_markup_count, structured_data_count, social_tags_count,
                load_time_seconds, content_size_bytes, improvement_priority, notes
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """, (
                'https://www.devoteam.com/snowflake-elite-partner/',  # Use the main page URL
                'Snowflake Elite Partner: Data & AI | Devoteam',  # Use the main page title
                position,
                ranking.get('search_query', ''),
                0,  # Default scores for ranking entry
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                False,
                False,
                False,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                False,
                0,
                0,
                0,
                0,
                0,
                'Daily ranking check',
                f"Google ranking check for {ranking.get('search_query', '')}"
            ))
        
        # Insert page analysis data
        for page_data in data.get('pages', []):
            cursor.execute("""
            INSERT INTO SEOdevoteamdatadriven (
                page_url, page_title, google_ranking_position, search_query,
                local_seo_score, content_quality_score, technical_seo_score, user_experience_score, overall_score,
                copenhagen_mentions, denmark_mentions, danish_mentions, snowflake_keyword_count,
                contact_info_present, local_address_present, danish_phone_present,
                alt_text_coverage_percentage, cta_count, forms_count, headings_count, images_count,
                meta_description_length, title_length, canonical_url_present,
                schema_markup_count, structured_data_count, social_tags_count,
                load_time_seconds, content_size_bytes, improvement_priority, notes
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """, (
                page_data.get('url', ''),
                page_data.get('page_title', ''),
                None,  # No ranking position for individual pages
                'snowflake consultants copenhagen',
                page_data.get('local_seo_score', 0),
                page_data.get('content_quality_score', 0),
                page_data.get('technical_seo_score', 0),
                page_data.get('user_experience_score', 0),
                page_data.get('overall_score', 0),
                page_data.get('copenhagen_mentions', 0),
                page_data.get('denmark_mentions', 0),
                page_data.get('danish_mentions', 0),
                page_data.get('snowflake_keyword_count', 0),
                page_data.get('contact_info_present', False),
                page_data.get('local_address_present', False),
                page_data.get('danish_phone_present', False),
                page_data.get('alt_text_coverage_percentage', 0),
                page_data.get('cta_count', 0),
                page_data.get('forms_count', 0),
                page_data.get('headings_count', 0),
                page_data.get('images_count', 0),
                page_data.get('meta_description_length', 0),
                page_data.get('title_length', 0),
                page_data.get('canonical_url_present', False),
                page_data.get('schema_markup_count', 0),
                page_data.get('structured_data_count', 0),
                page_data.get('social_tags_count', 0),
                page_data.get('load_time', 0),
                page_data.get('content_size', 0),
                page_data.get('improvement_priority', ''),
                page_data.get('notes', '')
            ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logging.info("✅ Data uploaded to Snowflake successfully")
        
    except Exception as e:
        logging.error(f"❌ Error uploading to Snowflake: {e}")

def main():
    """Main function to run daily SEO analysis"""
    logging.info("🚀 Starting daily SEO analysis...")
    
    analyzer = DailySEOAnalyzer()
    
    # Analyze Google ranking
    ranking_data = analyzer.check_google_ranking()
    
    # Analyze key pages
    pages_to_analyze = [
        "https://www.devoteam.com/snowflake-elite-partner/",
        "https://www.devoteam.com/",
        "https://www.devoteam.com/contact/"
    ]
    
    page_analyses = []
    for page_url in pages_to_analyze:
        page_data = analyzer.analyze_page_seo(page_url)
        page_analyses.append(page_data)
        time.sleep(2)  # Be respectful to servers
    
    # Combine all data
    analysis_data = {
        'timestamp': datetime.now().isoformat(),
        'ranking': ranking_data,
        'pages': page_analyses
    }
    
    # Save results to file
    with open('seo_analysis_results.json', 'w') as f:
        json.dump(analysis_data, f, indent=2)
    
    logging.info("📄 Analysis results saved to seo_analysis_results.json")
    
    # Upload to Snowflake
    upload_to_snowflake(analysis_data)
    
    logging.info("🎉 Daily SEO analysis completed successfully!")

if __name__ == "__main__":
    main()
