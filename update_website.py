#!/usr/bin/env python3
"""
Website Updater for Breaking News
Updates the index.html file with latest scraped medical research data
"""

import json
import re
from datetime import datetime
from pathlib import Path

def update_breaking_news_section(breaking_news_data):
    """Update the breaking news section in index.html with new data"""
    
    # The main page only shows a teaser (top article), not the full breaking news list
    # The full breaking news is on breaking-news.html
    # The teaser is updated by JavaScript from breaking_news_data.json
    # So we don't need to update the hidden breaking news section on the main page
    
    print(f"Main page teaser will be updated by JavaScript from {len(breaking_news_data)} breaking news items")
    return True

def generate_breaking_news_html(breaking_news_data):
    """Generate HTML for breaking news items"""
    
    if not breaking_news_data:
        return '<div class="loading">No breaking news at this time. Check back soon!</div>'
    
    html_items = []
    
    for item in breaking_news_data:
        html_item = f'''
        <div class="breaking-item">
          <div class="breaking-badge">{item['badge']}</div>
          <h3 class="breaking-title">{item['title']}</h3>
          <p class="breaking-summary">{item['summary']}</p>
          <div class="breaking-details">
            <h4>{item['details']['heading']}</h4>
            <p>{item['details']['content']}</p>
          </div>
          <div class="breaking-meta">
            <span>Published: {item['meta']['published']}</span>
            <span>Phase: {item['meta']['phase']}</span>
            <span>Status: {item['meta']['status']}</span>
            <span>Priority: {item['meta']['priority']}</span>
          </div>
          <a href="{item['link']}" class="breaking-link" target="_blank">Read Full Report →</a>
        </div>'''
        
        html_items.append(html_item)
    
    return '\n'.join(html_items)

def create_news_archive(breaking_news_data):
    """Create an archive of all breaking news items"""
    
    archive_path = Path('news_archive.json')
    
    # Load existing archive
    archive = []
    if archive_path.exists():
        with open(archive_path, 'r', encoding='utf-8') as f:
            archive = json.load(f)
    
    # Add new items (avoid duplicates)
    existing_ids = {item.get('id') for item in archive}
    
    for item in breaking_news_data:
        if item.get('id') not in existing_ids:
            item['archived_date'] = datetime.now().isoformat()
            archive.append(item)
    
    # Keep only last 50 items
    archive = archive[-50:]
    
    # Save archive
    with open(archive_path, 'w', encoding='utf-8') as f:
        json.dump(archive, f, indent=2)
    
    print(f"Updated news archive with {len(archive)} total items")

def main():
    """Main function to update the website"""
    
    # Load breaking news data
    data_path = Path('scraper/breaking_news_data.json')
    if not data_path.exists():
        print("Error: breaking_news_data.json not found. Run the scraper first.")
        return
    
    with open(data_path, 'r', encoding='utf-8') as f:
        breaking_news_data = json.load(f)
    
    print(f"Loaded {len(breaking_news_data)} breaking news items")
    
    # Update the website
    if update_breaking_news_section(breaking_news_data):
        print("Website updated successfully!")
        
        # Create archive
        create_news_archive(breaking_news_data)
        
        # Generate a summary report
        generate_summary_report(breaking_news_data)
    else:
        print("Failed to update website")

def generate_summary_report(breaking_news_data):
    """Generate a summary report of the update"""
    
    report = {
        'update_time': datetime.now().isoformat(),
        'total_items': len(breaking_news_data),
        'sources': {},
        'priorities': {},
        'badges': {}
    }
    
    for item in breaking_news_data:
        # Count sources
        source = item['meta'].get('phase', 'Unknown')
        report['sources'][source] = report['sources'].get(source, 0) + 1
        
        # Count priorities
        priority = item['meta'].get('priority', 'Unknown')
        report['priorities'][priority] = report['priorities'].get(priority, 0) + 1
        
        # Count badges
        badge = item.get('badge', 'Unknown')
        report['badges'][badge] = report['badges'].get(badge, 0) + 1
    
    # Save report
    with open('update_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print("Update report generated")

if __name__ == "__main__":
    main()
