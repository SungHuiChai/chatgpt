"""
Main orchestrator for comprehensive person search across multiple sources.
"""
import os
import json
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

from search_papers import PaperSearcher
from search_news import NewsSearcher
from search_web import WebSearcher


class PersonSearcher:
    """
    Comprehensive search engine for finding information about a person
    across academic papers, news articles, and web mentions.
    """
    
    def __init__(self, tavily_api_key: str = None):
        """
        Initialize the person searcher.
        
        Args:
            tavily_api_key: Optional Tavily API key for enhanced web search capabilities
        """
        self.tavily_api_key = tavily_api_key
        self.paper_searcher = PaperSearcher()
        self.news_searcher = NewsSearcher(serpapi_key=None)  # News uses basic search or Tavily
        self.web_searcher = WebSearcher(tavily_api_key=tavily_api_key)
    
    def search(self, person_name: str, university: str = None,
               max_results_per_source: int = 10,
               include_social: bool = False,
               search_papers: bool = True,
               search_news: bool = True,
               search_web: bool = True) -> Dict:
        """
        Perform comprehensive search for a person.
        
        Args:
            person_name: Full name of the person to search for
            university: Optional university affiliation for targeted news search
            max_results_per_source: Maximum results to retrieve from each source
            include_social: Whether to include social media searches
            search_papers: Whether to search for academic papers
            search_news: Whether to search for news articles
            search_web: Whether to perform general web search
            
        Returns:
            Dictionary containing all search results organized by category
        """
        print("="*80)
        print(f"COMPREHENSIVE SEARCH FOR: {person_name}")
        print("="*80)
        print()
        
        results = {
            'person_name': person_name,
            'search_timestamp': datetime.now().isoformat(),
            'papers': {},
            'news': {},
            'web': {},
            'summary': {}
        }
        
        # Search academic papers
        if search_papers:
            print("\n" + "🎓 SEARCHING ACADEMIC PAPERS...")
            print("="*80)
            try:
                paper_results = self.paper_searcher.search_all(person_name, max_results_per_source)
                results['papers'] = paper_results
                
                total_papers = sum(len(papers) for papers in paper_results.values())
                results['summary']['total_papers'] = total_papers
                print(f"\n✅ Total papers found: {total_papers}")
            except Exception as e:
                print(f"❌ Error searching papers: {e}")
                results['papers']['error'] = str(e)
        
        # Search news articles
        if search_news:
            print("\n" + "📰 SEARCHING NEWS ARTICLES...")
            print("="*80)
            try:
                news_results = self.news_searcher.search_all(person_name, university, max_results_per_source)
                results['news'] = news_results
                
                total_articles = sum(len(articles) for articles in news_results.values())
                results['summary']['total_news_articles'] = total_articles
                print(f"\n✅ Total news articles found: {total_articles}")
            except Exception as e:
                print(f"❌ Error searching news: {e}")
                results['news']['error'] = str(e)
        
        # Search web
        if search_web:
            print("\n" + "🌐 SEARCHING WEB...")
            print("="*80)
            try:
                web_results = self.web_searcher.search_all(person_name, max_results_per_source, include_social)
                results['web'] = web_results
                
                total_web_results = 0
                if 'general_search' in web_results:
                    total_web_results += len(web_results['general_search'])
                if 'podcasts_interviews' in web_results:
                    total_web_results += len(web_results['podcasts_interviews'])
                if 'social_media' in web_results:
                    total_web_results += sum(len(items) for items in web_results['social_media'].values())
                
                results['summary']['total_web_results'] = total_web_results
                print(f"\n✅ Total web results found: {total_web_results}")
            except Exception as e:
                print(f"❌ Error searching web: {e}")
                results['web']['error'] = str(e)
        
        return results
    
    def print_summary(self, results: Dict):
        """
        Print a formatted summary of search results.
        
        Args:
            results: Dictionary containing search results
        """
        print("\n" + "="*80)
        print(f"📊 SEARCH SUMMARY FOR: {results['person_name']}")
        print("="*80)
        
        summary = results.get('summary', {})
        
        print(f"\n🎓 Academic Papers: {summary.get('total_papers', 0)}")
        if results.get('papers'):
            for source, papers in results['papers'].items():
                if isinstance(papers, list):
                    print(f"   • {source.replace('_', ' ').title()}: {len(papers)}")
        
        print(f"\n📰 News Articles: {summary.get('total_news_articles', 0)}")
        if results.get('news'):
            for source, articles in results['news'].items():
                if isinstance(articles, list):
                    print(f"   • {source.replace('_', ' ').title()}: {len(articles)}")
        
        print(f"\n🌐 Web Results: {summary.get('total_web_results', 0)}")
        if results.get('web'):
            for source, items in results['web'].items():
                if isinstance(items, list):
                    print(f"   • {source.replace('_', ' ').title()}: {len(items)}")
                elif isinstance(items, dict):
                    for platform, platform_items in items.items():
                        print(f"   • {platform}: {len(platform_items)}")
        
        print("\n" + "="*80)
    
    def print_detailed_results(self, results: Dict, max_display: int = 5):
        """
        Print detailed search results.
        
        Args:
            results: Dictionary containing search results
            max_display: Maximum number of items to display per category
        """
        print("\n" + "="*80)
        print(f"📋 DETAILED RESULTS FOR: {results['person_name']}")
        print("="*80)
        
        # Academic Papers
        if results.get('papers'):
            print("\n🎓 ACADEMIC PAPERS")
            print("-"*80)
            for source, papers in results['papers'].items():
                if isinstance(papers, list) and papers:
                    print(f"\n{source.upper().replace('_', ' ')}:")
                    for i, paper in enumerate(papers[:max_display], 1):
                        print(f"\n{i}. {paper.get('title', 'N/A')}")
                        print(f"   Authors: {paper.get('authors', 'N/A')}")
                        print(f"   Year: {paper.get('year', 'N/A')}")
                        print(f"   Venue: {paper.get('venue', 'N/A')}")
                        if paper.get('citations') != 'N/A':
                            print(f"   Citations: {paper.get('citations', 0)}")
                        print(f"   URL: {paper.get('url', 'N/A')}")
                        if paper.get('abstract') and paper['abstract'] != 'N/A':
                            abstract = paper['abstract'][:200] + "..." if len(paper['abstract']) > 200 else paper['abstract']
                            print(f"   Abstract: {abstract}")
        
        # News Articles
        if results.get('news'):
            print("\n\n📰 NEWS ARTICLES")
            print("-"*80)
            for source, articles in results['news'].items():
                if isinstance(articles, list) and articles:
                    print(f"\n{source.upper().replace('_', ' ')}:")
                    for i, article in enumerate(articles[:max_display], 1):
                        print(f"\n{i}. {article.get('title', 'N/A')}")
                        print(f"   Source: {article.get('source', 'N/A')}")
                        print(f"   Date: {article.get('date', 'N/A')}")
                        print(f"   URL: {article.get('url', 'N/A')}")
                        if article.get('snippet') and article['snippet'] != 'N/A':
                            snippet = article['snippet'][:150] + "..." if len(article['snippet']) > 150 else article['snippet']
                            print(f"   Snippet: {snippet}")
        
        # Web Results
        if results.get('web'):
            print("\n\n🌐 WEB RESULTS")
            print("-"*80)
            for source, items in results['web'].items():
                if isinstance(items, list) and items:
                    print(f"\n{source.upper().replace('_', ' ')}:")
                    for i, item in enumerate(items[:max_display], 1):
                        print(f"\n{i}. {item.get('title', 'N/A')}")
                        print(f"   URL: {item.get('url', 'N/A')}")
                        if item.get('snippet') and item['snippet'] != 'N/A':
                            snippet = item['snippet'][:150] + "..." if len(item['snippet']) > 150 else item['snippet']
                            print(f"   Snippet: {snippet}")
                elif isinstance(items, dict):
                    for platform, platform_items in items.items():
                        if platform_items:
                            print(f"\n{platform.upper()}:")
                            for i, item in enumerate(platform_items[:max_display], 1):
                                print(f"\n{i}. {item.get('title', 'N/A')}")
                                print(f"   URL: {item.get('url', 'N/A')}")
        
        print("\n" + "="*80)
    
    def save_results(self, results: Dict, filename: str = None):
        """
        Save search results to a JSON file.
        
        Args:
            results: Dictionary containing search results
            filename: Optional custom filename (default: person_name_timestamp.json)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            person_name_clean = results['person_name'].replace(' ', '_').lower()
            filename = f"search_results_{person_name_clean}_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Results saved to: {filename}")
        except Exception as e:
            print(f"\n❌ Error saving results: {e}")


def main():
    """Main function to run the person search."""
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment
    tavily_api_key = os.getenv('TAVILY_API_KEY')
    
    if not tavily_api_key:
        print("⚠️  Warning: No TAVILY_API_KEY found in .env file.")
        print("   Basic search will be used with limited results.")
        print("   To get better results, sign up at: https://tavily.com/")
        print()
    
    # Initialize searcher
    searcher = PersonSearcher(tavily_api_key=tavily_api_key)
    
    # Example: Search for Aruzhan Abil
    person_name = "Aruzhan Abil"
    university = "Columbia"  # Her university affiliation
    
    # Perform comprehensive search
    results = searcher.search(
        person_name=person_name,
        university=university,
        max_results_per_source=10,
        include_social=False,  # Set to True to include social media
        search_papers=True,
        search_news=True,
        search_web=True
    )
    
    # Print summary
    searcher.print_summary(results)
    
    # Print detailed results
    searcher.print_detailed_results(results, max_display=5)
    
    # Save results to file
    searcher.save_results(results)
    
    print("\n✨ Search complete!")


if __name__ == "__main__":
    main()

