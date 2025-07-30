# Fake News Detector

A FastAPI-based service that analyzes news headlines for credibility using AI-powered fact-checking and web search verification.

## Features

- **AI-Powered Analysis**: Uses OpenAI models to generate fact-checking queries and analyze credibility
- **Multi-Source Verification**: Searches multiple sources using DuckDuckGo for comprehensive fact-checking
- **Batch Processing**: Handles large-scale analysis with concurrent processing and rate limiting
- **RESTful API**: Clean FastAPI endpoints for easy integration
- **Credibility Scoring**: Returns numerical credibility scores (0-100) with detailed flags

## Architecture

```
├── main.py              
├── config.py           
├── schema.py            
├── services/            
│   ├── openai_client.py
│   ├── search_client.py
│   └── search_providers/
├── llm/                
│   ├── query_generator.py
│   ├── technical_analyzer.py
│   └── credibility_analysis/
├── interfaces/         
├── utils/            
└── tests/              
```

## Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API key
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/alomj/news_checker
cd news_checker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI credentials
```

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Deployment

```bash
docker build -t fake-news-detector .
docker run -p 8000:8000 --env-file .env fake-news-detector
```

## API Endpoints

### `/news-checker` - Complete Analysis
Analyzes a news headline for credibility with full fact-checking.



### `/generate-news` - Query Generation Only
Generates fact-checking queries without performing searches.

### `/search-news` - Search Only
Performs web searches for provided headlines without AI analysis.

### `/rate-search` - Analysis Only
Analyzes pre-searched results for credibility.

## Configuration

Key configuration options in `config.py`:

- `OPENAI_KEY`: Your OpenAI API key
- `MODEL`: OpenAI model to use (e.g., "gpt-4")
- `BASE_URL`: OpenAI API base URL
- `max_limit`: Concurrent request limit (default: 5)
- `max_search`: Maximum search results per query (default: 5)

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
coverage run -m pytest tests/
coverage report
```

### Code Quality

```bash
# Linting
flake8 .

# The project follows PEP 8 with 100 character line limit
```

### CI/CD

GitHub Actions workflows are configured for:
- **Style Check**: Runs flake8 on every push/PR
- **Tests**: Runs pytest with coverage reporting

## How It Works

1. **Query Generation**: AI generates targeted search queries for fact-checking
2. **Web Search**: Multiple sources are searched using DuckDuckGo
3. **Batch Processing**: Results are processed in batches to handle API limits
4. **Credibility Analysis**: AI analyzes each source for credibility indicators
5. **Result Aggregation**: Scores and flags are compiled into final response

## Limitations

- Requires OpenAI API access (paid service)
- Search limited to DuckDuckGo news results
- Analysis quality depends on available sources
- Rate limited by both OpenAI and search provider limits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass and code follows style guidelines
6. Submit a pull request

