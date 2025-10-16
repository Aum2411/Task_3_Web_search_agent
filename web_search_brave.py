"""
Web search module using Brave Search API (no API key required for basic use)
"""
import requests
from typing import List, Dict

class WebSearcher:
    """Handles web search operations using Brave Search API"""
    def __init__(self):
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

    def search(self, query: str, num_results: int = 10) -> Dict:
        """
        Perform a web search using Brave Search API
        Args:
            query: Search query string
            num_results: Number of results to retrieve (default: 10)
        Returns:
            Dictionary containing search results
        """
        try:
            params = {
                'q': query,
                'count': num_results
            }
            url = f"https://api.search.brave.com/res/v1/web/search?q={query}&count={num_results}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = []
            for item in data.get('web', {}).get('results', []):
                results.append({
                    'title': item.get('title', 'No title'),
                    'link': item.get('url', ''),
                    'snippet': item.get('description', 'No description available')
                })
            return {'organic': results}
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
            search_results: Raw search results from API
        Returns:
            List of formatted search results
        """
        formatted_results = []
        if 'error' in search_results:
            return [{
                'title': 'Search Error',
                'snippet': search_results['error'],
                'link': ''
            }]
        organic_results = search_results.get('organic', [])
        for result in organic_results:
            formatted_results.append({
                'title': result.get('title', 'No title'),
                'snippet': result.get('snippet', 'No description available'),
                'link': result.get('link', '')
            })
        return formatted_results
