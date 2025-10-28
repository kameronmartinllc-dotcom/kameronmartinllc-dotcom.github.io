#!/usr/bin/env python3
"""
Medical Research Scraper for Type 1 Diabetes
Automatically scrapes PubMed, ClinicalTrials.gov, and medical journals
Updates the Breaking News section with latest developments
"""

import requests
import json
import re
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MedicalScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.t1d_keywords = [
            'type 1 diabetes', 'T1D', 'insulin-dependent diabetes', 'juvenile diabetes',
            'beta cell', 'autoimmune diabetes', 'diabetic ketoacidosis', 'insulin therapy',
            'glucose monitoring', 'closed-loop', 'artificial pancreas', 'islet transplantation',
            'stem cell diabetes', 'immunotherapy diabetes', 'diabetes cure', 'diabetes prevention'
        ]
        
    def scrape_pubmed(self, days_back: int = 7) -> List[Dict]:
        """Scrape recent PubMed articles related to Type 1 Diabetes"""
        logger.info("Scraping PubMed for recent T1D publications...")
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # PubMed search query for recent T1D articles
        start_date_str = start_date.strftime("%Y/%m/%d")
        end_date_str = end_date.strftime("%Y/%m/%d")
        query = f'("type 1 diabetes"[Title/Abstract] OR "T1D"[Title/Abstract] OR "insulin-dependent diabetes"[Title/Abstract]) AND ("{start_date_str}"[PDAT] : "{end_date_str}"[PDAT])'
        
        articles = []
        try:
            # Use PubMed's E-utilities API (free, no authentication required)
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
            
            # Search for articles
            search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmax=50&sort=relevance"
            response = self.session.get(search_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                pmids = [pmid.text for pmid in soup.find_all('Id')]
                
                logger.info(f"Found {len(pmids)} articles from PubMed")
                
                # Get detailed information for each article
                for pmid in pmids[:10]:  # Limit to top 10 most relevant
                    article_data = self._get_pubmed_article_details(pmid)
                    if article_data and self._is_relevant_t1d_article(article_data):
                        articles.append(article_data)
                        time.sleep(0.5)  # Be respectful to PubMed servers
                        
        except Exception as e:
            logger.error(f"Error scraping PubMed: {e}")
            
        return articles
    
    def _get_pubmed_article_details(self, pmid: str) -> Optional[Dict]:
        """Get detailed information for a specific PubMed article"""
        try:
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
            fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
            
            response = self.session.get(fetch_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                
                # Extract article details
                article = soup.find('PubmedArticle')
                if not article:
                    return None
                    
                title = article.find('ArticleTitle')
                title = title.text if title else "No title available"
                
                abstract = article.find('AbstractText')
                abstract = abstract.text if abstract else "No abstract available"
                
                authors = article.find_all('Author')
                author_list = []
                for author in authors[:3]:  # Limit to first 3 authors
                    last_name = author.find('LastName')
                    first_name = author.find('ForeName')
                    if last_name:
                        name = last_name.text
                        if first_name:
                            name = f"{first_name.text} {name}"
                        author_list.append(name)
                
                journal = article.find('Journal')
                journal_title = "Unknown Journal"
                if journal:
                    title_elem = journal.find('Title')
                    if title_elem:
                        journal_title = title_elem.text
                
                pub_date = article.find('PubDate')
                date_str = "Unknown Date"
                if pub_date:
                    year = pub_date.find('Year')
                    month = pub_date.find('Month')
                    day = pub_date.find('Day')
                    if year:
                        date_str = year.text
                        if month:
                            date_str = f"{month.text} {date_str}"
                        if day:
                            date_str = f"{day.text} {date_str}"
                
                return {
                    'pmid': pmid,
                    'title': title,
                    'abstract': abstract,
                    'authors': author_list,
                    'journal': journal_title,
                    'date': date_str,
                    'source': 'PubMed',
                    'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                }
                
        except Exception as e:
            logger.error(f"Error fetching article details for PMID {pmid}: {e}")
            
        return None
    
    def scrape_clinical_trials(self, days_back: int = 7) -> List[Dict]:
        """Scrape recent clinical trials from ClinicalTrials.gov"""
        logger.info("Scraping ClinicalTrials.gov for recent T1D trials...")
        
        trials = []
        try:
            # ClinicalTrials.gov search for T1D trials
            search_url = "https://clinicaltrials.gov/api/v2/studies"
            params = {
                'query.cond': 'Type 1 Diabetes',
                'filter.overallStatus': 'RECRUITING',
                'pageSize': 20,
                'sort': 'LastUpdatePostDate:desc'
            }
            
            response = self.session.get(search_url, params=params)
            if response.status_code == 200:
                data = response.json()
                
                for study in data.get('studies', [])[:10]:  # Limit to top 10
                    trial_data = self._process_clinical_trial(study)
                    if trial_data:
                        trials.append(trial_data)
                        
        except Exception as e:
            logger.error(f"Error scraping ClinicalTrials.gov: {e}")
            
        return trials
    
    def _process_clinical_trial(self, study: Dict) -> Optional[Dict]:
        """Process a clinical trial study into our format"""
        try:
            protocol_section = study.get('protocolSection', {})
            identification_module = protocol_section.get('identificationModule', {})
            status_module = protocol_section.get('statusModule', {})
            design_module = protocol_section.get('designModule', {})
            
            nct_id = identification_module.get('nctId', 'Unknown')
            title = identification_module.get('briefTitle', 'No title available')
            official_title = identification_module.get('officialTitle', title)
            
            # Get status and phase
            overall_status = status_module.get('overallStatus', 'Unknown')
            phase = design_module.get('phases', ['Unknown'])[0] if design_module.get('phases') else 'Unknown'
            
            # Get start date
            start_date = status_module.get('startDateStruct', {}).get('date', 'Unknown')
            
            # Determine priority based on phase and status
            priority = 'MEDIUM'
            if phase in ['PHASE2', 'PHASE3'] and overall_status == 'RECRUITING':
                priority = 'HIGH'
            elif phase == 'PHASE1' and overall_status == 'RECRUITING':
                priority = 'MEDIUM'
            
            return {
                'nct_id': nct_id,
                'title': official_title,
                'phase': phase,
                'status': overall_status,
                'start_date': start_date,
                'priority': priority,
                'source': 'ClinicalTrials.gov',
                'url': f"https://clinicaltrials.gov/study/{nct_id}"
            }
            
        except Exception as e:
            logger.error(f"Error processing clinical trial: {e}")
            return None
    
    def scrape_medical_journals(self) -> List[Dict]:
        """Scrape medical journals for T1D news (using RSS feeds and web scraping)"""
        logger.info("Scraping medical journals for T1D news...")
        
        articles = []
        
        # List of medical journal RSS feeds and websites
        sources = [
            {
                'name': 'Diabetes Care',
                'url': 'https://diabetesjournals.org/care/rss',
                'type': 'rss'
            },
            {
                'name': 'Nature Medicine',
                'url': 'https://www.nature.com/nm.rss',
                'type': 'rss'
            },
            {
                'name': 'JAMA',
                'url': 'https://jamanetwork.com/rss/site_1/1.xml',
                'type': 'rss'
            }
        ]
        
        for source in sources:
            try:
                if source['type'] == 'rss':
                    rss_articles = self._scrape_rss_feed(source['url'], source['name'])
                    articles.extend(rss_articles)
                time.sleep(1)  # Be respectful to servers
            except Exception as e:
                logger.error(f"Error scraping {source['name']}: {e}")
                
        return articles
    
    def _scrape_rss_feed(self, url: str, source_name: str) -> List[Dict]:
        """Scrape RSS feed for T1D related articles"""
        articles = []
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                
                for item in soup.find_all('item')[:5]:  # Limit to 5 per source
                    title = item.find('title')
                    title = title.text if title else "No title"
                    
                    description = item.find('description')
                    description = description.text if description else "No description"
                    
                    link = item.find('link')
                    link = link.text if link else "#"
                    
                    pub_date = item.find('pubDate')
                    pub_date = pub_date.text if pub_date else "Unknown date"
                    
                    # Check if article is T1D related
                    if self._is_relevant_t1d_article({'title': title, 'abstract': description}):
                        articles.append({
                            'title': title,
                            'abstract': description,
                            'date': pub_date,
                            'source': source_name,
                            'url': link,
                            'authors': [],
                            'journal': source_name
                        })
                        
        except Exception as e:
            logger.error(f"Error scraping RSS feed {url}: {e}")
            
        return articles
    
    def _is_relevant_t1d_article(self, article: Dict) -> bool:
        """Check if an article is relevant to Type 1 Diabetes"""
        text_to_check = f"{article.get('title', '')} {article.get('abstract', '')}".lower()
        
        # Check for T1D keywords
        keyword_matches = sum(1 for keyword in self.t1d_keywords if keyword.lower() in text_to_check)
        
        # Must have at least 2 T1D-related keywords
        return keyword_matches >= 2
    
    def generate_breaking_news_item(self, article: Dict) -> Dict:
        """Convert scraped article into breaking news format"""
        # Determine badge based on source and content
        badge = "NEW"
        if article.get('source') == 'ClinicalTrials.gov':
            if article.get('priority') == 'HIGH':
                badge = "HOT"
            else:
                badge = "TRIAL"
        elif 'breakthrough' in article.get('title', '').lower() or 'revolutionary' in article.get('title', '').lower():
            badge = "BREAKTHROUGH"
        elif 'fda' in article.get('title', '').lower() or 'approval' in article.get('title', '').lower():
            badge = "APPROVAL"
        
        # Generate family-friendly summary
        summary = self._generate_family_summary(article)
        
        # Generate detailed explanation
        details = self._generate_detailed_explanation(article)
        
        return {
            'id': hashlib.md5(article.get('url', '').encode()).hexdigest()[:8],
            'badge': badge,
            'title': article.get('title', 'No title available'),
            'summary': summary,
            'details': {
                'heading': "🔬 What This Means for Families:",
                'content': details
            },
            'meta': {
                'published': article.get('date', 'Unknown date'),
                'phase': article.get('phase', 'Research'),
                'status': article.get('status', 'Published'),
                'priority': article.get('priority', 'MEDIUM')
            },
            'link': article.get('url', '#')
        }
    
    def _generate_family_summary(self, article: Dict) -> str:
        """Generate a family-friendly summary of the article"""
        title = article.get('title', '')
        abstract = article.get('abstract', '')
        
        # Simple AI-like text processing to make it family-friendly
        summary = abstract[:300] + "..." if len(abstract) > 300 else abstract
        
        # Replace technical terms with simpler ones
        replacements = {
            'type 1 diabetes mellitus': 'Type 1 Diabetes',
            'insulin-dependent diabetes': 'Type 1 Diabetes',
            'beta cells': 'insulin-producing cells',
            'autoimmune': 'immune system',
            'glucose': 'blood sugar',
            'glycemic control': 'blood sugar control',
            'clinical trial': 'research study',
            'randomized controlled trial': 'research study'
        }
        
        for technical, simple in replacements.items():
            summary = summary.replace(technical, simple)
            
        return summary
    
    def _generate_detailed_explanation(self, article: Dict) -> str:
        """Generate a detailed explanation for families"""
        # This would ideally use AI, but for now we'll create template responses
        source = article.get('source', '')
        
        if source == 'ClinicalTrials.gov':
            return "This research study is looking for volunteers to test new treatments for Type 1 Diabetes. Participating in clinical trials helps advance our understanding of the disease and brings us closer to finding better treatments or even a cure."
        elif source == 'PubMed':
            return "This research paper presents new findings about Type 1 Diabetes. Scientists are constantly learning more about how the disease works and how to treat it better. This research contributes to our overall understanding and may lead to new treatment options in the future."
        else:
            return "This development represents ongoing progress in Type 1 Diabetes research. Every new discovery, no matter how small, brings us closer to better treatments and ultimately a cure for this disease."
    
    def run_scraping_workflow(self) -> List[Dict]:
        """Run the complete scraping workflow"""
        logger.info("Starting medical research scraping workflow...")
        
        all_articles = []
        
        # Scrape different sources
        try:
            pubmed_articles = self.scrape_pubmed()
            all_articles.extend(pubmed_articles)
            logger.info(f"Scraped {len(pubmed_articles)} articles from PubMed")
        except Exception as e:
            logger.error(f"PubMed scraping failed: {e}")
        
        try:
            clinical_trials = self.scrape_clinical_trials()
            all_articles.extend(clinical_trials)
            logger.info(f"Scraped {len(clinical_trials)} trials from ClinicalTrials.gov")
        except Exception as e:
            logger.error(f"ClinicalTrials.gov scraping failed: {e}")
        
        try:
            journal_articles = self.scrape_medical_journals()
            all_articles.extend(journal_articles)
            logger.info(f"Scraped {len(journal_articles)} articles from medical journals")
        except Exception as e:
            logger.error(f"Medical journal scraping failed: {e}")
        
        # Convert to breaking news format
        breaking_news = []
        for article in all_articles:
            try:
                news_item = self.generate_breaking_news_item(article)
                breaking_news.append(news_item)
            except Exception as e:
                logger.error(f"Error converting article to breaking news: {e}")
        
        # Sort by priority and date
        breaking_news.sort(key=lambda x: (
            {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}.get(x['meta']['priority'], 1),
            x['meta']['published']
        ))
        
        logger.info(f"Generated {len(breaking_news)} breaking news items")
        return breaking_news[:5]  # Return top 5 most relevant

def main():
    """Main function to run the scraper"""
    scraper = MedicalScraper()
    breaking_news = scraper.run_scraping_workflow()
    
    # Save to JSON file
    output_file = 'breaking_news_data.json'
    with open(output_file, 'w') as f:
        json.dump(breaking_news, f, indent=2)
    
    logger.info(f"Breaking news data saved to {output_file}")
    
    # Print summary
    for item in breaking_news:
        print(f"\n{item['badge']}: {item['title']}")
        print(f"Source: {item['meta']['phase']} - {item['meta']['status']}")
        print(f"Priority: {item['meta']['priority']}")

if __name__ == "__main__":
    main()
