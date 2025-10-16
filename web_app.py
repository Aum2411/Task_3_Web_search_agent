"""
Flask web application for the Web Search Agent
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from web_search import WebSearcher
from groq_ai import GroqAI

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize components
try:
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    if not groq_api_key:
        print("Warning: GROQ_API_KEY not found in environment variables")
        searcher = None
        ai = None
    else:
        serper_api_key = os.getenv('SERPER_API_KEY')
        if not serper_api_key:
            print("Warning: SERPER_API_KEY not found in environment variables")
            searcher = None
            ai = None
        else:
            searcher = WebSearcher(serper_api_key)
            ai = GroqAI(groq_api_key)
            print("✓ Web Search Agent initialized successfully!")
            print("✓ Using Serper.dev for web search")
except Exception as e:
    print(f"Error initializing agent: {e}")
    searcher = None
    ai = None


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search():
    """Handle search requests"""
    try:
        # Check if components are initialized
        if not searcher or not ai:
            return jsonify({
                'success': False,
                'error': 'Agent not properly configured. Please check your API keys.'
            }), 500
        
        # Get query from request
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Please enter a search query'
            }), 400
        
        # Perform web search
        num_results = data.get('num_results', 10)
        raw_results = searcher.search(query, num_results)
        search_results = searcher.format_results(raw_results)
        
        if not search_results or 'error' in raw_results:
            return jsonify({
                'success': False,
                'error': 'Failed to fetch search results. Please try again.'
            }), 500
        
        # Filter results with AI
        filter_results = data.get('filter_results', True)
        if filter_results and len(search_results) > 5:
            filtered_results = ai.filter_relevant_results(query, search_results, top_n=5)
        else:
            filtered_results = search_results[:5]
        
        # Generate AI summary
        summary = ai.summarize_results(query, filtered_results)
        
        return jsonify({
            'success': True,
            'query': query,
            'summary': summary,
            'results': filtered_results,
            'total_results': len(search_results)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'agent_initialized': searcher is not None and ai is not None
    })


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🤖 WEB SEARCH AGENT - Web Interface")
    print("=" * 60)
    print("Starting server...")
    print("\nOpen your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
