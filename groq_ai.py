"""
Groq AI module for processing and summarizing search results
"""
from groq import Groq
from typing import List, Dict


class GroqAI:
    """Handles AI operations using Groq API"""
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        """
        Initialize the GroqAI client
        
        Args:
            api_key: Groq API key
            model: Model to use (default: llama-3.1-70b-versatile)
        """
        self.client = Groq(api_key=api_key)
        self.model = model
    
    def summarize_results(self, query: str, search_results: List[Dict[str, str]]) -> str:
        """
        Summarize and filter search results using AI
        
        Args:
            query: Original user query
            search_results: List of search results to process
            
        Returns:
            AI-generated summary and analysis
        """
        # Format search results into a readable text
        results_text = self._format_results_for_prompt(search_results)
        
        # Create prompt for the AI
        prompt = f"""You are a helpful research assistant. A user has searched for: "{query}"

Here are the search results:

{results_text}

Please provide a comprehensive, well-organized summary that:
1. Directly answers the user's query based on the search results
2. Highlights the most relevant and important information
3. Synthesizes information from multiple sources
4. Includes specific facts, data, or insights when available
5. Mentions any contradictions or different perspectives if present
6. Cites which sources provided key information (by number)

Keep the response clear, concise, and informative."""

        try:
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert research assistant who excels at analyzing and summarizing information from multiple sources."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=2000
            )
            
            return chat_completion.choices[0].message.content
        
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def _format_results_for_prompt(self, search_results: List[Dict[str, str]]) -> str:
        """
        Format search results into a text block for the AI prompt
        
        Args:
            search_results: List of search results
            
        Returns:
            Formatted string of results
        """
        formatted = []
        
        for i, result in enumerate(search_results, 1):
            formatted.append(f"[{i}] {result['title']}")
            formatted.append(f"    {result['snippet']}")
            formatted.append(f"    URL: {result['link']}")
            formatted.append("")
        
        return "\n".join(formatted)
    
    def filter_relevant_results(self, query: str, search_results: List[Dict[str, str]], 
                               top_n: int = 5) -> List[Dict[str, str]]:
        """
        Use AI to filter and rank the most relevant search results
        
        Args:
            query: Original user query
            search_results: List of search results
            top_n: Number of top results to return
            
        Returns:
            Filtered list of most relevant results
        """
        if len(search_results) <= top_n:
            return search_results
        
        results_text = self._format_results_for_prompt(search_results)
        
        prompt = f"""Given the user query: "{query}"

And these search results:
{results_text}

Please identify the {top_n} most relevant result numbers (just the numbers) that best answer the query.
Respond with only the numbers separated by commas, like: 1,3,5,7,9"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=50
            )
            
            # Parse the response to get result indices
            response = chat_completion.choices[0].message.content.strip()
            indices = [int(x.strip()) - 1 for x in response.split(',') if x.strip().isdigit()]
            
            # Return filtered results
            return [search_results[i] for i in indices if 0 <= i < len(search_results)]
        
        except Exception as e:
            # If filtering fails, return top N results
            return search_results[:top_n]
