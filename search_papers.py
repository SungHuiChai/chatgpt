"""
Module for searching academic papers across multiple sources.
"""
import requests
from bs4 import BeautifulSoup
from scholarly import scholarly
import time
from typing import List, Dict


class PaperSearcher:
    """Search for academic papers using Google Scholar and arXiv."""
    
    def __init__(self):
        self.results = []
    
    def search_google_scholar(self, person_name: str, max_results: int = 10) -> List[Dict]:
        """
        Search Google Scholar for papers by a person.
        
        Args:
            person_name: Full name of the person to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing paper information
        """
        papers = []
        try:
            print(f"🔍 Searching Google Scholar for papers by {person_name}...")
            
            # Search for the author
            search_query = scholarly.search_author(person_name)
            
            # Get the first author match
            try:
                author = next(search_query)
                author = scholarly.fill(author)
                
                print(f"✓ Found author: {author.get('name', 'Unknown')}")
                print(f"  Affiliation: {author.get('affiliation', 'N/A')}")
                print(f"  Total citations: {author.get('citedby', 0)}")
                
                # Get publications
                publications = author.get('publications', [])[:max_results]
                
                for pub in publications:
                    try:
                        pub_filled = scholarly.fill(pub)
                        paper_info = {
                            'title': pub_filled.get('bib', {}).get('title', 'N/A'),
                            'authors': pub_filled.get('bib', {}).get('author', 'N/A'),
                            'year': pub_filled.get('bib', {}).get('pub_year', 'N/A'),
                            'venue': pub_filled.get('bib', {}).get('venue', 'N/A'),
                            'citations': pub_filled.get('num_citations', 0),
                            'url': pub_filled.get('pub_url', pub_filled.get('eprint_url', 'N/A')),
                            'abstract': pub_filled.get('bib', {}).get('abstract', 'N/A'),
                            'source': 'Google Scholar'
                        }
                        papers.append(paper_info)
                        print(f"  📄 {paper_info['title']} ({paper_info['year']})")
                    except Exception as e:
                        print(f"  ⚠ Error fetching publication details: {e}")
                        continue
                        
            except StopIteration:
                print(f"⚠ No author found for '{person_name}' on Google Scholar")
                
        except Exception as e:
            print(f"❌ Error searching Google Scholar: {e}")
        
        return papers
    
    def search_arxiv(self, person_name: str, max_results: int = 10) -> List[Dict]:
        """
        Search arXiv for papers by a person.
        
        Args:
            person_name: Full name of the person to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing paper information
        """
        papers = []
        try:
            print(f"🔍 Searching arXiv for papers by {person_name}...")
            
            # arXiv API endpoint
            base_url = 'http://export.arxiv.org/api/query?'
            
            # Format the search query
            query = f'search_query=au:"{person_name}"&start=0&max_results={max_results}'
            url = base_url + query
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                entries = soup.find_all('entry')
                
                if entries:
                    print(f"✓ Found {len(entries)} papers on arXiv")
                    
                    for entry in entries:
                        title = entry.find('title').text.strip().replace('\n', ' ')
                        authors = [author.find('name').text for author in entry.find_all('author')]
                        published = entry.find('published').text[:4]  # Get year
                        summary = entry.find('summary').text.strip().replace('\n', ' ')
                        link = entry.find('id').text
                        
                        paper_info = {
                            'title': title,
                            'authors': ', '.join(authors),
                            'year': published,
                            'venue': 'arXiv',
                            'citations': 'N/A',
                            'url': link,
                            'abstract': summary,
                            'source': 'arXiv'
                        }
                        papers.append(paper_info)
                        print(f"  📄 {title} ({published})")
                else:
                    print(f"⚠ No papers found for '{person_name}' on arXiv")
            else:
                print(f"❌ Error: arXiv API returned status code {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error searching arXiv: {e}")
        
        return papers
    
    def search_all(self, person_name: str, max_results: int = 10) -> Dict[str, List[Dict]]:
        """
        Search all paper sources for a person.
        
        Args:
            person_name: Full name of the person to search for
            max_results: Maximum number of results per source
            
        Returns:
            Dictionary with results from each source
        """
        results = {
            'google_scholar': self.search_google_scholar(person_name, max_results),
            'arxiv': self.search_arxiv(person_name, max_results)
        }
        
        return results


if __name__ == "__main__":
    # Example usage
    searcher = PaperSearcher()
    results = searcher.search_all("Aruzhan Abil", max_results=5)
    
    print("\n" + "="*80)
    print("SEARCH RESULTS")
    print("="*80)
    
    for source, papers in results.items():
        print(f"\n{source.upper().replace('_', ' ')}: {len(papers)} papers found")
        print("-"*80)
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   Authors: {paper['authors']}")
            print(f"   Year: {paper['year']}")
            print(f"   Venue: {paper['venue']}")
            print(f"   URL: {paper['url']}")

