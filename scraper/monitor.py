#!/usr/bin/env python3
"""
Monitoring and Quality Control for Medical Scraper
Checks scraper health, data quality, and sends alerts if needed
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import requests
from typing import Dict, List

class ScraperMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.issues = []
        
    def check_scraper_health(self) -> bool:
        """Check if the scraper is working properly"""
        self.logger.info("Checking scraper health...")
        
        # Check if data file exists and is recent
        data_file = Path('breaking_news_data.json')
        if not data_file.exists():
            self.issues.append("Breaking news data file not found")
            return False
        
        # Check file age
        file_age = datetime.now() - datetime.fromtimestamp(data_file.stat().st_mtime)
        if file_age > timedelta(hours=12):
            self.issues.append(f"Data file is {file_age} old - scraper may not be running")
            return False
        
        # Check data quality
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            if not data:
                self.issues.append("No breaking news data found")
                return False
            
            # Check for required fields
            for item in data:
                required_fields = ['title', 'summary', 'badge', 'meta']
                for field in required_fields:
                    if field not in item:
                        self.issues.append(f"Missing required field '{field}' in data item")
                        return False
            
            self.logger.info(f"Scraper health check passed - {len(data)} items found")
            return True
            
        except Exception as e:
            self.issues.append(f"Error reading data file: {e}")
            return False
    
    def check_website_availability(self) -> bool:
        """Check if the website is accessible"""
        self.logger.info("Checking website availability...")
        
        try:
            # Check if index.html exists and is readable
            index_file = Path('../index.html')
            if not index_file.exists():
                self.issues.append("index.html not found")
                return False
            
            # Check if the file contains breaking news section
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'breaking-news' not in content:
                self.issues.append("Breaking news section not found in index.html")
                return False
            
            self.logger.info("Website availability check passed")
            return True
            
        except Exception as e:
            self.issues.append(f"Error checking website: {e}")
            return False
    
    def check_data_quality(self) -> Dict:
        """Check the quality of scraped data"""
        self.logger.info("Checking data quality...")
        
        quality_report = {
            'total_items': 0,
            'valid_items': 0,
            'issues': [],
            'sources': {},
            'priorities': {},
            'badges': {}
        }
        
        try:
            with open('breaking_news_data.json', 'r') as f:
                data = json.load(f)
            
            quality_report['total_items'] = len(data)
            
            for item in data:
                # Check item validity
                if self._is_valid_item(item):
                    quality_report['valid_items'] += 1
                else:
                    quality_report['issues'].append(f"Invalid item: {item.get('title', 'Unknown')}")
                
                # Count sources
                source = item.get('meta', {}).get('phase', 'Unknown')
                quality_report['sources'][source] = quality_report['sources'].get(source, 0) + 1
                
                # Count priorities
                priority = item.get('meta', {}).get('priority', 'Unknown')
                quality_report['priorities'][priority] = quality_report['priorities'].get(priority, 0) + 1
                
                # Count badges
                badge = item.get('badge', 'Unknown')
                quality_report['badges'][badge] = quality_report['badges'].get(badge, 0) + 1
            
            # Check for diversity
            if len(quality_report['sources']) < 2:
                quality_report['issues'].append("Low source diversity")
            
            if len(quality_report['priorities']) < 2:
                quality_report['issues'].append("Low priority diversity")
            
            self.logger.info(f"Data quality check completed - {quality_report['valid_items']}/{quality_report['total_items']} valid items")
            
        except Exception as e:
            quality_report['issues'].append(f"Error checking data quality: {e}")
        
        return quality_report
    
    def _is_valid_item(self, item: Dict) -> bool:
        """Check if a data item is valid"""
        required_fields = ['title', 'summary', 'badge', 'meta', 'link']
        
        for field in required_fields:
            if field not in item or not item[field]:
                return False
        
        # Check title length
        if len(item.get('title', '')) < 10:
            return False
        
        # Check summary length
        if len(item.get('summary', '')) < 20:
            return False
        
        return True
    
    def check_recent_updates(self) -> bool:
        """Check if there have been recent updates"""
        self.logger.info("Checking for recent updates...")
        
        # Check if update_report.json exists and is recent
        report_file = Path('../update_report.json')
        if not report_file.exists():
            self.issues.append("Update report not found")
            return False
        
        try:
            with open(report_file, 'r') as f:
                report = json.load(f)
            
            update_time = datetime.fromisoformat(report.get('update_time', ''))
            time_since_update = datetime.now() - update_time
            
            if time_since_update > timedelta(hours=24):
                self.issues.append(f"No updates in {time_since_update}")
                return False
            
            self.logger.info(f"Recent updates found - last update {time_since_update} ago")
            return True
            
        except Exception as e:
            self.issues.append(f"Error checking recent updates: {e}")
            return False
    
    def generate_health_report(self) -> Dict:
        """Generate a comprehensive health report"""
        self.logger.info("Generating health report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'scraper_health': self.check_scraper_health(),
            'website_availability': self.check_website_availability(),
            'recent_updates': self.check_recent_updates(),
            'data_quality': self.check_data_quality(),
            'issues': self.issues,
            'overall_status': 'HEALTHY'
        }
        
        # Determine overall status
        if not report['scraper_health'] or not report['website_availability']:
            report['overall_status'] = 'CRITICAL'
        elif not report['recent_updates'] or report['data_quality']['issues']:
            report['overall_status'] = 'WARNING'
        
        # Save report
        with open('health_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Health report generated - Status: {report['overall_status']}")
        return report
    
    def send_alert_if_needed(self, report: Dict):
        """Send alert if there are critical issues"""
        if report['overall_status'] == 'CRITICAL':
            self.logger.error("CRITICAL issues detected - alert should be sent")
            # Here you would implement email/Slack notifications
            # For now, just log the issues
            for issue in report['issues']:
                self.logger.error(f"CRITICAL: {issue}")

def main():
    """Main monitoring function"""
    monitor = ScraperMonitor()
    report = monitor.generate_health_report()
    monitor.send_alert_if_needed(report)
    
    # Print summary
    print(f"\n=== Scraper Health Report ===")
    print(f"Overall Status: {report['overall_status']}")
    print(f"Scraper Health: {'✓' if report['scraper_health'] else '✗'}")
    print(f"Website Available: {'✓' if report['website_availability'] else '✗'}")
    print(f"Recent Updates: {'✓' if report['recent_updates'] else '✗'}")
    print(f"Data Quality: {report['data_quality']['valid_items']}/{report['data_quality']['total_items']} valid items")
    
    if report['issues']:
        print(f"\nIssues Found:")
        for issue in report['issues']:
            print(f"  - {issue}")

if __name__ == "__main__":
    main()
