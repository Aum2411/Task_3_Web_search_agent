"""
Web search module using Serper.dev API
"""
import requests
import os
from typing import List, Dict, Optional


class WebSearcher:
    """Handles web search operations using Serper.dev API"""
    
    def __init__(self, api_key: str):
        """
        Initialize the WebSearcher with API key
        
        Args:
            api_key: Serper.dev API key
        """
        self.api_key = api_key
        self.base_url = "https://google.serper.dev/search"
    
    def search(self, query: str, num_results: int = 10) -> Dict:
        """
        Perform a web search
        
        Args:
            query: Search query string
            num_results: Number of results to retrieve (default: 10)
            
        Returns:
            Dictionary containing search results
        """
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query,
            'num': num_results
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
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
