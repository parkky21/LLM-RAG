# Function Execution API

A Python-based API service that dynamically retrieves and executes automation functions using LLM + RAG (Retrieval-Augmented Generation). The system processes natural language user prompts, maps them to predefined automation functions, and generates executable Python code for function invocation.

## Features

- **Function Registry**: Pre-defined automation functions for system operations, application control, and utilities
- **LLM + RAG for Function Retrieval**: Intelligent matching of user queries to relevant functions
- **Dynamic Code Generation**: Automatic creation of executable Python scripts
- **Context Awareness**: Session-based memory to improve function retrieval over time
- **RESTful API**: Easy integration with any application

## Architecture

The solution uses a modern, clean architecture:

- **FastAPI** for high-performance API endpoints
- **ChromaDB** for vector-based function storage and retrieval
- **Sentence Transformers** for embeddings creation
- **Transformers** for LLM-based code generation
- **Pydantic** for data validation and serialization

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/function-execution-api.git
cd function-execution-api
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

### Running the API

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### Docker Support

Build and run with Docker:

```bash
docker build -t function-execution-api .
docker run -p 8000:8000 function-execution-api
```

## API Usage

### Execute a Function

```bash
curl -X POST "http://localhost:8000/execute" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Open calculator"}'
```

Response:
```json
{
  "function": "application.open_calculator",
  "code": "from app.functions.application import open_calculator\n\ndef main():\n    try:\n        result = open_calculator()\n        if result is None:\n            print(\"Function executed successfully with no return value.\")\n        elif isinstance(result, bool):\n            status = \"successfully\" if result else \"with issues\"\n            print(f\"Function executed {status}.\")\n        else:\n            print(f\"Result: {result}\")\n    except Exception as e:\n        print(f\"Error executing function: {e}\")\n\nif __name__ == \"__main__\":\n    main()",
  "execution_result": null,
  "context": "No previous interactions."
}
```

### List Available Functions

```bash
curl -X GET "http://localhost:8000/functions"
```

## Extending the System

### Adding New Functions

1. Create a new function in one of the modules in `app/functions/` or add a new module
2. The function will automatically be added to the registry on startup

Example:
```python
# app/functions/utilities.py

def compress_files(directory, output_file):
    """
    Compress all files in a directory into a zip archive.
    
    Args:
        directory (str): Path to directory containing files to compress
        output_file (str): Path to output zip file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import shutil
        shutil.make_archive(output_file, 'zip', directory)
        return True
    except Exception:
        return False
```

## Implementation Details

### RAG Implementation

The system uses a two-stage approach:
1. Function metadata (names, docstrings, signatures) is embedded and stored in ChromaDB
2. User queries are converted to embeddings and compared to find the most relevant functions

### Context Management

The context manager tracks:
- Previous user queries
- Functions that were executed
- Results of those executions

This improves the accuracy of function matching over time within a session.

### Code Generation

Code generation follows a template-based approach with LLM enhancement:
1. A base template is created for the matched function
2. Parameters are extracted from the user's query
3. The LLM refines the code for better robustness and error handling

## Repository Structure

```
project_structure/
├── app/
│   ├── main.py               # FastAPI application
│   ├── config.py             # Configuration management
│   ├── models/               # Pydantic models and database
│   ├── services/             # Core services
│   ├── functions/            # Automation functions
│   └── utils/                # Utilities
├── tests/                    # Unit and integration tests
├── requirements.txt          # Dependencies
├── Dockerfile                # Container definition
└── README.md                 # Project documentation
```

## Performance Considerations

- The system uses lightweight embedding models for faster performance
- Functions and embeddings are loaded and cached on startup
- Session data is persisted to disk for reliability

## Future Enhancements

- Function parameter extraction using LLM
- User-defined function registration through API
- Enhanced error handling and retries
- Web UI for testing and administration
- Performance monitoring and analytics