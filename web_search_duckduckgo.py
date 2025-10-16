"""
Web search module using DuckDuckGo (no API key required)
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import urllib.parse


class WebSearcher:
    """Handles web search operations using DuckDuckGo HTML search"""
    
    def __init__(self):
        """Initialize the WebSearcher"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search(self, query: str, num_results: int = 10) -> Dict:
        """
        Perform a web search using DuckDuckGo Lite (less likely to block bots)
        """
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://lite.duckduckgo.com/lite/?q={encoded_query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            # Each result is in a <tr> with class 'result'
            for tr in soup.find_all('tr', class_='result'):
                try:
                    a = tr.find('a', href=True)
                    title = a.get_text(strip=True) if a else "No title"
                    link = a['href'] if a else ''
                    snippet = tr.find('td', class_='snippet')
                    snippet_text = snippet.get_text(strip=True) if snippet else "No description available"
                    if title and link:
                        results.append({
                            'title': title,
                            'link': link,
                            'snippet': snippet_text
                        })
                except Exception:
                    continue
            return {'organic': results[:num_results]}
        except Exception as e:
            print(f"Search error: {e}")
            return {
                'error': str(e),
                'organic': []
            }
    
    def format_results(self, search_results: Dict) -> List[Dict[str, str]]:
        """
        Format search results into a clean structure
        
        Args:
            search_results: Raw search results from search
            
        Returns:
            List of formatted search results
        """
        formatted_results = []
        
        # Check if there's an error
        if 'error' in search_results:
            return [{
                'title': 'Search Error',
                'snippet': search_results['error'],
                'link': ''
            }]
        
        # Extract organic search results
        organic_results = search_results.get('organic', [])
        
        for result in organic_results:
            formatted_results.append({
                'title': result.get('title', 'No title'),
                'snippet': result.get('snippet', 'No description available'),
                'link': result.get('link', '')
            })
        
        return formatted_results
