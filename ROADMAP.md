# Newspaper Framework Roadmap

## Aktueller Stand (v2.1)

### Erledigt
- **Framework-Kern**: `NewspaperFrameWork`, `Article`, `LayoutConfig`, `MediaConfig`
- **Quiz-System**: `QuizSystem`, `Question` mit Validierung und HTML-Ausgabe
- **Sudoku-Generator**: `SudokuGenerator` mit 3 Schwierigkeitsstufen
- **HTML-Export**: Responsive Design, 4 Themes (classic, modern, minimal, premium), XSS-Schutz
- **JSON-Export**: Strukturierte Daten mit Statistiken
- **REST-API**: `api_server.py` mit Flask-Routes (CRUD fuer Zeitungen)
- **MCP-Server**: `MCP_SERVER.py` mit Tool-Registrierung
- **Fehlerbehandlung**: `NewspaperFrameworkError` (harte Fehler) + `NewspaperFrameworkWarning` (nicht-kritisch)

### Kurzfristig
- PDF-Export (z.B. ueber reportlab oder WeasyPrint)
- Test-Suite (pytest)
- Package-Setup (pyproject.toml)

### Mittelfristig
- LLM-Integration (Gemini CLI, Perplexity API) — siehe `REST_API_EXTENSION_PLAN.md`
- Template-System mit vordefinierten Zeitungsvorlagen
- Lesezeit-Berechnung fuer Artikel

### Langfristig
- Analytics-Dashboard
- Social-Media-Integration
- Team-Kollaboration und Workflow-Management

## Vision

Ein Framework, das so intuitiv ist, dass selbst ein Anfänger-LLM eine professionelle Zeitung erstellen kann.
