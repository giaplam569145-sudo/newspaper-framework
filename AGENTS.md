# AGENTS.md

## Quick Reference

- **Language**: Python 3.12+ (Windows, `pwsh` shell)
- **No package manager**: No `requirements.txt`, `pyproject.toml`, or `setup.py`. No virtualenv. Core framework is stdlib-only.
- **No test suite**: No test runner, no test directory. Verify changes by running `python newspaper_framework.py` (executes `create_sample_newspaper()` demo).
- **No linter/formatter/typecheck configured**: None exist. Follow existing style when editing.

## Architecture

| File | State | Notes |
|------|-------|-------|
| `newspaper_framework.py` | **Stable, working** | Core library. Public classes: `NewspaperFrameWork`, `Article`, `QuizSystem`, `SudokuGenerator`, `Question`, `LayoutConfig`, `MediaConfig` |
| `api_server.py` | **Working** | Flask REST API. Endpoints: POST/GET `/api/newspaper[/<id>]`, POST `/api/newspaper/<id>/article`, POST `/api/newspaper/<id>/export`. Requires `flask` package. |
| `MCP_SERVER.py` | **Working** | MCP tool registration. `NewspaperMCPServer` class + `get_tools()`. No external MCP SDK dependency currently. |
| `examples/demo_newspaper.py` | **Working** | Advanced demo with logo, images, sudoku. Includes `sys.path` fix for subdirectory. |

## Key Classes (in `newspaper_framework.py`)

- `NewspaperFrameWork` — main entry point. `add_article()`, `set_logo()`, `add_quiz()`, `add_sudoku()`, `generate()`, `export_html(filename, theme)`, `export_json(filename)`.
- `Article` — dataclass. Min 10 chars content enforced via `NewspaperFrameworkError`. Priority clamped to 1-5.
- `QuizSystem` — holds `Question` objects. `add_question()`, `generate_quiz()`, `to_html()`.
- `SudokuGenerator` — generates 9x9 grids. Difficulty: `"easy"` (30 blanks), `"medium"` (40), `"hard"` (50).

## Error Classes

- `NewspaperFrameworkError(Exception)` — hard validation errors (empty title, short content, invalid quiz options).
- `NewspaperFrameworkWarning(UserWarning)` — non-critical warnings (missing images, missing logo). Emitted via `warnings.warn()`.

## Conventions

- German-language user-facing messages. English code identifiers.
- No emojis in `print()` statements — Windows `cp1252` console encoding will crash on emoji characters.
- `NewspaperFrameWork` — note the capital W in "FrameWork". This is intentional, used everywhere.
- `export_html()` accepts `theme` parameter: `"classic"`, `"modern"`, `"minimal"`, `"premium"`.

## Verifying Changes

```bash
python newspaper_framework.py
```

Should exit 0 and produce `beispiel_zeitung.html` + `beispiel_zeitung.json`.

## Planned Work (see `REST_API_EXTENSION_PLAN.md`)

v3.0 plans: Gemini CLI integration, Perplexity API fact-checking with Gemini fallback, new REST endpoints. Not yet implemented.

## Git

- Local-only repo (no remote). User: `Newspaper Framework AI <framework@newspaper.com>`.
- Commit language: English messages.
