"""
Example script showing how to use the Person Search Tool.

This demonstrates searching for a person across multiple sources.
"""
import os
from dotenv import load_dotenv
from person_search import PersonSearcher


def main():
    """Run example searches."""
    
    # Load environment variables from .env file (if exists)
    load_dotenv()
    
    # Get API key from environment (optional)
    tavily_api_key = os.getenv('TAVILY_API_KEY')
    
    if tavily_api_key:
        print("✅ Tavily API key found - using enhanced search")
    else:
        print("⚠️  No Tavily API key - using basic search (limited results)")
        print("   To get better results, create a .env file with TAVILY_API_KEY")
        print()
    
    # Initialize the person searcher
    searcher = PersonSearcher(tavily_api_key=tavily_api_key)
    
    # Example 1: Search for a specific person
    print("\n" + "="*80)
    print("EXAMPLE 1: Searching for Aruzhan Abil")
    print("="*80)
    
    results = searcher.search(
        person_name="Aruzhan Abil",
        university="Columbia",  # Her university affiliation
        max_results_per_source=10,
        include_social=False,
        search_papers=True,
        search_news=True,
        search_web=True
    )
    
    # Display summary
    searcher.print_summary(results)
    
    # Display detailed results (first 3 items per category)
    searcher.print_detailed_results(results, max_display=3)
    
    # Save results to JSON file
    searcher.save_results(results)
    
    print("\n✨ Example search complete!")
    print("\nTo search for a different person, modify this script or run:")
    print("  python person_search.py")
    

def example_papers_only():
    """Example: Search only for academic papers."""
    from search_papers import PaperSearcher
    
    print("\n" + "="*80)
    print("EXAMPLE: Papers Only Search")
    print("="*80 + "\n")
    
    searcher = PaperSearcher()
    results = searcher.search_all("Aruzhan Abil", max_results=5)
    
    for source, papers in results.items():
        if papers:
            print(f"\n{source}: {len(papers)} papers found")
            for i, paper in enumerate(papers[:3], 1):
                print(f"  {i}. {paper['title']} ({paper['year']})")


def example_news_only():
    """Example: Search only for news articles."""
    from search_news import NewsSearcher
    
    print("\n" + "="*80)
    print("EXAMPLE: News Only Search")
    print("="*80 + "\n")
    
    load_dotenv()
    
    searcher = NewsSearcher()
    results = searcher.search_all("Aruzhan Abil", university="Columbia")
    
    for source, articles in results.items():
        if articles:
            print(f"\n{source}: {len(articles)} articles found")
            for i, article in enumerate(articles[:3], 1):
                print(f"  {i}. {article['title']}")


def example_custom_search():
    """Example: Custom search with specific parameters."""
    load_dotenv()
    tavily_api_key = os.getenv('TAVILY_API_KEY')
    
    print("\n" + "="*80)
    print("EXAMPLE: Custom Search Parameters")
    print("="*80 + "\n")
    
    searcher = PersonSearcher(tavily_api_key=tavily_api_key)
    
    # Search with custom parameters
    results = searcher.search(
        person_name="Aruzhan Abil",
        university=None,  # Don't filter by university
        max_results_per_source=5,  # Fewer results per source
        include_social=True,  # Include social media
        search_papers=True,
        search_news=False,  # Skip news
        search_web=True
    )
    
    searcher.print_summary(results)


if __name__ == "__main__":
    # Run the main example
    main()
    
    # Uncomment to run other examples:
    # example_papers_only()
    # example_news_only()
    # example_custom_search()

