"""
Configuration file for Person Search Tool.

Copy this file to config.py and add your actual API keys.
"""

# Tavily API Configuration
# Sign up at: https://tavily.com/ (Free tier: 1,000 searches/month)
# Tavily is an AI-powered search API designed for LLMs and AI agents
# For better and more reliable web search results, it's recommended to use Tavily
TAVILY_API_KEY = None  # Replace with your actual API key or set as environment variable

# Search Settings
DEFAULT_MAX_RESULTS = 10  # Default maximum results per source
SEARCH_TIMEOUT = 10  # Timeout for HTTP requests in seconds
RATE_LIMIT_DELAY = 1  # Delay between requests in seconds (be polite to servers)

# University News Sites (add more as needed)
UNIVERSITY_NEWS_SITES = {
    'columbia': 'https://news.columbia.edu/?s=',
    'mit': 'https://news.mit.edu/search/',
    'stanford': 'https://news.stanford.edu/search/',
    'harvard': 'https://news.harvard.edu/gazette/?s=',
    'yale': 'https://news.yale.edu/search/',
    'princeton': 'https://www.princeton.edu/search?q=',
    'cornell': 'https://news.cornell.edu/?s=',
    'upenn': 'https://penntoday.upenn.edu/?s='
}

# Social Media Platforms to Search (excluding LinkedIn, X, GitHub which you already scrape)
SOCIAL_MEDIA_PLATFORMS = [
    'medium.com',
    'dev.to',
    'stackoverflow.com',
    'reddit.com',
    'youtube.com'
]

# Search Filters
ENABLE_PAPERS = True  # Search for academic papers
ENABLE_NEWS = True    # Search for news articles
ENABLE_WEB = True     # Search general web
ENABLE_SOCIAL = False # Search social media platforms

