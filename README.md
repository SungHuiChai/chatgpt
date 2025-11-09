# Person Search Tool 🔍

A comprehensive Python-based search tool for finding information about a person across multiple sources including academic papers, news articles, and web mentions. Perfect for research, background checks, or finding someone's public contributions.

## 🎯 Features

- **📚 Academic Paper Search**
  - Google Scholar integration
  - arXiv search
  - Finds research papers, publications, and citations

- **📰 News Article Search**
  - Google News search
  - University news sites (Columbia, MIT, Stanford, Harvard, etc.)
  - Find media mentions and features

- **🌐 Web Search**
  - General Google search
  - Podcast and interview mentions
  - Social media profiles (Medium, Dev.to, Stack Overflow, etc.)
  - Domain-specific searches

## 📋 Use Case Example

**Goal**: Find information about "Aruzhan Abil"
- ✅ Finds her research papers
- ✅ Discovers Columbia news article where she was featured
- ✅ Locates other web mentions and profiles

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Steps

1. **Clone or download this repository**
   ```bash
   cd /path/to/chatgpt
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys (Optional but recommended)**
   
   Create a `.env` file in the project root:
   ```bash
   # Create .env file
   touch .env
   ```
   
   Add your Tavily API key to `.env`:
   ```
   TAVILY_API_KEY=your_actual_api_key_here
   ```
   
   **Get a Tavily API key** (Free tier: 1,000 searches/month):
   - Sign up at [https://tavily.com/](https://tavily.com/)
   - Get your API key from the dashboard
   - Paste it in the `.env` file
   
   > **Note**: The tool works without an API key but with limited results using basic web scraping.
   > Tavily is an AI-powered search API designed specifically for LLMs and AI agents.

4. **Copy configuration file (Optional)**
   ```bash
   cp config_example.py config.py
   ```

## 💻 Usage

### Quick Start

Run the main search script:
```bash
python person_search.py
```

This will search for "Aruzhan Abil" by default and save results to a JSON file.

### Custom Search

Edit `person_search.py` or create your own script:

```python
from person_search import PersonSearcher

# Initialize the searcher
searcher = PersonSearcher(tavily_api_key="your_key_here")  # or None for basic search

# Perform comprehensive search
results = searcher.search(
    person_name="Aruzhan Abil",
    university="Columbia",  # Optional: for targeted university news search
    max_results_per_source=10,
    include_social=False,  # Set True to search social media
    search_papers=True,
    search_news=True,
    search_web=True
)

# Print summary
searcher.print_summary(results)

# Print detailed results
searcher.print_detailed_results(results, max_display=5)

# Save to JSON file
searcher.save_results(results)
```

### Using Individual Search Modules

#### Search Papers Only
```python
from search_papers import PaperSearcher

searcher = PaperSearcher()
results = searcher.search_all("Aruzhan Abil", max_results=10)

for source, papers in results.items():
    print(f"\n{source}: {len(papers)} papers")
    for paper in papers:
        print(f"  - {paper['title']}")
```

#### Search News Only
```python
from search_news import NewsSearcher

searcher = NewsSearcher(serpapi_key="your_key")
results = searcher.search_all("Aruzhan Abil", university="Columbia")

for source, articles in results.items():
    print(f"\n{source}: {len(articles)} articles")
    for article in articles:
        print(f"  - {article['title']}")
```

#### Search Web Only
```python
from search_web import WebSearcher

searcher = WebSearcher(tavily_api_key="your_key")
results = searcher.search_all("Aruzhan Abil", max_results=10)

for search_type, items in results.items():
    if isinstance(items, list):
        print(f"\n{search_type}: {len(items)} results")
```

## 📁 Project Structure

```
chatgpt/
├── person_search.py       # Main orchestrator script
├── search_papers.py       # Academic paper search module
├── search_news.py         # News article search module
├── search_web.py          # General web search module
├── config_example.py      # Configuration template
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── LICENSE               # License file
```

## 🔧 Configuration

Edit `config_example.py` (or `config.py` if you copied it) to customize:

- API keys
- Default search settings
- University news sites
- Social media platforms to search
- Search filters and timeouts

## 📊 Output Format

### Console Output
The tool provides formatted output with:
- 🔍 Search progress indicators
- ✅ Success messages with counts
- ⚠️ Warnings for no results
- ❌ Error messages with details

### JSON Output
Results are saved in JSON format with structure:
```json
{
  "person_name": "Person Name",
  "search_timestamp": "2024-11-09T10:30:00",
  "papers": {
    "google_scholar": [...],
    "arxiv": [...]
  },
  "news": {
    "google_news": [...],
    "university_news": [...]
  },
  "web": {
    "general_search": [...],
    "podcasts_interviews": [...]
  },
  "summary": {
    "total_papers": 10,
    "total_news_articles": 5,
    "total_web_results": 15
  }
}
```

## 🎯 Examples

### Example 1: Basic Search
```bash
python person_search.py
```

### Example 2: Search with Custom Parameters
```python
from person_search import PersonSearcher
import os

# Load API key from environment
tavily_api_key = os.getenv('TAVILY_API_KEY')

searcher = PersonSearcher(tavily_api_key=tavily_api_key)

# Search for a researcher
results = searcher.search(
    person_name="John Doe",
    university="MIT",
    max_results_per_source=5,
    search_papers=True,
    search_news=True,
    search_web=False  # Skip web search
)

searcher.print_summary(results)
```

### Example 3: Search Multiple People
```python
from person_search import PersonSearcher

searcher = PersonSearcher()

people = ["Aruzhan Abil", "John Smith", "Jane Doe"]

for person in people:
    print(f"\n{'='*80}")
    print(f"Searching for: {person}")
    print('='*80)
    
    results = searcher.search(person_name=person, max_results_per_source=3)
    searcher.print_summary(results)
    searcher.save_results(results)
```

## ⚠️ Important Notes

1. **Rate Limiting**: The tool includes delays between requests to be respectful to servers. Don't modify these unless necessary.

2. **API Quotas**: Tavily free tier has a limit of 1,000 searches/month. Each person search uses multiple API calls.

3. **Web Scraping**: Basic search (without API key) uses web scraping which may be blocked by sites or return limited results.

4. **Tavily Advantage**: Tavily is specifically designed for AI agents with better quality, relevance scoring, and content extraction compared to traditional search APIs.

4. **Accuracy**: Results depend on publicly available information and search engine indexing.

5. **Privacy**: Use this tool responsibly and respect privacy laws and regulations.

## 🐛 Troubleshooting

### Issue: No results found
- **Solution**: Try different name variations (e.g., "John A. Smith" vs "John Smith")
- Check if the person has public information online
- Try with a SerpAPI key for better results

### Issue: "scholarly" module errors
- **Solution**: 
  ```bash
  pip install --upgrade scholarly
  ```
- If Google Scholar blocks requests, wait a few minutes and try again

### Issue: Tavily API errors
- **Solution**: 
  - Check your API key is correct in `.env` file
  - Verify you haven't exceeded your monthly quota (1,000 searches/month on free tier)
  - Check internet connection
  - Visit [Tavily dashboard](https://tavily.com/) to check your usage

### Issue: Slow performance
- **Solution**: 
  - Reduce `max_results_per_source`
  - Disable social media search (`include_social=False`)
  - Use Tavily API for faster and more reliable results

## 🔐 Privacy & Ethics

This tool searches **publicly available information only**. Please:
- Use it ethically and legally
- Respect privacy laws (GDPR, CCPA, etc.)
- Don't use for harassment or stalking
- Verify information from original sources
- Consider getting consent when appropriate

## 📝 License

See the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new search sources
- Improve search accuracy
- Fix bugs
- Enhance documentation

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review example usage
3. Check API documentation (SerpAPI, scholarly)

## 🎓 Credits

Built using:
- [Tavily](https://tavily.com/) - AI-powered search API for agents
- [scholarly](https://github.com/scholarly-python-package/scholarly) - Google Scholar scraping
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - Web scraping
- [requests](https://requests.readthedocs.io/) - HTTP library

---

**Made with ❤️ for research and discovery**

