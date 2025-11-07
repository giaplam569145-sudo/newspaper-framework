# Newspaper Framework for LLMs

A simple, fault-tolerant framework for AI-powered newspaper production with advanced media features.

## Goal

To enable LLMs to create high-quality morning newspapers with minimal effort, while the framework ensures consistent quality and automatic error correction.

## Quick Start

```python
from newspaper_framework import NewspaperFrameWork, QuizSystem

# Create the framework
paper = NewspaperFrameWork("AI Morning News")

# Add an article (the LLM replaces this with its own content)
paper.add_article(
    title="AI Revolutionizes the Newspaper Industry",
    content="New framework facilitates AI-powered newspaper production...",
    author="AI Editor",
    category="Technology",
    priority=1,
    image_path="tech_image.jpg",
    image_caption="AI in media production"
)

# Set the logo
paper.set_logo("logo.png")

# Add a quiz
quiz = QuizSystem("Technology Quiz")
quiz.add_question(
    "What is AI?",
    ["Artificial Intelligence", "Kitchen International", "Merchant Institute", "No Idea"],
    0,
    "Technology"
)
paper.add_quiz(quiz)

# Add a Sudoku puzzle
paper.add_sudoku("medium")

# Export
paper.export_html("my_newspaper.html")
paper.export_json("my_newspaper.json")
```

## 📋 Features

- ✅ **LLM-Friendly API**: Intuitive method names and clear feedback.
- ✅ **Automatic Validation**: Content is automatically checked and corrected.
- ✅ **Design System**: Consistent layouts without design overhead.
- ✅ **Fault-Tolerant**: Gentle corrections instead of hard errors.
- ✅ **Single-File Solution**: Easy distribution via chat messages.
- ✅ **Responsive Export**: HTML, JSON, PDF (optional).
- ✅ **Token-Efficient**: LLMs can focus on content.
- ✅ **Consistent Quality**: Guaranteed output quality.
- ✅ **Logo/Banner Integration**: Easy logo management.
- ✅ **Image Support**: Article images with captions.
- ✅ **Interactive Quizzes**: Question-answer systems.
- ✅ **Sudoku Puzzles**: Automatic Sudoku generation.
- ✅ **Responsive Design**: Mobile-optimized output.

## ️ Installation

```python
# Simply download the file and import it
import newspaper_framework
```

## Design Principles

### 1. LLM-First
- Method names like `add_article()` instead of `append_content()`.
- Clear success/error messages with emojis.
- Automatic content validation and correction.
- Helpful warnings instead of cryptic error messages.

### 2. Fault Tolerance
- Short articles are automatically supplemented.
- Incorrect inputs are gently corrected.
- Missing images generate warnings, not crashes.

### 3. Media Integration
- Simple logo management.
- Image support for articles.
- Interactive elements (quizzes, Sudoku).

## 📖 Documentation for LLMs

### Key Methods:

#### `add_article(title, content, **kwargs)`
Adds an article with automatic validation.

#### `set_logo(logo_path)`
Sets a logo for the newspaper.

#### `add_quiz(quiz)`
Adds an interactive quiz.

#### `add_sudoku(difficulty="medium")`
Adds a Sudoku puzzle.

#### `export_html(filename)`
Exports as a responsive HTML file.

#### `export_json(filename)`
Exports as a structured JSON file.

### Error Handling:
- `NewspaperFrameworkWarning` for LLM-friendly messages.
- Automatic corrections for potential errors.
- Continuous processing even with partial errors.

## 🎨 Examples

### Newspaper with All Features
```python
from newspaper_framework import NewspaperFrameWork, QuizSystem

paper = NewspaperFrameWork("Complete Newspaper")
paper.set_logo("logo.png")

# Multiple articles
paper.add_article("Title 1", "Content 1...", priority=1, category="Politics")
paper.add_article("Title 2", "Content 2...", priority=2, category="Business")

# Quiz
quiz = QuizSystem("Daily Quiz")
quiz.add_question("Question?", ["Option 1", "Option 2"], 0)
paper.add_quiz(quiz)

# Sudoku
paper.add_sudoku("hard")

paper.export_html("complete.html")
```

### Custom Layout
```python
from newspaper_framework import NewspaperFrameWork, LayoutConfig

layout = LayoutConfig(
    font_family="Times New Roman",
    primary_color="#1a1a1a",
    max_width=1000,
    columns=3
)

paper = NewspaperFrameWork("Premium Newspaper", layout=layout)
```

## 📄 Files

- `newspaper_framework.py` - The main framework.
- `api_server.py` - A RESTful API server for the framework.
- `MCP_SERVER.py` - An MCP server for AI agent integration.
- `README.md` - This overview.

## 🔄 Version 2.0 Features

- **New**: Logo/banner integration.
- **New**: Image support for articles.
- **New**: Interactive quiz systems.
- **New**: Sudoku puzzle generation.
- **New**: Improved error handling.
- **New**: Responsive design systems.
- **New**: Expanded export formats.

## 🤖 For LLMs

This framework was specifically developed for AI systems:

1. **Simple API**: Clear method names and parameters.
2. **Automatic Correction**: Focus on content, not error handling.
3. **Consistent Quality**: Guaranteed output quality.
4. **Token Efficiency**: Minimal overhead complexity.
5. **Fault Tolerance**: Robust processing even with incomplete data.

## 📞 Support

For questions or issues:
1. Check the API documentation.
2. Validate your input data.
3. Utilize the automatic error correction.

---

*Developed with ❤️ for AI-powered newspaper production*