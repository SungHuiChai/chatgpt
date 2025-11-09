"""
Module for searching news articles and media mentions.
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time


class NewsSearcher:
    """Search for news articles and media mentions of a person."""
    
    def __init__(self, serpapi_key: str = None):
        """
        Initialize the news searcher.
        
        Args:
            serpapi_key: Optional API key for SerpAPI (for Google News search)
        """
        self.serpapi_key = serpapi_key
    
    def search_google_news(self, person_name: str, max_results: int = 10) -> List[Dict]:
        """
        Search Google News for mentions of a person.
        
        Args:
            person_name: Full name of the person to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing news article information
        """
        articles = []
        
        if not self.serpapi_key:
            print("⚠ No SerpAPI key provided. Using basic search (limited results).")
            return self._search_google_news_basic(person_name, max_results)
        
        try:
            print(f"🔍 Searching Google News for {person_name}...")
            
            from serpapi import GoogleSearch
            
            params = {
                "q": f'"{person_name}"',
                "tbm": "nws",  # News search
                "api_key": self.serpapi_key,
                "num": max_results
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            news_results = results.get("news_results", [])
            
            if news_results:
                print(f"✓ Found {len(news_results)} news articles")
                
                for item in news_results:
                    article_info = {
                        'title': item.get('title', 'N/A'),
                        'source': item.get('source', {}).get('name', 'N/A'),
                        'date': item.get('date', 'N/A'),
                        'snippet': item.get('snippet', 'N/A'),
                        'url': item.get('link', 'N/A'),
                        'thumbnail': item.get('thumbnail', 'N/A'),
                        'search_type': 'Google News'
                    }
                    articles.append(article_info)
                    print(f"  📰 {article_info['title']} - {article_info['source']}")
            else:
                print(f"⚠ No news articles found for '{person_name}'")
                
        except Exception as e:
            print(f"❌ Error searching Google News: {e}")
            print("ℹ Falling back to basic search...")
            return self._search_google_news_basic(person_name, max_results)
        
        return articles
    
    def _search_google_news_basic(self, person_name: str, max_results: int = 10) -> List[Dict]:
        """
        Basic Google News search without API (web scraping).
        Note: This is less reliable and may be blocked by Google.
        """
        articles = []
        try:
            print(f"🔍 Performing basic Google News search for {person_name}...")
            
            # Google News search URL
            query = person_name.replace(' ', '+')
            url = f"https://www.google.com/search?q={query}&tbm=nws"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find news result divs (structure may change)
                news_items = soup.find_all('div', class_='SoaBEf')[:max_results]
                
                if news_items:
                    print(f"✓ Found {len(news_items)} news articles")
                    
                    for item in news_items:
                        try:
                            title_elem = item.find('div', role='heading')
                            title = title_elem.text if title_elem else 'N/A'
                            
                            link_elem = item.find('a')
                            link = link_elem.get('href', 'N/A') if link_elem else 'N/A'
                            
                            source_elem = item.find('div', class_='MgUUmf')
                            source = source_elem.text if source_elem else 'N/A'
                            
                            snippet_elem = item.find('div', class_='GI74Re')
                            snippet = snippet_elem.text if snippet_elem else 'N/A'
                            
                            article_info = {
                                'title': title,
                                'source': source,
                                'date': 'N/A',
                                'snippet': snippet,
                                'url': link,
                                'thumbnail': 'N/A',
                                'search_type': 'Google News (Basic)'
                            }
                            articles.append(article_info)
                            print(f"  📰 {title}")
                        except Exception as e:
                            continue
                else:
                    print(f"⚠ No news articles found (basic search)")
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error in basic Google News search: {e}")
        
        return articles
    
    def search_university_news(self, person_name: str, university: str = None) -> List[Dict]:
        """
        Search university news sites for mentions.
        
        Args:
            person_name: Full name of the person to search for
            university: University name (e.g., "Columbia", "MIT")
            
        Returns:
            List of dictionaries containing article information
        """
        articles = []
        
        # University news site search URLs
        university_sites = {
            'columbia': 'https://news.columbia.edu/?s=',
            'mit': 'https://news.mit.edu/search/',
            'stanford': 'https://news.stanford.edu/search/',
            'harvard': 'https://news.harvard.edu/gazette/?s='
        }
        
        if university:
            sites = {university.lower(): university_sites.get(university.lower())}
            if not sites[university.lower()]:
                print(f"⚠ University '{university}' not in predefined list. Using generic search.")
                return articles
        else:
            sites = university_sites
        
        for uni_name, base_url in sites.items():
            if not base_url:
                continue
                
            try:
                print(f"🔍 Searching {uni_name.upper()} news for {person_name}...")
                
                query = person_name.replace(' ', '+')
                url = base_url + query
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Generic search for article links
                    links = soup.find_all('a', href=True)
                    
                    found_count = 0
                    for link in links[:20]:  # Check first 20 links
                        href = link.get('href', '')
                        text = link.text.strip()
                        
                        # Filter for likely article links
                        if text and len(text) > 20 and person_name.lower() in text.lower():
                            article_info = {
                                'title': text,
                                'source': f"{uni_name.upper()} News",
                                'date': 'N/A',
                                'snippet': text[:200],
                                'url': href if href.startswith('http') else base_url.split('?')[0].rstrip('/') + href,
                                'thumbnail': 'N/A',
                                'search_type': 'University News'
                            }
                            articles.append(article_info)
                            found_count += 1
                            print(f"  📰 {text[:80]}...")
                    
                    if found_count == 0:
                        print(f"  ⚠ No articles found on {uni_name.upper()} news")
                else:
                    print(f"  ❌ Error: HTTP {response.status_code}")
                    
                time.sleep(1)  # Be polite to servers
                
            except Exception as e:
                print(f"  ❌ Error searching {uni_name.upper()} news: {e}")
        
        return articles
    
    def search_all(self, person_name: str, university: str = None, max_results: int = 10) -> Dict[str, List[Dict]]:
        """
        Search all news sources for a person.
        
        Args:
            person_name: Full name of the person to search for
            university: Optional university name for targeted search
            max_results: Maximum number of results per source
            
        Returns:
            Dictionary with results from each source
        """
        results = {
            'google_news': self.search_google_news(person_name, max_results),
            'university_news': self.search_university_news(person_name, university)
        }
        
        return results


if __name__ == "__main__":
    # Example usage
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    serpapi_key = os.getenv('SERPAPI_KEY')
    searcher = NewsSearcher(serpapi_key=serpapi_key)
    
    results = searcher.search_all("Aruzhan Abil", university="Columbia", max_results=5)
    
    print("\n" + "="*80)
    print("NEWS SEARCH RESULTS")
    print("="*80)
    
    for source, articles in results.items():
        print(f"\n{source.upper().replace('_', ' ')}: {len(articles)} articles found")
        print("-"*80)
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Source: {article['source']}")
            print(f"   URL: {article['url']}")

