#!/usr/bin/env python3
"""
Diabetes Assistance Program Scraper
Scrapes manufacturer websites and diabetes supply companies for uninsured patient assistance programs
"""

import requests
from bs4 import BeautifulSoup
import json
import logging
from typing import Dict, List
import time
from urllib.parse import urljoin, urlparse
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DiabetesAssistanceScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Major diabetes manufacturers and suppliers
        self.companies = {
            # Insulin Manufacturers
            'insulin_manufacturers': {
                'Eli Lilly': {
                    'base_url': 'https://www.lilly.com',
                    'assistance_pages': [
                        '/diabetes/insulin-affordability',
                        '/patient-assistance',
                        '/diabetes/lilly-cares'
                    ]
                },
                'Novo Nordisk': {
                    'base_url': 'https://www.novonordisk-us.com',
                    'assistance_pages': [
                        '/patients/pap.html',
                        '/diabetes-care/let-us-help/help-with-costs.html'
                    ]
                },
                'Sanofi': {
                    'base_url': 'https://www.sanofi.us',
                    'assistance_pages': [
                        '/en/your-health/diabetes/patient-resources',
                        '/en/your-health/diabetes/insulin-affordability'
                    ]
                }
            },
            
            # CGM Manufacturers
            'cgm_manufacturers': {
                'Dexcom': {
                    'base_url': 'https://www.dexcom.com',
                    'assistance_pages': [
                        '/dexcom-warrior-program',
                        '/patient-assistance-program',
                        '/coverage-support'
                    ]
                },
                'Abbott (FreeStyle)': {
                    'base_url': 'https://www.freestyle.abbott',
                    'assistance_pages': [
                        '/us-en/support/patient-assistance-program.html',
                        '/us-en/support/coverage-support.html'
                    ]
                },
                'Medtronic': {
                    'base_url': 'https://www.medtronicdiabetes.com',
                    'assistance_pages': [
                        '/customer-support/insurance-coverage-support',
                        '/customer-support/financial-assistance'
                    ]
                }
            },
            
            # Pump Manufacturers
            'pump_manufacturers': {
                'Tandem': {
                    'base_url': 'https://www.tandemdiabetes.com',
                    'assistance_pages': [
                        '/support/insurance-and-coverage',
                        '/support/financial-assistance'
                    ]
                },
                'Omnipod (Insulet)': {
                    'base_url': 'https://www.omnipod.com',
                    'assistance_pages': [
                        '/coverage-support',
                        '/patient-assistance'
                    ]
                },
                'Medtronic': {
                    'base_url': 'https://www.medtronicdiabetes.com',
                    'assistance_pages': [
                        '/customer-support/insurance-coverage-support',
                        '/customer-support/financial-assistance'
                    ]
                }
            },
            
            # Supply Warehouses/Distributors
            'supply_companies': {
                'Diabetes Express': {
                    'base_url': 'https://www.diabetesexpress.com',
                    'assistance_pages': [
                        '/uninsured-discount-program',
                        '/patient-assistance'
                    ]
                },
                'ADW Diabetes': {
                    'base_url': 'https://www.adwdiabetes.com',
                    'assistance_pages': [
                        '/discount-programs',
                        '/uninsured-patients'
                    ]
                },
                'Diabetic Warehouse': {
                    'base_url': 'https://www.diabeticwarehouse.org',
                    'assistance_pages': [
                        '/discount-program',
                        '/patient-assistance'
                    ]
                },
                'Total Diabetes Supply': {
                    'base_url': 'https://www.totaldiabetessupply.com',
                    'assistance_pages': [
                        '/uninsured-discount',
                        '/patient-programs'
                    ]
                }
            }
        }
        
        # Additional resources to check
        self.additional_resources = [
            {
                'name': 'GoodRx',
                'url': 'https://www.goodrx.com/diabetes',
                'description': 'Prescription discount program'
            },
            {
                'name': 'NeedyMeds',
                'url': 'https://www.needymeds.org',
                'description': 'Patient assistance program database'
            },
            {
                'name': 'Partnership for Prescription Assistance',
                'url': 'https://www.pparx.org',
                'description': 'Pharmaceutical assistance programs'
            },
            {
                'name': 'Patient Access Network Foundation',
                'url': 'https://www.panfoundation.org',
                'description': 'Copay assistance for chronic diseases'
            }
        ]

    def scrape_assistance_programs(self) -> List[Dict]:
        """Scrape all diabetes assistance programs"""
        logger.info("Starting diabetes assistance program scraping...")
        
        all_programs = []
        
        # Scrape each category
        for category, companies in self.companies.items():
            logger.info(f"Scraping {category}...")
            
            for company_name, company_info in companies.items():
                try:
                    programs = self._scrape_company_programs(company_name, company_info, category)
                    all_programs.extend(programs)
                    time.sleep(2)  # Be respectful to servers
                except Exception as e:
                    logger.error(f"Error scraping {company_name}: {e}")
        
        # Add additional resources
        for resource in self.additional_resources:
            try:
                program = self._scrape_additional_resource(resource)
                if program:
                    all_programs.append(program)
                time.sleep(2)
            except Exception as e:
                logger.error(f"Error scraping {resource['name']}: {e}")
        
        logger.info(f"Found {len(all_programs)} assistance programs")
        return all_programs

    def _scrape_company_programs(self, company_name: str, company_info: Dict, category: str) -> List[Dict]:
        """Scrape assistance programs from a specific company"""
        programs = []
        base_url = company_info['base_url']
        
        for assistance_path in company_info['assistance_pages']:
            try:
                url = urljoin(base_url, assistance_path)
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    program = self._extract_program_info(soup, url, company_name, category)
                    if program:
                        programs.append(program)
                else:
                    logger.warning(f"Failed to access {url} - Status: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                # Create a basic entry even if scraping fails
                programs.append({
                    'company': company_name,
                    'category': category,
                    'program_name': f"{company_name} Patient Assistance",
                    'url': urljoin(base_url, assistance_path),
                    'description': f"Patient assistance program for {company_name} products",
                    'eligibility': "Varies - check website for details",
                    'how_to_apply': "Visit website or call customer service",
                    'contact_info': "See website for contact information",
                    'scraped_successfully': False
                })
        
        return programs

    def _extract_program_info(self, soup: BeautifulSoup, url: str, company_name: str, category: str) -> Dict:
        """Extract assistance program information from webpage"""
        
        # Try to find program title
        title_selectors = ['h1', 'h2', '.title', '.program-title', '.page-title']
        program_name = company_name + " Patient Assistance"
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem and title_elem.get_text().strip():
                program_name = title_elem.get_text().strip()
                break
        
        # Extract description
        description = self._extract_description(soup)
        
        # Extract eligibility information
        eligibility = self._extract_eligibility(soup)
        
        # Extract application process
        how_to_apply = self._extract_application_process(soup)
        
        # Extract contact information
        contact_info = self._extract_contact_info(soup)
        
        return {
            'company': company_name,
            'category': category,
            'program_name': program_name,
            'url': url,
            'description': description,
            'eligibility': eligibility,
            'how_to_apply': how_to_apply,
            'contact_info': contact_info,
            'scraped_successfully': True,
            'last_updated': time.strftime('%Y-%m-%d')
        }

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract program description"""
        description_keywords = ['assistance', 'program', 'help', 'support', 'discount', 'afford']
        
        # Look for paragraphs containing assistance-related keywords
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text().lower()
            if any(keyword in text for keyword in description_keywords) and len(text) > 50:
                return p.get_text().strip()[:300] + "..."
        
        # Fallback to meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '')[:300] + "..."
        
        return "Patient assistance program - visit website for details"

    def _extract_eligibility(self, soup: BeautifulSoup) -> str:
        """Extract eligibility requirements"""
        eligibility_keywords = ['eligible', 'qualify', 'income', 'uninsured', 'requirements']
        
        text_content = soup.get_text().lower()
        sentences = text_content.split('.')
        
        eligibility_info = []
        for sentence in sentences:
            if any(keyword in sentence for keyword in eligibility_keywords):
                clean_sentence = sentence.strip().capitalize()
                if len(clean_sentence) > 20:
                    eligibility_info.append(clean_sentence)
        
        if eligibility_info:
            return '. '.join(eligibility_info[:3]) + "."
        
        return "Eligibility varies - check website for specific requirements"

    def _extract_application_process(self, soup: BeautifulSoup) -> str:
        """Extract how to apply information"""
        application_keywords = ['apply', 'application', 'enroll', 'sign up', 'register']
        
        text_content = soup.get_text().lower()
        sentences = text_content.split('.')
        
        application_info = []
        for sentence in sentences:
            if any(keyword in sentence for keyword in application_keywords):
                clean_sentence = sentence.strip().capitalize()
                if len(clean_sentence) > 20:
                    application_info.append(clean_sentence)
        
        if application_info:
            return '. '.join(application_info[:2]) + "."
        
        return "Visit website or contact customer service to apply"

    def _extract_contact_info(self, soup: BeautifulSoup) -> str:
        """Extract contact information"""
        contact_info = []
        
        # Look for phone numbers
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        text = soup.get_text()
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info.append(f"Phone: {phones[0]}")
        
        # Look for email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info.append(f"Email: {emails[0]}")
        
        if contact_info:
            return ', '.join(contact_info)
        
        return "Contact information available on website"

    def _scrape_additional_resource(self, resource: Dict) -> Dict:
        """Scrape additional diabetes resources"""
        try:
            response = self.session.get(resource['url'], timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                return {
                    'company': resource['name'],
                    'category': 'additional_resources',
                    'program_name': resource['name'],
                    'url': resource['url'],
                    'description': resource['description'],
                    'eligibility': "Varies by program",
                    'how_to_apply': "Visit website for details",
                    'contact_info': "See website",
                    'scraped_successfully': True,
                    'last_updated': time.strftime('%Y-%m-%d')
                }
        except Exception as e:
            logger.error(f"Error scraping {resource['name']}: {e}")
        
        return None

    def generate_assistance_guide(self, programs: List[Dict]) -> Dict:
        """Generate a comprehensive assistance guide"""
        
        # Organize by category
        by_category = {}
        for program in programs:
            category = program['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(program)
        
        # Create family-friendly summaries
        guide = {
            'title': 'Diabetes Assistance Programs for Uninsured Families',
            'last_updated': time.strftime('%Y-%m-%d'),
            'introduction': {
                'heading': '💙 Help is Available',
                'content': 'If you\'re managing diabetes without insurance, you\'re not alone. Many manufacturers and organizations offer assistance programs to help reduce the cost of insulin, CGMs, pumps, and supplies. This guide compiles current programs to help you find the support you need.'
            },
            'categories': {},
            'quick_tips': [
                'Start with manufacturer programs - they often have the most generous assistance',
                'Don\'t be discouraged if you don\'t qualify for one program - try others',
                'Keep documentation of your income and medical needs ready',
                'Many programs can be combined with discount cards like GoodRx',
                'Call customer service - they often know about programs not listed online'
            ],
            'emergency_resources': [
                'For immediate insulin needs: Contact manufacturer patient assistance hotlines',
                'For supplies: Check local diabetes support groups and endocrinologist offices',
                'For CGMs: Many companies offer trial programs or starter kits'
            ]
        }
        
        # Add category-specific information
        category_descriptions = {
            'insulin_manufacturers': {
                'title': '💉 Insulin Assistance Programs',
                'description': 'Major insulin manufacturers offer programs that can reduce insulin costs to $35/month or even free for qualifying patients.'
            },
            'cgm_manufacturers': {
                'title': '📱 CGM Assistance Programs', 
                'description': 'Continuous glucose monitor companies provide programs to help with device and sensor costs.'
            },
            'pump_manufacturers': {
                'title': '⚡ Insulin Pump Assistance',
                'description': 'Pump manufacturers offer financing, loaner programs, and assistance for qualifying patients.'
            },
            'supply_companies': {
                'title': '📦 Supply Discount Programs',
                'description': 'Diabetes supply companies offer discounted rates for uninsured patients on test strips, lancets, and other supplies.'
            },
            'additional_resources': {
                'title': '🔗 Additional Resources',
                'description': 'Other organizations and programs that can help reduce diabetes-related costs.'
            }
        }
        
        for category, programs_list in by_category.items():
            if category in category_descriptions:
                guide['categories'][category] = {
                    **category_descriptions[category],
                    'programs': programs_list
                }
        
        return guide

def main():
    """Main function to run the assistance scraper"""
    scraper = DiabetesAssistanceScraper()
    
    # Scrape assistance programs
    programs = scraper.scrape_assistance_programs()
    
    # Generate comprehensive guide
    guide = scraper.generate_assistance_guide(programs)
    
    # Save to JSON files
    with open('scraper/diabetes_assistance_programs.json', 'w') as f:
        json.dump(programs, f, indent=2)
    
    with open('scraper/diabetes_assistance_guide.json', 'w') as f:
        json.dump(guide, f, indent=2)
    
    logger.info(f"Saved {len(programs)} assistance programs")
    logger.info("Generated comprehensive assistance guide")
    
    # Print summary
    print(f"\n🎯 DIABETES ASSISTANCE PROGRAMS FOUND: {len(programs)}")
    
    by_category = {}
    for program in programs:
        category = program['category']
        by_category[category] = by_category.get(category, 0) + 1
    
    for category, count in by_category.items():
        print(f"  {category.replace('_', ' ').title()}: {count} programs")

if __name__ == "__main__":
    main()
