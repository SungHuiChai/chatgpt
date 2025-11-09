# Person Search Tool - Project Overview

## 📌 Project Summary

A comprehensive Python-based search algorithm for finding information about individuals across multiple online sources, going beyond just LinkedIn, X (Twitter), and GitHub.

**Created for:** Finding academic papers, news articles, media mentions, and other public information about people.

**Example Use Case:** Finding Aruzhan Abil's research paper and Columbia news article where she was featured.

---

## 🏗️ Architecture

### Modular Design
The project is built with a modular architecture where each search source has its own independent module:

```
┌─────────────────────────────────────────┐
│       person_search.py (Orchestrator)    │
│  - Coordinates all searches              │
│  - Aggregates results                    │
│  - Formats output                        │
│  - Saves to JSON                         │
└───────────┬─────────────────────────────┘
            │
      ┌─────┴──────────────┐
      │                    │
┌─────▼─────┐    ┌────────▼────────┐    ┌────────▼──────┐
│ Papers    │    │ News Articles   │    │ Web Search    │
│ Module    │    │ Module          │    │ Module        │
├───────────┤    ├─────────────────┤    ├───────────────┤
│• Scholar  │    │• Google News    │    │• Google       │
│• arXiv    │    │• Univ. News     │    │• Podcasts     │
│           │    │                 │    │• Social Media │
└───────────┘    └─────────────────┘    └───────────────┘
```

---

## 📁 Files and Their Purpose

### Core Search Modules

| File | Purpose | Key Features |
|------|---------|-------------|
| `search_papers.py` | Academic paper search | • Google Scholar integration<br>• arXiv API search<br>• Returns papers with citations, abstracts, URLs |
| `search_news.py` | News article search | • Google News search<br>• University news sites<br>• Media mentions |
| `search_web.py` | General web search | • Google search<br>• Podcast/interview search<br>• Social media mentions<br>• Domain-specific search |
| `person_search.py` | Main orchestrator | • Coordinates all searches<br>• Aggregates results<br>• Formats output<br>• Saves to JSON |

### Configuration & Setup

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `config_example.py` | Configuration template |
| `.gitignore` | Git ignore patterns |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Complete documentation |
| `QUICKSTART.md` | 5-minute setup guide |
| `PROJECT_OVERVIEW.md` | This file - architecture overview |

### Examples

| File | Purpose |
|------|---------|
| `example_search.py` | Example usage scripts |
| `person_search.py` | Main executable (includes example) |

---

## 🎯 Search Capabilities

### 1. Academic Papers
- **Google Scholar**: Author profiles, publications, citations
- **arXiv**: Research papers in sciences
- **Returns**: Title, authors, year, venue, citations, abstract, URL

### 2. News Articles
- **Google News**: Recent news mentions
- **University News**: Columbia, MIT, Stanford, Harvard, etc.
- **Returns**: Title, source, date, snippet, URL

### 3. Web Mentions
- **General Search**: Overall web presence
- **Podcasts/Interviews**: Speaking appearances
- **Social Media**: Medium, Dev.to, Stack Overflow, Reddit, YouTube
- **Returns**: Title, URL, snippet, source

---

## 🔧 Technical Stack

### Core Technologies
- **Python 3.7+**: Main programming language
- **requests**: HTTP requests
- **BeautifulSoup4**: Web scraping and parsing
- **scholarly**: Google Scholar API
- **python-dotenv**: Environment variable management

### Optional Enhancements
- **SerpAPI**: Enhanced Google search results (100 free searches/month)
- **lxml**: Fast XML/HTML parsing

---

## 🚀 Usage Patterns

### Pattern 1: Quick Search (Default)
```bash
python person_search.py
```
- Searches for predefined person (Aruzhan Abil)
- Uses all search modules
- Saves results to JSON

### Pattern 2: Custom Search (Recommended)
```python
from person_search import PersonSearcher

searcher = PersonSearcher(serpapi_key="optional_key")
results = searcher.search(
    person_name="Jane Doe",
    university="MIT",
    max_results_per_source=10
)
```

### Pattern 3: Module-Specific Search
```python
from search_papers import PaperSearcher

searcher = PaperSearcher()
papers = searcher.search_all("Jane Doe")
```

---

## 📊 Data Flow

```
User Input (Name)
    ↓
┌───────────────────────────────┐
│  PersonSearcher.search()      │
└───────────────────────────────┘
    ↓
    ├─→ PaperSearcher.search_all()
    │       ├─→ Google Scholar API
    │       └─→ arXiv API
    │
    ├─→ NewsSearcher.search_all()
    │       ├─→ Google News (SerpAPI or scraping)
    │       └─→ University news sites
    │
    └─→ WebSearcher.search_all()
            ├─→ Google search
            ├─→ Podcast/interview search
            └─→ Social media search
    ↓
Results Aggregation
    ↓
    ├─→ Console Output (formatted)
    ├─→ Summary Display
    ├─→ Detailed Results Display
    └─→ JSON File Export
```

---

## 🎨 Key Design Decisions

### 1. **Modular Architecture**
- Each search type in separate module
- Easy to add/remove sources
- Can use modules independently

### 2. **Graceful Degradation**
- Works without API keys (basic search)
- Fallback mechanisms for failed searches
- Continues on errors

### 3. **Rate Limiting**
- Built-in delays between requests
- Respects server resources
- Avoids being blocked

### 4. **Flexible Output**
- Console display for immediate feedback
- JSON export for programmatic use
- Customizable result counts

### 5. **Error Handling**
- Try-catch blocks for robustness
- Informative error messages
- Partial results on failures

---

## 🔒 Privacy & Ethics

### Built-in Safeguards
- **Public information only**: No private data access
- **Rate limiting**: Respectful server usage
- **User Agent headers**: Transparent identity
- **No credential storage**: Only searches public data

### User Responsibilities
- Use ethically and legally
- Respect privacy laws (GDPR, CCPA)
- Verify information from sources
- Don't use for harassment

---

## 📈 Performance Characteristics

### With SerpAPI Key
- Fast and reliable results
- 100 searches/month (free tier)
- Better quality results
- **Recommended for production use**

### Without API Key (Basic Search)
- Slower due to web scraping
- May be blocked occasionally
- Limited result quality
- **Good for testing/development**

### Typical Search Times
- Papers: 10-30 seconds
- News: 5-15 seconds
- Web: 5-15 seconds
- **Total: 20-60 seconds per person**

---

## 🧩 Extensibility

### Easy to Add New Sources

1. **Create new search module** (e.g., `search_books.py`)
2. **Implement search methods**
3. **Add to orchestrator** (`person_search.py`)
4. **Update configuration** (`config_example.py`)

### Example: Adding Book Search
```python
# In search_books.py
class BookSearcher:
    def search_google_books(self, person_name):
        # Implementation
        pass
    
    def search_all(self, person_name):
        return self.search_google_books(person_name)

# In person_search.py
from search_books import BookSearcher

class PersonSearcher:
    def __init__(self):
        # ... existing code ...
        self.book_searcher = BookSearcher()
    
    def search(self, person_name):
        # ... existing code ...
        results['books'] = self.book_searcher.search_all(person_name)
```

---

## 🎯 Future Enhancements (Potential)

### Additional Sources
- [ ] Patents (Google Patents, USPTO)
- [ ] Books (Google Books, Amazon)
- [ ] Conference presentations (IEEE, ACM)
- [ ] Video content (YouTube transcripts)
- [ ] GitHub repositories (code contributions)

### Features
- [ ] Parallel searching (async/await)
- [ ] Caching mechanism
- [ ] Web UI/dashboard
- [ ] Export to PDF report
- [ ] Duplicate detection
- [ ] Relevance scoring
- [ ] Timeline visualization

### Integrations
- [ ] Database storage (SQLite, PostgreSQL)
- [ ] REST API wrapper
- [ ] Slack/Discord bot
- [ ] Chrome extension

---

## 🏆 Success Metrics

For the use case (Aruzhan Abil):
- ✅ Finds research papers
- ✅ Discovers Columbia news article
- ✅ Locates other web mentions
- ✅ Aggregates all in one place
- ✅ Exports searchable JSON

---

## 📚 Learning Resources

### APIs Used
- [SerpAPI Documentation](https://serpapi.com/docs)
- [scholarly Documentation](https://scholarly.readthedocs.io/)
- [arXiv API Documentation](https://arxiv.org/help/api)

### Python Libraries
- [requests Documentation](https://requests.readthedocs.io/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 🎓 Project Statistics

| Metric | Value |
|--------|-------|
| Core modules | 3 (papers, news, web) |
| Total files | 10 |
| Lines of code | ~1,500+ |
| External APIs | 3 (Scholar, arXiv, SerpAPI) |
| Search sources | 10+ |
| Dependencies | 6 packages |

---

## 🤝 Usage Scenarios

### Scenario 1: Academic Research
**Goal**: Find papers by a researcher
**Use**: `search_papers.py` module
**Output**: Publications, citations, collaborators

### Scenario 2: Background Check
**Goal**: Comprehensive online presence
**Use**: Full `person_search.py`
**Output**: Papers, news, web mentions, social profiles

### Scenario 3: Media Mentions
**Goal**: Find where someone was featured
**Use**: `search_news.py` + `search_web.py`
**Output**: Articles, interviews, podcast appearances

### Scenario 4: Recruitment
**Goal**: Evaluate candidate's public profile
**Use**: All modules
**Output**: Complete digital footprint

---

## 📞 Support & Maintenance

### Self-Service
1. Check `QUICKSTART.md` for setup
2. Review `README.md` for details
3. Examine `example_search.py` for usage
4. Read inline code comments

### Troubleshooting
- Most issues covered in README.md
- Check API quotas and keys
- Verify internet connection
- Update dependencies

---

**Built for research, discovery, and due diligence** 🔍

