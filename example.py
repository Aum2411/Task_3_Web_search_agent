"""
Simple example script demonstrating the Web Search Agent
"""
import os
from dotenv import load_dotenv
from web_search_duckduckgo import WebSearcher
from groq_ai import GroqAI


def simple_example():
    """Simple example of using the search agent"""
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    if not groq_api_key:
        print("Error: Please set GROQ_API_KEY in .env file")
        return
    
    searcher = WebSearcher()  # No API key needed for DuckDuckGo
    ai = GroqAI(groq_api_key)
    
    print("✓ Using DuckDuckGo for web search (no API key required)\n")
    
    # Example query
    query = "What are the latest developments in artificial intelligence in 2025?"
    
    print(f"Searching for: {query}\n")
    
    # Step 1: Search the web
    print("Step 1: Searching the web...")
    raw_results = searcher.search(query, num_results=5)
    search_results = searcher.format_results(raw_results)
    
    print(f"Found {len(search_results)} results\n")
    
    # Step 2: Show raw results
    print("Step 2: Raw search results:")
    print("-" * 60)
    for i, result in enumerate(search_results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   {result['snippet'][:100]}...")
        print(f"   {result['link']}")
    
    # Step 3: Get AI summary
    print("\n" + "=" * 60)
    print("Step 3: AI-Powered Summary:")
    print("-" * 60)
    summary = ai.summarize_results(query, search_results)
    print(summary)
    print("\n" + "=" * 60)


if __name__ == "__main__":
    simple_example()
