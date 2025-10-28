# Medical Research Scraper for Type 1 Diabetes

This automated system scrapes medical publications and clinical trials to keep your Breaking News section updated with the latest Type 1 Diabetes research developments.

## 🚀 Features

- **Automated Scraping**: Pulls data from PubMed, ClinicalTrials.gov, and medical journal RSS feeds
- **Smart Filtering**: Only includes T1D-relevant content using keyword matching
- **Family-Friendly Content**: Converts technical research into accessible summaries
- **Automated Updates**: GitHub Actions workflow runs every 6 hours
- **Quality Control**: Monitoring system ensures data quality and system health
- **No API Keys Required**: Uses publicly accessible sources

## 📁 File Structure

```
scraper/
├── medical_scraper.py      # Main scraping engine
├── config.py              # Configuration settings
├── monitor.py             # Health monitoring
├── setup.py               # Setup script
├── requirements.txt       # Python dependencies
└── breaking_news_data.json # Scraped data output

.github/workflows/
└── update-breaking-news.yml # Automated GitHub Actions workflow

update_website.py          # Updates index.html with new data
```

## 🛠️ Setup

### 1. Install Dependencies

```bash
cd scraper
python setup.py
```

### 2. Test the Scraper

```bash
python medical_scraper.py
```

### 3. Update Your Website

```bash
python ../update_website.py
```

## 🔧 Configuration

Edit `scraper/config.py` to customize:

- **Scraping frequency**: How often to check for new content
- **Keywords**: T1D-related terms to filter content
- **Sources**: Which medical journals to scrape
- **Priority mapping**: How to categorize content importance

## 📊 Data Sources

### PubMed
- **What**: Medical research papers
- **API**: E-utilities (free, no auth required)
- **Filter**: T1D keywords in title/abstract
- **Update**: Real-time

### ClinicalTrials.gov
- **What**: Active clinical trials
- **API**: REST API (free, no auth required)
- **Filter**: T1D-related trials, recruiting status
- **Update**: Real-time

### Medical Journals (RSS)
- **What**: Latest journal articles
- **Sources**: Diabetes Care, Nature Medicine, JAMA, NEJM, Lancet
- **Filter**: T1D keywords in titles/descriptions
- **Update**: Real-time

## 🤖 Automated Workflow

The system runs automatically via GitHub Actions:

1. **Every 6 hours**: Scraper runs and fetches new content
2. **Content Processing**: Filters and formats T1D-relevant articles
3. **Website Update**: Updates your index.html with new breaking news
4. **Quality Check**: Monitors data quality and system health
5. **Auto-commit**: Changes are automatically committed to your repository

## 📈 Monitoring

### Health Checks
- Data freshness (last update time)
- Content quality (required fields, length)
- Source diversity
- Website availability

### Manual Monitoring
```bash
cd scraper
python monitor.py
```

### Logs
- Scraper logs: `scraper/logs/scraper.log`
- Health reports: `scraper/health_report.json`
- Update reports: `update_report.json`

## 🎯 Content Quality

### Automatic Filtering
- **Keyword Matching**: Must contain 2+ T1D-related terms
- **Relevance Scoring**: Prioritizes breakthrough/revolutionary content
- **Source Prioritization**: Clinical trials and high-impact journals first

### Content Processing
- **Technical → Simple**: Converts medical jargon to family-friendly language
- **Priority Assignment**: HIGH/MEDIUM/LOW based on source and content
- **Badge Assignment**: HOT/NEW/BREAKTHROUGH/APPROVAL based on content type

## 🔄 Manual Updates

### Add New Breaking News
```python
from update_website import addBreakingNews

new_item = {
    'badge': 'HOT',
    'title': 'Your New Development',
    'summary': 'Brief description...',
    'details': {
        'heading': 'What This Means:',
        'content': 'Detailed explanation...'
    },
    'meta': {
        'published': 'January 2025',
        'phase': 'Phase 2',
        'status': 'Recruiting',
        'priority': 'HIGH'
    },
    'link': 'https://your-link.com'
}

addBreakingNews(new_item)
```

### Force Update
```bash
# Run scraper manually
cd scraper
python medical_scraper.py

# Update website
python ../update_website.py

# Commit changes
git add .
git commit -m "Manual update: $(date)"
git push
```

## 🚨 Troubleshooting

### Common Issues

1. **No new content found**
   - Check internet connection
   - Verify source URLs are accessible
   - Adjust keyword filters in config.py

2. **Website not updating**
   - Check file permissions
   - Verify index.html exists
   - Check update_website.py logs

3. **GitHub Actions failing**
   - Check workflow logs in GitHub Actions tab
   - Verify repository permissions
   - Check Python version compatibility

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python medical_scraper.py
```

## 📝 Customization

### Add New Sources
Edit `config.py`:
```python
MEDICAL_SOURCES.append({
    'name': 'Your Journal',
    'url': 'https://your-journal.com/rss',
    'type': 'rss',
    'priority': 'HIGH'
})
```

### Modify Keywords
Edit `config.py`:
```python
T1D_KEYWORDS.extend([
    'your_new_keyword',
    'another_term'
])
```

### Change Update Frequency
Edit `.github/workflows/update-breaking-news.yml`:
```yaml
schedule:
  - cron: '0 */3 * * *'  # Every 3 hours instead of 6
```

## 🔒 Security & Privacy

- **No API Keys**: Uses only public, free APIs
- **No Personal Data**: Only scrapes public research content
- **Rate Limiting**: Respects server limits with delays
- **Error Handling**: Graceful failure without exposing sensitive info

## 📞 Support

If you encounter issues:

1. Check the logs in `scraper/logs/`
2. Run the monitor: `python scraper/monitor.py`
3. Test individual components
4. Check GitHub Actions workflow status

## 🎉 Success Metrics

The system tracks:
- **Content Volume**: Number of articles found per update
- **Source Diversity**: Variety of medical sources
- **Quality Score**: Percentage of valid, relevant content
- **Update Frequency**: Time between successful updates
- **Website Health**: Availability and functionality

---

**Note**: This system is designed to be respectful of source websites and uses only publicly available data. It includes appropriate delays and error handling to avoid overloading servers.
