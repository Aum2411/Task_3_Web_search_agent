# 🤖 Web Search Agent with Groq AI

An intelligent web search agent that combines real-time web search with AI-powered summarization and analysis using Groq API and Serper.dev.

## 🌟 Features

- **Beautiful Web Interface**: Modern, responsive UI with smooth animations and gradients
- **Real-time Web Search**: Fetches current information using DuckDuckGo (no API key required!)
- **AI-Powered Summarization**: Uses Groq AI (Llama 3.1) to analyze and summarize search results
- **Intelligent Filtering**: Automatically identifies and ranks the most relevant results
- **Interactive Mode**: Both web interface and command-line interface available
- **Source Citations**: Provides links to original sources for verification
- **No Extra API Keys**: Only requires Groq API key - web search is completely free!

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API key (provided)
- **That's it!** No other API keys needed

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Configure API Keys

The Groq API key is already configured in the `.env` file. **No other API keys are needed!**

The application uses **DuckDuckGo** for web search, which requires no API key or registration.

Your `.env` file should contain:
```
GROQ_API_KEY=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
```

### 3. Run the Agent

**Web Interface** (Recommended - Beautiful UI):
```powershell
python web_app.py
```
Then open your browser to: **http://localhost:5000**

**Command Line Interface**:
```powershell
python agent.py
```

**Simple Example**:
```powershell
python example.py
```

## 💻 Usage

### Web Interface (Recommended)

1. Start the web server:
```powershell
python web_app.py
```

2. Open your browser to **http://localhost:5000**

3. Type your query in the search box and hit Enter

4. Get beautiful, AI-powered results with:
   - Comprehensive summary
   - Source cards with snippets
   - Smooth animations and transitions
   - Responsive design for all devices

### Command Line Interface

```powershell
python agent.py
```

Then type your queries:
```
💬 Your query: What are the latest AI developments in 2025?
```

The agent will:
1. Search the web for relevant information
2. Filter the most relevant results using AI
3. Provide a comprehensive summary with source citations

### Programmatic Usage

```python
from agent import WebSearchAgent

# Initialize the agent
agent = WebSearchAgent()

# Perform a search and get summary
result = agent.search_and_summarize(
    query="What is quantum computing?",
    num_results=10,
    filter_results=True
)

# Access the results
print(result['summary'])
print(result['filtered_results'])
```

## 📁 Project Structure

```
Task_3/
├── web_app.py            # Flask web application (beautiful web UI)
├── agent.py              # Command-line interface
├── example.py            # Simple usage example
├── web_search.py         # Web search module (Serper.dev integration)
├── groq_ai.py           # Groq AI module (summarization & filtering)
├── templates/
│   └── index.html       # Modern HTML interface
├── static/
│   ├── css/
│   │   └── style.css    # Advanced CSS with animations
│   └── js/
│       └── app.js       # JavaScript for interactivity
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (API keys)
├── .env.example         # Template for environment variables
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## 🔧 How It Works

1. **User Query**: You submit a search query
2. **Web Search**: The agent searches DuckDuckGo (free, no API key needed)
3. **AI Filtering**: Groq AI identifies the most relevant results
4. **Summarization**: AI synthesizes information from multiple sources
5. **Response**: You receive a comprehensive summary with source links

## 🎯 Use Cases

- **Research**: Quick research on any topic with AI-powered insights
- **News Updates**: Get summarized updates on current events
- **Learning**: Understand complex topics with synthesized explanations
- **Fact-Checking**: Compare information from multiple sources
- **Decision Making**: Gather and analyze information for informed decisions

## 🔑 API Keys

### Groq API
- Already configured in `.env` file
- Model: Llama 3.1 70B Versatile
- Free tier available

### Web Search
- **DuckDuckGo** - Completely free, no API key required!
- No registration needed
- No rate limits for reasonable usage

## 📝 Example Queries

```
- "What are the latest developments in renewable energy?"
- "Explain quantum computing in simple terms"
- "What is the current state of AI safety research?"
- "Best practices for Python web development in 2025"
- "How does blockchain technology work?"
```

## ⚙️ Configuration

You can modify the behavior in `agent.py`:

- **Number of results**: Change `num_results` parameter (default: 10)
- **AI Model**: Change model in `groq_ai.py` (default: llama-3.1-70b-versatile)
- **Filtering**: Enable/disable with `filter_results` parameter
- **Temperature**: Adjust AI creativity in `groq_ai.py` (default: 0.7)

## 🛠️ Troubleshooting

### Import Errors
If you see "Import could not be resolved" errors:
```powershell
pip install -r requirements.txt
```

### API Key Errors
Make sure your `.env` file contains a valid Groq API key:
```
GROQ_API_KEY=gsk_...
```

### No Search Results
- DuckDuckGo search is free and has no limits
- Check your internet connection
- Try rephrasing your query

## 📚 Available Models

Groq supports multiple models (configured in `groq_ai.py`):
- `llama-3.1-70b-versatile` (default) - Best for general tasks
- `llama-3.1-8b-instant` - Faster, good for simple queries
- `mixtral-8x7b-32768` - Alternative with large context window

## 🤝 Contributing

Feel free to enhance this agent with:
- Additional search providers
- More AI models and providers
- Advanced filtering algorithms
- User interface improvements
- Export functionality (PDF, Markdown)

## 📄 License

This project is provided as-is for educational and research purposes.

## 🔗 Resources

- [Groq API Documentation](https://console.groq.com/docs)
- [DuckDuckGo](https://duckduckgo.com/)
- [Llama 3.1 Model Card](https://ai.meta.com/llama/)

## 🎉 Credits

Built with:
- **Groq** - Ultra-fast AI inference
- **DuckDuckGo** - Privacy-focused search (free, no API key!)
- **Llama 3.1** - Meta's open-source AI model

---

**Happy Searching! 🔍🤖**
