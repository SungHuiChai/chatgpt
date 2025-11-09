"""
Module for general web searches using Tavily API.
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time


class WebSearcher:
    """Perform general web searches for a person using Tavily API."""
    
    def __init__(self, tavily_api_key: str = None):
        """
        Initialize the web searcher.
        
        Args:
            tavily_api_key: Optional API key for Tavily (recommended for best results)
        """
        self.tavily_api_key = tavily_api_key
    
    def search_tavily(self, person_name: str, max_results: int = 10, 
                     additional_keywords: str = None) -> List[Dict]:
        """
        Perform a search using Tavily API.
        
        Args:
            person_name: Full name of the person to search for
            max_results: Maximum number of results to return
            additional_keywords: Optional additional search terms
            
        Returns:
            List of dictionaries containing search result information
        """
        results = []
        
        if not self.tavily_api_key:
            print("⚠ No Tavily API key provided. Using basic search (limited results).")
            return self._search_basic(person_name, max_results, additional_keywords)
        
        try:
            from tavily import TavilyClient
            
            query = f'"{person_name}"'
            if additional_keywords:
                query += f" {additional_keywords}"
            
            print(f"🔍 Searching with Tavily for: {query}")
            
            tavily_client = TavilyClient(api_key=self.tavily_api_key)
            
            response = tavily_client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced",  # Use advanced search for better results
                include_raw_content=False
            )
            
            if response and 'results' in response:
                tavily_results = response['results']
                print(f"✓ Found {len(tavily_results)} results")
                
                for item in tavily_results:
                    result_info = {
                        'title': item.get('title', 'N/A'),
                        'url': item.get('url', 'N/A'),
                        'snippet': item.get('content', 'N/A'),
                        'score': item.get('score', 0),
                        'source': 'Tavily Search'
                    }
                    results.append(result_info)
                    print(f"  🔗 {result_info['title']}")
            else:
                print(f"⚠ No results found")
                
        except ImportError:
            print("❌ Tavily library not installed. Run: pip install tavily-python")
            return self._search_basic(person_name, max_results, additional_keywords)
        except Exception as e:
            print(f"❌ Error with Tavily API: {e}")
            print("ℹ Falling back to basic search...")
            return self._search_basic(person_name, max_results, additional_keywords)
        
        return results
    
    def _search_basic(self, person_name: str, max_results: int = 10,
                     additional_keywords: str = None) -> List[Dict]:
        """
        Basic web search without API (web scraping).
        Fallback when Tavily API is not available.
        Note: This is less reliable and may be blocked.
        """
        results = []
        try:
            query = person_name.replace(' ', '+')
            if additional_keywords:
                query += '+' + additional_keywords.replace(' ', '+')
            
            print(f"🔍 Performing basic web search for: {person_name}")
            
            url = f"https://www.google.com/search?q={query}&num={max_results}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find search result divs
                search_results = soup.find_all('div', class_='g')[:max_results]
                
                if search_results:
                    print(f"✓ Found {len(search_results)} results")
                    
                    for i, item in enumerate(search_results, 1):
                        try:
                            title_elem = item.find('h3')
                            title = title_elem.text if title_elem else 'N/A'
                            
                            link_elem = item.find('a')
                            link = link_elem.get('href', 'N/A') if link_elem else 'N/A'
                            
                            snippet_elem = item.find('div', class_='VwiC3b')
                            if not snippet_elem:
                                snippet_elem = item.find('span', class_='aCOpRe')
                            snippet = snippet_elem.text if snippet_elem else 'N/A'
                            
                            result_info = {
                                'title': title,
                                'url': link,
                                'snippet': snippet,
                                'score': 1.0 - (i * 0.05),  # Simple relevance score
                                'source': 'Basic Search'
                            }
                            results.append(result_info)
                            print(f"  🔗 {title}")
                        except Exception as e:
                            continue
                else:
                    print(f"⚠ No results found")
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error in basic search: {e}")
        
        return results
    
    def search_news(self, person_name: str, max_results: int = 5) -> List[Dict]:
        """
        Search for news articles about a person using Tavily.
        
        Args:
            person_name: Full name of the person to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing news article information
        """
        if not self.tavily_api_key:
            print("⚠ No Tavily API key. Skipping news search.")
            return []
        
        try:
            from tavily import TavilyClient
            
            print(f"🔍 Searching for news about {person_name}...")
            
            tavily_client = TavilyClient(api_key=self.tavily_api_key)
            
            response = tavily_client.search(
                query=f'"{person_name}" news OR article OR featured',
                max_results=max_results,
                search_depth="advanced",
                topic="news"  # Focus on news content
            )
            
            results = []
            if response and 'results' in response:
                tavily_results = response['results']
                print(f"✓ Found {len(tavily_results)} news articles")
                
                for item in tavily_results:
                    article_info = {
                        'title': item.get('title', 'N/A'),
                        'url': item.get('url', 'N/A'),
                        'snippet': item.get('content', 'N/A'),
                        'score': item.get('score', 0),
                        'source': 'Tavily News'
                    }
                    results.append(article_info)
                    print(f"  📰 {article_info['title']}")
            else:
                print(f"⚠ No news articles found")
            
            return results
            
        except Exception as e:
            print(f"❌ Error searching news: {e}")
            return []
    
    def search_academic(self, person_name: str, max_results: int = 5) -> List[Dict]:
        """
        Search for academic content and research mentions.
        
        Args:
            person_name: Full name of the person to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing academic content
        """
        return self.search_tavily(
            person_name, 
            max_results, 
            additional_keywords="research OR paper OR publication OR scholar OR university"
        )
    
    def search_social_media(self, person_name: str, platforms: List[str] = None) -> Dict[str, List[Dict]]:
        """
        Search for social media profiles and mentions.
        
        Args:
            person_name: Full name of the person to search for
            platforms: List of platforms to search (default: common platforms)
            
        Returns:
            Dictionary with platform names as keys and results as values
        """
        if platforms is None:
            # Common platforms (excluding LinkedIn, X, GitHub as already scraped)
            platforms = [
                'medium.com',
                'dev.to',
                'stackoverflow.com',
                'reddit.com',
                'youtube.com'
            ]
        
        print(f"🔍 Searching social media platforms for {person_name}...")
        
        results = {}
        for platform in platforms:
            try:
                platform_results = self.search_tavily(
                    person_name,
                    max_results=3,
                    additional_keywords=f"site:{platform}"
                )
                
                if platform_results:
                    results[platform] = platform_results
                    print(f"  ✓ Found {len(platform_results)} results on {platform}")
                else:
                    print(f"  ⚠ No results on {platform}")
                
                time.sleep(0.5)  # Be polite
                
            except Exception as e:
                print(f"  ❌ Error searching {platform}: {e}")
        
        return results
    
    def search_podcasts_interviews(self, person_name: str, max_results: int = 5) -> List[Dict]:
        """
        Search for podcast appearances and interviews.
        
        Args:
            person_name: Full name of the person to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing podcast/interview information
        """
        print(f"🔍 Searching for podcasts and interviews featuring {person_name}...")
        
        return self.search_tavily(
            person_name,
            max_results=max_results,
            additional_keywords="podcast OR interview OR talk OR guest OR speaker"
        )
    
    def search_all(self, person_name: str, max_results: int = 10,
                   include_social: bool = False) -> Dict[str, any]:
        """
        Perform comprehensive web search for a person using Tavily.
        
        Args:
            person_name: Full name of the person to search for
            max_results: Maximum number of results per search type
            include_social: Whether to include social media search
            
        Returns:
            Dictionary with results from various search types
        """
        results = {
            'general_search': self.search_tavily(person_name, max_results),
            'news': self.search_news(person_name, max_results=5),
            'academic': self.search_academic(person_name, max_results=5),
            'podcasts_interviews': self.search_podcasts_interviews(person_name, max_results=5)
        }
        
        if include_social:
            results['social_media'] = self.search_social_media(person_name)
        
        return results


if __name__ == "__main__":
    # Example usage
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    tavily_api_key = os.getenv('TAVILY_API_KEY')
    searcher = WebSearcher(tavily_api_key=tavily_api_key)
    
    results = searcher.search_all("Aruzhan Abil", max_results=5, include_social=False)
    
    print("\n" + "="*80)
    print("WEB SEARCH RESULTS")
    print("="*80)
    
    for search_type, search_results in results.items():
        if isinstance(search_results, list):
            print(f"\n{search_type.upper().replace('_', ' ')}: {len(search_results)} results")
            print("-"*80)
            for i, result in enumerate(search_results, 1):
                print(f"\n{i}. {result['title']}")
                print(f"   URL: {result['url']}")
                print(f"   Snippet: {result.get('snippet', 'N/A')[:100]}...")
        else:
            print(f"\n{search_type.upper().replace('_', ' ')}:")
            print("-"*80)
            for platform, items in search_results.items():
                print(f"  {platform}: {len(items)} results")
