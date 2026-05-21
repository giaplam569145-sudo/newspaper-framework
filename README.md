# Newspaper Framework for LLMs

A modular, fault-tolerant framework for AI-powered newspaper production with quizzes, sudoku, crosswords, and multiple export formats.

## Quick Start

```python
from src.newspaper import Newspaper, QuizSystem
from src.newspaper.content.crossword import CrosswordGenerator

paper = Newspaper("AI Morning News")

paper.add_article(
    title="AI Revolutionizes Newspaper Production",
    content="The Newspaper Framework allows LLMs to create high-quality newspapers with minimal effort...",
    author="AI Editor",
    category="Technology",
    priority=1
)

paper.set_logo("logo.png")

quiz = QuizSystem("Technology Quiz")
quiz.add_question(
    "What is AI?",
    ["Artificial Intelligence", "Kitchen International", "Merchant Institute", "No Idea"],
    0,
    "Technology"
)
paper.add_quiz(quiz)

paper.add_sudoku("medium")

crossword = CrosswordGenerator(
    words=["python", "html"],
    clues={"python": "A popular programming language.", "html": "A markup language for the web."},
)
paper.add_crossword(crossword.generate())

paper.export_html("my_newspaper.html")
paper.export_json("my_newspaper.json")
```

## Features

- **LLM-Friendly API**: Intuitive method names and clear feedback
- **Automatic Validation**: Content checked and corrected automatically
- **Fault-Tolerant**: Gentle corrections, warnings via `warnings.warn()`
- **Modular Architecture**: Clean `src/` package layout with DRY/SOLID principles
- **Content Types**: Articles, quizzes, sudoku, crossword puzzles
- **Export Formats**: HTML (Jinja2 templates with autoescape), JSON
- **Responsive Design**: Mobile-optimized HTML output
- **REST API**: Flask-based HTTP API (`src/api/rest.py`)

## Installation

```bash
pip install -r requirements.txt
```

Core framework only needs `jinja2`. Full features need `flask`, `pycrossword-generator`, `mcp`.

## Project Structure

```
src/newspaper/          Core package
  core.py               Newspaper class (main entry point)
  models.py             Article, Question, LayoutConfig, MediaConfig
  exceptions.py         NewspaperFrameworkError + NewspaperFrameworkWarning
  content/              Quiz, Sudoku, Crossword generators
  export/               HTML (Jinja2) and JSON exporters
src/api/                REST API and MCP server
tests/                  pytest test suite (48 tests)
run_api.py              Start the REST API server
run_mcp.py              Start the MCP server
sample_generator.py     Demo script
```

## Running

```bash
# Generate a sample newspaper
python sample_generator.py

# Start REST API
python run_api.py

# Run tests
python -m pytest tests/ -v
```

## API Overview

### Newspaper Methods

| Method | Description |
|--------|-------------|
| `add_article(title, content, **kwargs)` | Add an article (min 10 chars content) |
| `set_logo(logo_path)` | Set newspaper logo |
| `add_quiz(quiz)` | Add a QuizSystem |
| `add_sudoku(difficulty)` | Add sudoku ("easy", "medium", "hard") |
| `add_crossword(crossword)` | Add a crossword puzzle |
| `generate()` | Return structured dict of the newspaper |
| `export_html(filename)` | Export as responsive HTML |
| `export_json(filename)` | Export as structured JSON |

### Error Handling

- `NewspaperFrameworkError` — hard validation errors (empty title, short content, invalid quiz options)
- `NewspaperFrameworkWarning` — non-critical warnings (missing images, missing logo)

## License

Local project. No license file yet.
