# Chronicle AI – Feature-Vorschläge und Anforderungsanalyse

Dieses Dokument enthält eine fundierte Architekturanalyse der aktuellen Applikation **Chronicle AI (Newspaper Framework for LLMs)**, eine Erhebung potenzieller Anforderungen moderner KI-gestützter Redaktionssysteme sowie acht konkrete, detaillierte Feature-Vorschläge zur Weiterentwicklung des Frameworks.

---

## 1. Systemanalyse & Ist-Zustand

### 1.1 Überblick über die Codebase
Das Framework ist als Python-Bibliothek (Python 3.12+) mit zwei Schnittstellenarten (Flask REST API und Model Context Protocol / MCP) konzipiert. Ziel ist es, Large Language Models (LLMs) und autonomen Agenten die programmatische Erstellung interaktiver digitaler Zeitungen zu ermöglichen.

| Modul | Hauptbestandteile | Aktueller Zustand |
|---|---|---|
| **Core (`src/newspaper/core.py`)** | Klasse `Newspaper` | Orchestriert Artikel, Quizzes, Sudokus, Kreuzworträtsel; speichert Metadaten; triggert Exporte. |
| **Datenmodelle (`src/newspaper/models.py`)** | `Article`, `LayoutConfig`, `MediaConfig`, `Question` | Typisierte Dataclasses mit Validierungslogik (Mindestlänge, Prioritäten-Clamping). |
| **Content-Generatoren (`src/newspaper/content/`)** | `QuizSystem`, `SudokuGenerator`, `CrosswordGenerator` | Standardisierte Erzeugung von Rätsel- und Quizformaten. Sudoku und Quiz sind reine Algorithmen; Crossword bindet optional `pycrossword` ein. |
| **Export-Engine (`src/newspaper/export/`)** | `HtmlExporter` (Jinja2), `JsonExporter` | Generierung strukturierter JSON-Dateien sowie responsiver, interaktiver HTML-Dokumente inklusive JavaScript-Validierung und Dark/Light-Mode. |
| **API & Agenten-Integration (`src/api/`)** | `rest.py` (Flask), `mcp_server.py` (MCP) | In-Memory-Verwaltung von Zeitungsinstanzen; REST- und MCP-Tool-Schnittstellen für LLM-Agenten. |
| **Testsuite (`tests/`)** | 86 automatisierte pytest-Tests | Vollständige Testabdeckung aller Module (Modelle, Core, Content, Exporte, REST API). |

### 1.2 Stärken der aktuellen Architektur
1. **Hohe Robustheit und defensive Validierung**: Klare Trennung zwischen `NewspaperFrameworkError` (harte Validierungsfehler) und `NewspaperFrameworkWarning` (z. B. fehlende Bilddateien).
2. **Klares Schichtenmodell**: Saubere Trennung von Domänenmodell (`models.py`), Business-Logik (`core.py`), Content-Generierung (`content/`) und Export (`export/`).
3. **Interaktive HTML-Ausgabe**: Das Jinja2-Template `base.html` bietet fertige Interaktion (Echtzeit-Prüfung von Sudoku, Kreuzworträtsel und Quiz, Lesefortschrittsbalken, Theme-Switch).
4. **Agenten-Fokus**: Sowohl REST als auch MCP erlauben eine unkomplizierte Anbindung an Agentensysteme (wie Claude Desktop, LangChain, CrewAI oder AutoGen).

### 1.3 Identifizierte Lücken und Limitierungen
1. **Fehlende Persistenz**: Die Zeitungsinstanzen im REST API Server (`api.newspapers`) und MCP Server liegen rein im flüchtigen Arbeitsspeicher (In-Memory). Ein Server-Neustart führt zu vollständigem Datenverlust.
2. **Eingeschränkte Exportformate**: Es existieren nur HTML und JSON. Formate wie druckfertiges PDF (Print-on-Demand) oder RSS/Atom-Feeds für News-Aggregatoren fehlen gänzlich.
3. **Keine Content-Kuration / Deduplizierung**: LLMs neigen bei autonomen Recherche-Zyklen zu redundanten Artikeln. Es existieren keine Mechanismen zur Vermeidung von Dubletten oder zur automatischen Zusammenfassung.
4. **Starres Content-Spektrum**: Neben Artikeln werden nur drei Rätseltypen unterstützt (Quiz, Sudoku, Kreuzworträtsel). Standardelemente moderner Zeitungen (z. B. Infoboxen, Wetterberichte, Börsendaten/Finanz-Ticker, Meinungsumfragen/Polls oder Wortsuchrätsel) fehlen.
5. **Kein asynchrones Task-Management**: Aufwändige Operationen (z. B. LLM-Texterzeugung, KI-Bildgenerierung) blockieren synchrone Requests; es gibt keine Webhook-Unterstützung für asynchrone Fertigstellungsmeldungen.

---

## 2. Detaillierte Feature-Vorschläge

Auf Basis der Architekturanalyse und der Anforderungen professioneller, KI-getriebener Verlagssysteme werden folgende acht Features empfohlen:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Chronicle AI Roadmap                            │
├────────────────────────────────────────────────────────────────────────┤
│  Kurzfristig (Quick Wins)        Mittelfristig (Core Expansion)        │
│  ├─ F1: Druck- & PDF-Export      ├─ F5: Persistente Speicherung        │
│  ├─ F2: Interaktive Rubriken     ├─ F6: Neue Inhaltstypen              │
│  └─ F3: Prompt-Template-System   └─ F7: Batching & Streaming           │
│                                                                        │
│  Langfristig (Ecosystem)                                               │
│  ├─ F4: RSS/Atom-Syndication                                           │
│  └─ F8: Webhook- & CMS-Integration                                     │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Feature 1: Print-Ready PDF- & Druck-Export (`PdfExporter` & Print CSS)

#### Problemstellung & Kontext
Zeitungen und Magazine werden häufig nicht nur auf Bildschirmen konsumiert, sondern als PDF archiviert, per E-Mail als E-Paper versendet oder physisch ausgedruckt. Derzeit bietet das Framework nur interaktives HTML und JSON. Zwar lässt sich HTML über den Browser drucken, jedoch fehlen Seitenumbrüche (`@page`, `break-inside: avoid`), ein mehrspaltiger Zeitungs-Umbruch für DIN-A4/US-Letter und saubere Kopf-/Fußzeilen.

#### Detaillierte Anforderungen & Spezifikation
- **Modul**: `src/newspaper/export/pdf_exporter.py` (erweitert `Exporter`).
- **Engine**: WeasyPrint oder Headless Chromium (Playwright/Puppeteer), optional mit Fallback auf paged media CSS im HTML.
- **Druck-Stylesheet**:
  - Exakte Steuerung von `@page { size: A4 portrait; margin: 15mm; }`.
  - Vermeidung von abgeschnittenen Artikeln oder verwaisten Überschriften mittels `break-after: avoid` und `page-break-inside: avoid`.
  - Druckoptimiertes Zwei-/Dreispalten-Layout für Artikeltexte (`column-count: 2`, `column-gap: 20px`).
  - Automatische Seitennummerierung ("Seite X von Y") und Ausgabedatum in der Fußzeile.
- **API-Erweiterung**:
  - `Newspaper.export_pdf(filename: str, page_format: str = "A4") -> str`.
  - REST: `POST /api/newspaper/<id>/export` mit `{"format": "pdf"}`.

#### Mehrwert & Impact
Ermöglicht den Einsatz von Chronicle AI in klassischen Print-on-Demand-Workflows, für automatisierte morgendliche E-Paper-Zustellungen und als druckfertiges PDF für Bildungseinrichtungen oder Redaktionen.

---

### Feature 2: Dynamische Rubriken-Filterung & Tagging-System

#### Problemstellung & Kontext
Das Datenmodell `Article` besitzt zwar ein Attribut `category: str`, dieses dient im HTML-Template derzeit jedoch nur als rein statisches Text-Badge. Mit wachsender Artikelanzahl verliert die generierte Zeitung schnell an Übersicht.

#### Detaillierte Anforderungen & Spezifikation
- **Modellerweiterung (`models.py`)**:
  - `tags: List[str] = field(default_factory=list)` auf `Article`.
  - `reading_time_minutes: int` (automatische Berechnung basierend auf Wortanzahl: z. B. ~200 Wörter/Minute).
- **Interaktive UI-Features (`base.html`)**:
  - Filter-Toolbar oberhalb der Artikel ("Alle", "Technologie", "Politik", "Wirtschaft" etc.) inklusive Badge mit Artikelzähler.
  - Clientseitiges Umschalten ohne Neuladen (mittels CSS-Transitions oder `data-category`-Attributen).
  - Anzeige der geschätzten Lesezeit ("⏱ 3 Min. Lesezeit") in der Artikel-Metazeile.
- **API-Erweiterung**:
  - Filterbare JSON-Generierung: `paper.generate(category="Technologie")`.
  - REST-Endpunkt zur Abfrage aller Kategorien: `GET /api/newspaper/<id>/categories`.

#### Mehrwert & Impact
Steigert die Usability und Lesefreundlichkeit für Endanwender dramatisch. LLMs können Artikeln strukturierte semantische Tags zuweisen, die dem Leser eine gezielte Navigation ermöglichen.

---

### Feature 3: LLM-Prompt-Template-Engine & Autonome Redaktions-Pipelines

#### Problemstellung & Kontext
Das Framework bezeichnet sich im Titel als *"Newspaper Framework for LLMs"*, stellt aktuell aber nur die Datenstrukturen und Ausgabeformate bereit. Die Orchestrierung von Prompts zur Generierung von Artikeln, Faktenchecks, Schlagzeilen oder Rätseln muss der Aufrufer komplett selbst implementieren.

#### Detaillierte Anforderungen & Spezifikation
- **Neues Modul (`src/newspaper/ai/`)**:
  - `prompt_templates.py`: Standardisierte Prompt-Templates (z. B. "Lead Article Prompt", "Op-Ed / Kommentar", "Quiz Generation Prompt aus Rohdaten", "Kurznachrichten Ticker").
  - `editorial_agent.py`: Abstrakter Redaktionsassistent, der unstrukturierte Rohtexte oder RSS-Feeds einliest und strukturierte `Article`-Objekte extrahiert.
- **Validierungs-Guards**:
  - Automatisches Zählen von Wörtern und Prüfung der Mindestlänge (Verhinderung von `NewspaperFrameworkError` vor der Instanziierung).
  - Automatischer Schlagzeilen-Generator (Generierung von 3 Headline-Varianten zur Auswahl).
- **MCP-Tool-Erweiterung**:
  - MCP-Tool `generate_article_prompt(topic, tone, category, length)`.

#### Mehrwert & Impact
Senkt die Integrationshürde für Entwickler von LLM-Agenten massiv. Chronicle AI wandelt sich von einer reinen Rendering-Engine zu einem ganzheitlichen Redaktions-Toolkit.

---

### Feature 4: Syndication-Engine (RSS 2.0 & Atom Feed Exporter)

#### Problemstellung & Kontext
Digitale Nachrichteninhalte müssen maschinenlesbar an andere Dienste (News-Aggregatoren, E-Mail-Newsletter, Intranet-Portale, Slack/Discord-Bots) weitergegeben werden können. Derzeit existiert nur ein proprietäres JSON-Format.

#### Detaillierte Anforderungen & Spezifikation
- **Neues Modul**: `src/newspaper/export/rss_exporter.py` und `atom_exporter.py`.
- **Standards-Konformität**:
  - RSS 2.0 Spezifikation (`<rss version="2.0">`, `<channel>`, `<item>`, `<guid>`, `<pubDate>` nach RFC 822).
  - Vollständige Enclosure-Tags für Beitragsbilder (`<enclosure url="..." type="image/jpeg" />`).
- **Methoden**:
  - `Newspaper.export_rss(filename: str) -> str`
  - `Newspaper.export_atom(filename: str) -> str`
- **REST-Endpunkt**:
  - `GET /api/newspaper/<id>/feed.xml` mit MIME-Type `application/rss+xml`.

#### Mehrwert & Impact
Ermöglicht die nahtlose Einbindung der generierten Zeitungen in Feedreader (Feedly, Inoreader) und automatisierte Social-Media-Verteilungen.

---

### Feature 5: Persistente Speicherung & Multi-Ausgaben-Verwaltung (Storage Provider)

#### Problemstellung & Kontext
Sowohl die Flask REST API (`src/api/rest.py`) als auch der MCP Server (`src/api/mcp_server.py`) halten Zeitungsinstanzen in einem einfachen Python-Dictionary (`self.newspapers: Dict[str, Newspaper]`). Bei einem Neustart oder Absturz sind alle Daten verloren. Zudem können keine vergangenen Ausgaben ("Archiv", Vorwochenausgaben) abgerufen werden.

#### Detaillierte Anforderungen & Spezifikation
- **Neues Modul (`src/newspaper/storage/`)**:
  - `base.py`: Abstrakte Basisklasse `StorageBackend` mit Methoden:
    - `save(newspaper: Newspaper) -> str`
    - `load(newspaper_id: str) -> Newspaper`
    - `list_all() -> List[Dict[str, Any]]`
    - `delete(newspaper_id: str) -> bool`
  - `sqlite_storage.py`: Leichtgewichtige SQLite-Implementierung (Zero Configuration, ideal für Serverless und lokale Workflows).
  - `filesystem_storage.py`: Speicherung von Zeitungsständen als JSON-Snapshots in einem definierten Ordner (`./data/editions/`).
- **REST API Endpunkte**:
  - `GET /api/newspaper`: Liste aller erstellten Zeitungen.
  - `GET /api/newspaper/<id>`: Abruf der Metadaten und Artikel einer bestehenden Zeitung.
  - `DELETE /api/newspaper/<id>`: Löschen einer Zeitung.

#### Mehrwert & Impact
Voraussetzung für produktive Deployments, Web-Frontends, Archivfunktionen und historische Ausgaben-Übersichten.

---

### Feature 6: Erweiterte interaktive Inhaltstypen (Wortsuchrätsel, Umfragen, Infoboxen)

#### Problemstellung & Kontext
Derzeit beschränkt sich die Unterhaltungs- und Medienecke auf Multiple-Choice-Quizzes, Sudoku und Kreuzworträtsel. Moderne Zeitungsformate leben von Meinungsumfragen (Polls), Wortsuchgittern ("Word Search") und visuellen Infoboxen ("Fakt des Tages", "Zitat der Woche", "Glossar").

#### Detaillierte Anforderungen & Spezifikation
- **Wortsuchgitter-Generator (`src/newspaper/content/wordsearch.py`)**:
  - Erzeugung von 10x10 bis 15x15 Buchstabenrastern mit versteckten Begriffen (horizontal, vertikal, diagonal).
  - Interaktives Markieren der gefundenen Wörter im HTML per Drag/Click.
- **Meinungsumfrage / Poll (`src/newspaper/content/poll.py`)**:
  - Frage mit Optionen und initialen Prozentwerten oder interaktiver Stimmabgabe mit lokaler Visualisierung via HTML5 Canvas oder animierten CSS-Balken.
- **Redaktionelle Infoboxen (`Infobox`, `QuoteBox` in `models.py`)**:
  - Hervorgehobene Zitate von Persönlichkeiten mit Autorenzeile und Porträt.
  - "Key Takeaways" / Kernaussagen-Kästen für lange Analysen.

#### Mehrwert & Impact
Macht die erzeugte Zeitung redaktionell vielseitiger und visuell ansprechender, insbesondere für Wissensmagazine und Special-Interest-Ausgaben.

---

### Feature 7: Asynchrone Generierung, Streaming & Batching

#### Problemstellung & Kontext
Die sequenzielle Erstellung von Artikeln durch LLMs dauert je nach Modell mehrere Sekunden bis Minuten. Wenn ein Agent 5 Artikel, 2 Rätsel und ein Sudoku anlegt, läuft ein synchroner HTTP-Aufruf schnell in ein Gateway-Timeout (504).

#### Detaillierte Anforderungen & Spezifikation
- **Batch-API**:
  - Neuer REST-Endpunkt `POST /api/newspaper/<id>/batch`: Entgegennahme eines kombinierten JSON-Payloads mit Artikeln, Sudokus und Quizzes in einem einzigen Aufruf.
- **Asynchrone Hintergrund-Jobs**:
  - Optionaler Einsatz von Background-Tasks (z. B. via Python `concurrent.futures` oder Celery/Redis).
  - Statusabfrage über `GET /api/newspaper/<id>/status` (`"status": "generating" | "ready" | "failed"`).
- **Streaming-Unterstützung**:
  - Server-Sent Events (SSE) für Fortschrittsmeldungen bei der Zeitungserstellung ("Sudoku generiert (1/3)", "HTML gerendert (3/3)").

#### Mehrwert & Impact
Skalierbarkeit und Stabilität bei automatisierter Massenproduktion oder komplexen Agenten-Workflows, Vermeidung von Netzwerk-Timeouts.

---

### Feature 8: Webhook- & Publishing-Integration (Discord, Slack, WordPress, Web-Push)

#### Problemstellung & Kontext
Sobald eine Zeitung fertig generiert und gerendert wurde, verbleibt die Datei lokal im Dateisystem. In autonomen Systemen soll die Fertigstellung jedoch externe Aktionen auslösen (z. B. Benachrichtigung eines Teams im Slack-Channel oder Veröffentlichung im Web-CMS).

#### Detaillierte Anforderungen & Spezifikation
- **Neues Modul (`src/newspaper/publishing/webhook.py`)**:
  - Konfigurierbare Webhooks in `Newspaper`:
    ```python
    paper.add_webhook("https://hooks.slack.com/services/...", event="on_export")
    ```
  - Standardisierter JSON-Event-Payload mit Titel, Datum, Artikelzähler, Download-Link und Zusammenfassung.
- **S3 / Cloud Storage Uploader (`src/newspaper/export/s3_uploader.py`)**:
  - Automatisches Hochladen der generierten HTML- und PDF-Dateien auf AWS S3, Cloudflare R2 oder GitHub Pages mit Rückgabe der öffentlichen URL.

#### Mehrwert & Impact
Schließt die Lücke zwischen Content-Erstellung und Content-Distribution und ermöglicht vollwertige "Headless Autonomous Publishing Pipelines".

---

## 3. Priorisierungsmatrix & Implementierungs-Roadmap

Die Vorschläge lassen sich nach **Aufwand (T-Shirt-Größe)** und **Geschäftswert / Nutzen für LLM-Agenten** bewerten:

| Feature | Aufwand | Nutzen / Impact | Empfohlene Phase |
|---|:---:|:---:|:---:|
| **F1: Print-Ready PDF- & Druck-Export** | M | Hoch | Phase 1 (Core) |
| **F2: Dynamische Rubriken-Filterung & Tags** | S | Hoch | Phase 1 (Core) |
| **F3: Prompt-Template-Engine & Pipelines** | M | Sehr hoch | Phase 1 (Core) |
| **F4: Syndication-Engine (RSS/Atom)** | S | Mittel | Phase 2 (Extension) |
| **F5: Persistente Speicherung (SQLite)** | M | Sehr hoch | Phase 2 (Extension) |
| **F6: Neue Inhaltstypen (WordSearch, Polls)** | M | Hoch | Phase 2 (Extension) |
| **F7: Batching & Async Task Management** | L | Hoch | Phase 3 (Scale) |
| **F8: Webhook- & Publishing-Integration** | M | Mittel | Phase 3 (Scale) |

*Legende: S = Gering (< 1 Sprint), M = Mittel (1-2 Sprints), L = Groß (> 2 Sprints)*

---

## 4. Fazit & Ausblick

Das Framework **Chronicle AI** verfügt bereits über ein exzellentes Fundament mit solider Typisierung, vorbildlicher Testabdeckung und modernem visuellen CI/Design.

Durch die Umsetzung der hier vorgeschlagenen Erweiterungen – insbesondere der **Druck-/PDF-Ausgabe (F1)**, der **Rubriken-Filterung (F2)**, der **Prompt-Templates (F3)** sowie der **persistenten Speicherung (F5)** – wird Chronicle AI von einer Design- und Renderbibliothek zu einer vollwertigen, produktionsreifen Redaktionsplattform für autonome KI-Agenten ausgebaut.
