#!/usr/bin/env python3
"""
Setup script for the medical scraper
Installs dependencies and sets up the environment
"""

import subprocess
import sys
from pathlib import Path

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = ['logs', 'data', 'archive']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def test_scraper():
    """Test the scraper to make sure it works"""
    print("Testing scraper...")
    try:
        from medical_scraper import MedicalScraper
        scraper = MedicalScraper()
        
        # Test with a small sample
        print("  - Testing PubMed scraping...")
        articles = scraper.scrape_pubmed(days_back=1)
        print(f"    Found {len(articles)} articles")
        
        print("  - Testing ClinicalTrials.gov scraping...")
        trials = scraper.scrape_clinical_trials(days_back=1)
        print(f"    Found {len(trials)} trials")
        
        print("✓ Scraper test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Scraper test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("=== Medical Scraper Setup ===")
    
    # Install requirements
    if not install_requirements():
        print("Setup failed - could not install requirements")
        return False
    
    # Create directories
    create_directories()
    
    # Test scraper
    if not test_scraper():
        print("Setup failed - scraper test failed")
        return False
    
    print("\n=== Setup Complete ===")
    print("The medical scraper is ready to use!")
    print("\nTo run the scraper:")
    print("  python medical_scraper.py")
    print("\nTo monitor the scraper:")
    print("  python monitor.py")
    print("\nTo update the website:")
    print("  python ../update_website.py")
    
    return True

if __name__ == "__main__":
    main()
