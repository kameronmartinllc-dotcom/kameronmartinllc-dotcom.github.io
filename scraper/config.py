"""
Configuration file for the medical scraper
"""

# Scraping settings
SCRAPING_CONFIG = {
    'days_back': 7,  # How many days back to look for articles
    'max_articles_per_source': 10,  # Maximum articles per source
    'min_keyword_matches': 2,  # Minimum T1D keyword matches required
    'request_delay': 0.5,  # Delay between requests (seconds)
    'timeout': 30,  # Request timeout (seconds)
}

# Type 1 Diabetes keywords for filtering
T1D_KEYWORDS = [
    'type 1 diabetes', 'T1D', 'insulin-dependent diabetes', 'juvenile diabetes',
    'beta cell', 'autoimmune diabetes', 'diabetic ketoacidosis', 'insulin therapy',
    'glucose monitoring', 'closed-loop', 'artificial pancreas', 'islet transplantation',
    'stem cell diabetes', 'immunotherapy diabetes', 'diabetes cure', 'diabetes prevention',
    'beta cell regeneration', 'insulin production', 'pancreatic islets', 'autoimmune attack',
    'diabetes research', 'diabetes treatment', 'insulin pump', 'continuous glucose monitoring'
]

# Priority mapping for different sources and content
PRIORITY_MAPPING = {
    'ClinicalTrials.gov': {
        'PHASE3': 'HIGH',
        'PHASE2': 'HIGH', 
        'PHASE1': 'MEDIUM',
        'RECRUITING': 'HIGH',
        'ACTIVE': 'MEDIUM'
    },
    'PubMed': {
        'breakthrough': 'HIGH',
        'revolutionary': 'HIGH',
        'cure': 'HIGH',
        'prevention': 'HIGH',
        'fda': 'HIGH',
        'approval': 'HIGH'
    }
}

# Badge mapping based on content and source
BADGE_MAPPING = {
    'ClinicalTrials.gov': {
        'HIGH': 'HOT',
        'MEDIUM': 'TRIAL',
        'LOW': 'TRIAL'
    },
    'PubMed': {
        'breakthrough': 'BREAKTHROUGH',
        'revolutionary': 'BREAKTHROUGH', 
        'fda': 'APPROVAL',
        'approval': 'APPROVAL',
        'cure': 'BREAKTHROUGH',
        'prevention': 'NEW'
    }
}

# RSS feeds and sources to scrape
MEDICAL_SOURCES = [
    {
        'name': 'Diabetes Care',
        'url': 'https://diabetesjournals.org/care/rss',
        'type': 'rss',
        'priority': 'HIGH'
    },
    {
        'name': 'Nature Medicine',
        'url': 'https://www.nature.com/nm.rss',
        'type': 'rss',
        'priority': 'HIGH'
    },
    {
        'name': 'JAMA',
        'url': 'https://jamanetwork.com/rss/site_1/1.xml',
        'type': 'rss',
        'priority': 'MEDIUM'
    },
    {
        'name': 'NEJM',
        'url': 'https://www.nejm.org/rss',
        'type': 'rss',
        'priority': 'HIGH'
    },
    {
        'name': 'Lancet',
        'url': 'https://www.thelancet.com/rss',
        'type': 'rss',
        'priority': 'HIGH'
    }
]

# Email notifications (optional)
EMAIL_CONFIG = {
    'enabled': False,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': '',
    'sender_password': '',
    'recipient_emails': []
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'scraper.log',
    'max_size': 10485760,  # 10MB
    'backup_count': 5
}
