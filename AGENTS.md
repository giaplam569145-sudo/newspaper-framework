# AGENTS.md

## Quick Reference

- **Language**: Python 3.12+ (Windows, `pwsh` shell)
- **Dependencies**: `requirements.txt` (flask, jinja2, pycrossword-generator, mcp, pytest). Core `src/newspaper/` needs only stdlib + jinja2.
- **Test suite**: pytest. Run with `python -m pytest tests/ -v` (49 tests).
- **Config**: `pyproject.toml` for build, pytest, ruff, mypy settings.

## Architecture

```
src/newspaper/          # Core package
  __init__.py           # Public exports
  core.py               # Newspaper class (main entry point)
  models.py             # Article, Question, LayoutConfig, MediaConfig dataclasses
  exceptions.py         # NewspaperFrameworkError + NewspaperFrameworkWarning
  content/
    base.py             # ContentGenerator ABC
    quiz.py             # QuizSystem
    sudoku.py           # SudokuGenerator
    crossword.py        # CrosswordGenerator (needs pycrossword-generator)
  export/
    base.py             # Exporter ABC
    html_exporter.py    # HtmlExporter (Jinja2 with autoescape)
    json_exporter.py    # JsonExporter
    templates/base.html # Jinja2 template
src/api/
  rest.py               # Flask REST API (full CRUD + quiz/sudoku/crossword)
  mcp_server.py         # MCP server (needs mcp package)
tests/                  # pytest test suite (49 tests)
run_api.py              # Entry point: python run_api.py
run_mcp.py              # Entry point: python run_mcp.py
sample_generator.py     # Demo script using src/ package
examples/
  demo_newspaper.py     # Example using the Newspaper class
```

## Key Classes

- `Newspaper` (in `src/newspaper/core.py`) — main entry point. `add_article(force=False)`, `set_logo()`, `add_quiz()`, `add_sudoku()`, `add_crossword()`, `generate()`, `export_html()`, `export_json()`.
- `Article` — dataclass. Min 10 chars content enforced via `NewspaperFrameworkError`. Priority clamped 1-5.
- `QuizSystem` — holds `Question` objects. `add_question()`, `to_dict()`.
- `SudokuGenerator` — 9x9 grids. Difficulty: `"easy"` (30 blanks), `"medium"` (40), `"hard"` (50).
- `CrosswordGenerator` — uses `pycrossword-generator`. `generate()` returns `Crossword` dataclass.

## Error Classes

- `NewspaperFrameworkError(Exception)` — hard validation errors (empty title, short content, invalid quiz).
- `NewspaperFrameworkWarning(UserWarning)` — non-critical (missing images/logo). Emitted via `warnings.warn()`.

## Conventions

- Use `logging` module, not `print()` — all modules use `logging.getLogger(__name__)`.
- `Newspaper` class (renamed from legacy `NewspaperFrameWork`).
- Jinja2 autoescape handles XSS protection in HTML export.
- `generate()` is side-effect-free: no stdout, no in-place mutation of articles.
- `add_article()` raises `NewspaperFrameworkError` for short content by default. Use `force=True` to auto-correct.
- REST API propagates `NewspaperFrameworkError` as HTTP 400.

## Verifying Changes

```bash
python -m pytest tests/ -v
python sample_generator.py
```

## Git

- Remote: `https://github.com/giaplam569145-sudo/newspaper-framework.git`
- Commit language: English messages.
