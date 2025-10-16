"""
Main Web Search Agent Application
Combines web search and AI summarization
"""
import os
from dotenv import load_dotenv
from web_search_duckduckgo import WebSearcher
from groq_ai import GroqAI


class WebSearchAgent:
    """Intelligent web search agent powered by Groq AI"""
    
    def __init__(self):
        """Initialize the agent with API credentials"""
        # Load environment variables
        load_dotenv()
        
        # Get API keys
        groq_api_key = os.getenv('GROQ_API_KEY')
        
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Initialize components
        self.searcher = WebSearcher()  # No API key needed for DuckDuckGo
        self.ai = GroqAI(groq_api_key)
        
        print("✓ Web Search Agent initialized successfully!")
        print("✓ Using DuckDuckGo for web search (no API key required)")
    
    def search_and_summarize(self, query: str, num_results: int = 10, 
                           filter_results: bool = True) -> dict:
        """
        Perform a web search and get AI-powered summary
        
        Args:
            query: User's search query
            num_results: Number of search results to retrieve
            filter_results: Whether to use AI to filter most relevant results
            
        Returns:
            Dictionary containing search results and AI summary
        """
        print(f"\n🔍 Searching for: '{query}'")
        print("=" * 60)
        
        # Step 1: Perform web search
        print("\n[1/3] Fetching search results...")
        raw_results = self.searcher.search(query, num_results)
        search_results = self.searcher.format_results(raw_results)
        
        if not search_results or 'error' in raw_results:
            return {
                'query': query,
                'error': 'Failed to fetch search results',
                'results': [],
                'summary': 'No results available due to search error.'
            }
        
        print(f"      Found {len(search_results)} results")
        
        # Step 2: Filter results using AI (optional)
        filtered_results = search_results
        if filter_results and len(search_results) > 5:
            print("\n[2/3] Filtering most relevant results with AI...")
            filtered_results = self.ai.filter_relevant_results(query, search_results, top_n=5)
            print(f"      Selected {len(filtered_results)} most relevant results")
        else:
            print("\n[2/3] Using all results (no filtering)")
        
        # Step 3: Generate AI summary
        print("\n[3/3] Generating AI-powered summary...")
        summary = self.ai.summarize_results(query, filtered_results)
        
        print("\n✓ Processing complete!")
        
        return {
            'query': query,
            'num_results': len(search_results),
            'filtered_results': filtered_results,
            'all_results': search_results,
            'summary': summary
        }
    
    def interactive_mode(self):
        """Run the agent in interactive mode"""
        print("\n" + "=" * 60)
        print("🤖 WEB SEARCH AGENT - Interactive Mode")
        print("=" * 60)
        print("Powered by Groq AI + Serper.dev")
        print("\nType your search queries below.")
        print("Commands: 'quit' or 'exit' to stop, 'help' for options\n")
        
        while True:
            try:
                query = input("\n💬 Your query: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if query.lower() == 'help':
                    self._show_help()
                    continue
                
                # Perform search and get summary
                result = self.search_and_summarize(query)
                
                # Display results
                self._display_results(result)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
    
    def _display_results(self, result: dict):
        """Display search results in a formatted way"""
        print("\n" + "=" * 60)
        print("📊 SEARCH RESULTS")
        print("=" * 60)
        
        # Display summary
        print("\n🤖 AI Summary:")
        print("-" * 60)
        print(result['summary'])
        
        # Display source links
        print("\n\n🔗 Source Links:")
        print("-" * 60)
        for i, source in enumerate(result['filtered_results'], 1):
            print(f"\n[{i}] {source['title']}")
            print(f"    {source['link']}")
        
        print("\n" + "=" * 60)
    
    def _show_help(self):
        """Display help information"""
        print("\n" + "=" * 60)
        print("📖 HELP")
        print("=" * 60)
        print("""
How to use:
1. Type your search query and press Enter
2. The agent will search the web and provide an AI summary
3. Results are automatically filtered for relevance

Commands:
- 'quit' or 'exit' - Exit the program
- 'help' - Show this help message

Tips:
- Be specific in your queries for better results
- Ask questions naturally, like talking to a person
- The AI will synthesize information from multiple sources
        """)


def main():
    """Main entry point"""
    try:
        # Create and run the agent
        agent = WebSearchAgent()
        agent.interactive_mode()
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("\nPlease make sure:")
        print("1. You have created a .env file")
        print("2. Added your GROQ_API_KEY")
        print("\nNo other API keys are required - DuckDuckGo search is used automatically!")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")


if __name__ == "__main__":
    main()
