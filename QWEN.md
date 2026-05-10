# Newspaper Framework - Projektkontext

**Projekt**: Newspaper Framework fuer LLMs
**Ziel**: Einfaches, fehlertolerantes Framework fuer KI-gestuetzte Zeitungsproduktion
**Sprache**: Python 3.12+ (stdlib-only Kern)
**Architektur**: Single-File Framework mit REST-API und MCP-Server

## Aktueller Stand

### Stabil und lauffaehig
- `newspaper_framework.py` — Kern-Framework (v2.1)
- `api_server.py` — REST-API (Flask)
- `examples/demo_newspaper.py` — funktionierende Demo

- `MCP_SERVER.py` — MCP-Server (lauffaehig, braucht MCP-SDK fuer Protokoll-Integration)

### Design-Prinzipien
- **LLM-first**: API und Doku fuer LLMs optimiert
- **Fehlertolerant**: Automatische Korrektur mit Warnungen
- **Sicher**: HTML-Escaping gegen XSS, Validierung aller Eingaben
- **Stdlib-only Kern**: Keine externen Abhaengigkeiten fuer `newspaper_framework.py`

### Fehlerklassen
- `NewspaperFrameworkError(Exception)` — harte Validierungsfehler
- `NewspaperFrameworkWarning(UserWarning)` — nicht-kritische Hinweise

### Konventionen
- Deutschsprachige Ausgaben und Warnungen
- Keine Emojis in `print()` (Windows cp1252)
- `NewspaperFrameWork` — grosses W in "FrameWork" ist intentional
