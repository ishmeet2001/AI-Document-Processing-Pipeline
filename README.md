# Unstructured Data Pipeline

An intelligent agentic system powered by **LangChain** and **Google Gemini** that extracts structured invoice data from unstructured text files and stores it in SQLite databases.

## Features

- 🤖 **AI-Powered Extraction**: Leverages Google Gemini LLM to intelligently parse invoice data
- 🔄 **Agentic Workflow**: Uses LangChain agents with tool calling for autonomous database operations
- 📊 **Schema Validation**: Enforces strict Pydantic schemas for invoice and item details
- 💾 **SQLite Integration**: Automatically creates and populates relational databases with foreign key constraints
- 🧵 **Concurrent Processing**: Multi-threaded file validation and reading for optimal performance
- ✅ **Comprehensive Testing**: Full test suite with pytest

## Project Structure

```
Unstructured Data Pipeline/
├── src/
│   └── unstructured-data-pipeline/
│       ├── __init__.py
│       ├── config.py                      # Configuration and environment variables
│       ├── main.py                        # CLI entry point
│       ├── .env.local                     # Environment configuration
│       ├── .gitignore
│       │
│       ├── application/
│       │   └── pipelines/
│       │       └── llm_pipeline.py        # Agent creation and template formatting
│       │
│       ├── domain/
│       │   ├── prompts/
│       │   │   ├── human_instructions.py  # User input template
│       │   │   └── llm_instructions.py    # System prompt template
│       │   │
│       │   ├── schema/
│       │   │   ├── invoice.py             # Invoice and ItemDetails Pydantic models
│       │   │   └── llm_output.py          # LLM response schema
│       │   │
│       │   ├── tools/
│       │   │   ├── file_creation.py       # Database file creation tools
│       │   │   └── sql_execution.py       # SQL execution with retry logic
│       │   │
│       │   └── validators/
│       │       └── file_naming.py         # File path and type validators
│       │
│       ├── infrastructure/
│       │   ├── CLI/
│       │   │   └── main.py                # File reading with threading
│       │   │
│       │   └── llm_providers/
│       │       └── gemini_provider.py     # Google Gemini LLM initialization
│       │
│       └── saved_files/                   # Default database storage location
│
├── tests/
│   ├── __init__.py
│   ├── test_app.py                        # Comprehensive test suite
│   └── test_files/
│       ├── invoice_clean.txt
│       ├── invoice_email.txt
│       └── invoice_messy.txt
│
├── Makefile                               # Build automation commands
├── pyproject.toml                         # Project metadata and dependencies
├── run_tests.py                           # Test runner script
└── README.md                              # This file
```

## Installation

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key

### Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd "Unstructured Data Pipeline"
   ```

2. **Install dependencies**

   ```bash
   make install
   # or
   pip install -e .
   ```

3. **Configure environment variables**

   Create or edit `src/unstructured-data-pipeline/.env.local`:

   ```env
   FILES_STORAGE=/path/to/your/database/Data.db
   FILE_TYPES_ALLOWED=txt
   PROCESS_COMMAND=process <input_path> --db <output_db_path>
   GOOGLE_GEMINI_API_KEY=your-api-key-here
   ```

## Usage

### Running the Pipeline

Navigate to the source directory and run the main script:

```bash
cd src/unstructured-data-pipeline
python main.py
```

### CLI Commands

When prompted, use the following commands:

- **View available commands**:

  ```
  Commands
  ```

- **Process a file**:

  ```
  process <path/to/invoice.txt> --db <path/to/output.db>
  ```

  Example:

  ```
  process ../../tests/test_files/invoice_clean.txt --db ./saved_files/invoices.db
  ```

- **Exit the program**:
  ```
  Exit
  ```

### How It Works

1. **File Validation**: The system validates file paths, types (`.txt`), and existence
2. **Content Extraction**: Files are read using multi-threaded workers for efficiency
3. **AI Processing**: Google Gemini analyzes the unstructured text and extracts invoice details
4. **Database Operations**: The agent autonomously:
   - Checks if the database file exists
   - Creates the database if needed
   - Creates tables matching the invoice schema with foreign key relationships
   - Inserts extracted data with proper validation
5. **Result**: Structured invoice data stored in a relational SQLite database

## Testing

### Run Tests

```bash
# Using the test runner
python run_tests.py

# Using Make
make test

# Using pytest directly
pytest tests/
```

### Test Coverage

The test suite includes:

- File validation (path, type, existence)
- Concurrent file reading
- Database file creation
- SQL execution with error handling
- Schema enforcement

## Development

### Code Quality

```bash
# Lint the code
make lint

# Format the code
make format

# Clean cache files
make clean
```

### Dependencies

Core dependencies:

- `langchain` - Agent framework
- `langchain-google-genai` - Google Gemini integration
- `langgraph` - Agent orchestration
- `pydantic` - Schema validation
- `python-dotenv` - Environment configuration

Development dependencies:

- `pytest` - Testing framework
- `ruff` - Linting and formatting

## Schema

### Invoice Schema

```python
Invoice:
  - Sender_Name: str
  - Date: date
  - Item_Details: List[ItemDetails]
  - Total_Amount: float
  - Currency: str

ItemDetails:
  - Description: str
  - Quantity: str
  - Unit_price: int
```