# Feature-Vorschläge und Anforderungsanalyse: Chronicle AI Newspaper Framework

## 1. Executive Summary & Ist-Zustands-Analyse

Das **Chronicle AI Newspaper Framework** ist eine leichtgewichtige, modulare Python-Bibliothek, die darauf ausgelegt ist, Large Language Models (LLMs) und autonomen Agenten die strukturierte Erzeugung digitaler Zeitungen zu ermöglichen.

### Aktueller Funktionsumfang (Ist-Zustand)
- **Kernarchitektur (`src/newspaper/core.py`, `models.py`)**: Bereitstellung der zentralen Klasse `Newspaper` mit Datenstrukturen für Artikel (`Article`), Layout (`LayoutConfig`), Medien (`MediaConfig`) und Quizfragen (`Question`).
- **Inhaltsgeneratoren (`src/newspaper/content/`)**:
  - `QuizSystem`: Multiple-Choice-Fragen mit Validierung.
  - `SudokuGenerator`: Erzeugung von 9x9-Sudokus in drei Schwierigkeitsgraden inkl. Lösungsmatrix.
  - `CrosswordGenerator`: Generierung von Kreuzworträtseln basierend auf `pycrossword-generator`.
- **Exportformate (`src/newspaper/export/`)**:
  - `HtmlExporter`: Generiert eine eigenständige, interaktive HTML-Seite auf Basis eines Jinja2-Templates mit modernem UI ("Chronicle Modern Editorial"), Dark-/Light-Mode-Umschaltung, Lesefortschrittsbalken und interaktiver Überprüfung von Quiz, Sudoku und Kreuzworträtseln via JavaScript.
  - `JsonExporter`: Strukturierter Export des gesamten Zeitungsdatenmodells als JSON.
- **Schnittstellen (`src/api/`)**:
  - REST-API (`Flask`) zur Erstellung und Befüllung von Zeitungen über HTTP.
  - MCP-Server (`Model Context Protocol`) zur direkten Anbindung an KI-Assistenten und autonome Agenten.
- **Qualitätssicherung**: Vollständige Testabdeckung mit 86 pytest-Unit-Tests und Mypy-Typisierung.

### Identifizierte Limitierungen und Lücken
1. **Reines Fließtext-Rendering im Artikel**: Der Artikelinhalt wird im HTML-Template derzeit als einfacher Textabsatz (`<p>{{ article.content }}</p>`) gerendert. LLMs produzieren von Natur aus Markdown (Zwischenüberschriften, Listen, Zitate, Tabellen, Fettschrift), was aktuell ungeparst bleibt oder HTML-Tags maskiert.
2. **Fehlender Print- & PDF-Export**: Zeitungen sind traditionell auch ein Druck- bzw. PDF-Medium. Aktuell existiert ausschließlich ein Single-Page-HTML- und JSON-Export, jedoch kein mehrseitiger, druckoptimierter PDF-Export (z. B. via CSS Paged Media / WeasyPrint).
3. **Mangelnde Quellen- & Fakten-Transparenz (Fact-Checking)**: Für LLM-generierte redaktionelle Inhalte sind Transparenz bezüglich Primärquellen, Faktenabgleich und Konfidenzwerte essenziell, fehlen jedoch im Datenmodell vollständig.
4. **Fehlende dynamische redaktionelle Widgets**: Moderne digitale Ausgaben leben neben Rätseln von tagesaktuellen Informationsboxen wie Wettervorhersagen, Börsen-/Finanz-Tickern oder Infografiken.
5. **Eindimensionale Ressort-/Seitenstruktur**: Alle Artikel liegen in einer flachen Liste vor, priorisiert über Ganzzahlen (1–5). Es gibt keine Unterteilung in echte Seiten (Page 1: Titelseite, Page 2: Wirtschaft, Page 3: Feuilleton) oder Ressort-Sektionen mit separaten Kolumnen.
6. **Eingeschränkte Template- & Theming-Flexibilität**: Das Layout ist fest an ein einziges HTML-Template gebunden. Unterschiedliche Publikationsstile (z. B. klassischer Broadsheet-/Tageszeitungs-Look vs. Tech-Magazin vs. Boulevard) sind ohne Eingriff in den Core-Code nicht wählbar.
7. **Fehlende Validierungs- & Redaktions-Hooks**: Es gibt keine Pipeline-Hooks, mit denen LLM-Outputs vor der Publikation automatisch redigiert, auf Rechtschreibung/Stil geprüft oder bezüglich Längenrestriktionen gekürzt werden können.
8. **Fehlender E-Reader-/EPUB-Export**: Für mobile Offline-Nutzung auf E-Ink-Geräten (Kindle, Kobo, Tolino) fehlt ein standardisierter EPUB3-Export.

---

## 2. Detaillierte Feature-Vorschläge

Nachfolgend werden acht fundierte, priorisierte Feature-Vorschläge detailliert ausgearbeitet. Jeder Vorschlag enthält Motivation, Anwendungsfall, technische Architektur, API-Design sowie eine Nutzen- und Aufwandseinschätzung.

---

### Feature 1: Markdown- & Rich-Text-Rendering für Artikel

#### 1.1 Motivation & Anforderungskontext
Large Language Models (wie Claude, GPT-4, Llama) generieren strukturierte Texte standardmäßig im Markdown-Format (mit `## Zwischenüberschriften`, `*Aufzählungen*`, `**Hervorhebungen**`, `> Blockquotes` und Code-Snippets). Im aktuellen Framework wird `article.content` im HTML-Template in ein einziges `<p>`-Tag gepackt. Dies zerstört die Textgliederung, führt zu unleserlichen Textblöcken und verhindert professionelle typografische Hierarchien in redaktionellen Beiträgen.

#### 1.2 Technische Konzeption & Architektur
- **Modul**: `src/newspaper/content/markdown_parser.py` bzw. Integration in `src/newspaper/models.py` / `html_exporter.py`.
- **Bibliothek**: Einbindung von `markdown` oder `mistune` mit aktivierten Extensions (Tabellen, Fenced Code, typografische Anführungszeichen) oder sicheres integriertes Sanitizing.
- **Sicherheitsaspekt**: Um XSS-Sicherheitslücken vorzubeugen, muss HTML-Code innerhalb von Markdown sanitisiert werden (z. B. via `bleach` oder Whitelisting im Jinja2-Filter).
- **Template-Anpassung**: Im Template `base.html` wird `article.content | render_markdown | safe` verwendet.

#### 1.3 API-Design & Beispiel
```python
# Verwendung im Python SDK
article = paper.add_article(
    title="Die Zukunft der Agentik",
    content="""
## Paradigmenwechsel in der Softwareentwicklung
Autonome Agenten übernehmen zunehmend komplexe Aufgaben.

### Wichtigste Meilensteine:
- **MCP-Protokolle**: Einheitliche Tool-Schnittstellen
- **Selbstkorrektur**: Automatische Testschleifen

> "Code wird künftig mehr orchestriert als zeilenweise getippt."
""",
    format="markdown"  # Standardmäßig oder konfigurierbar
)
```

#### 1.4 Nutzen- & Aufwandseinschätzung
- **Priorität**: Hoch (P1)
- **Komplexität**: Gering bis Mittel (1–2 Tage)
- **Mehrwert**: Dramatische Verbesserung der typografischen Lesbarkeit und nahtlose LLM-Kompatibilität.

---

### Feature 2: Print- & PDF-Export-Engine (CSS Paged Media / WeasyPrint)

#### 2.1 Motivation & Anforderungskontext
Viele Nutzer und Unternehmen nutzen Zeitungen nicht nur am Bildschirm, sondern drucken sie aus oder archivieren sie als PDF (z. B. als morgendlicher News-Digest für die Geschäftsleitung oder personalisiertes PDF-Briefing). Ein reines Web-HTML-Layout bricht beim Drucken oft unschön um (Seitenumbrüche mitten in Bildern oder Rätseln).

#### 2.2 Technische Konzeption & Architektur
- **Modul**: `src/newspaper/export/pdf_exporter.py`
- **Technologie**: Einsatz von `WeasyPrint` oder einer leichtgewichtigen Chrome-Headless-CLI. WeasyPrint unterstützt den W3C-Standard *CSS Paged Media Module Level 3* (`@page`, `@page :left`, `@page :right`, `size: A4 portrait;`, `marks: crop cross;`, `break-inside: avoid;`).
- **Template**: Spezielles Print-Template `src/newspaper/export/templates/print_base.html` mit echtem zweispaltigem Zeitungs-Umbruch (`column-count: 2; column-gap: 5mm; text-align: justify; hyphens: auto;`).
- **Methoden-Erweiterung**: `paper.export_pdf("ausgabe.pdf", page_format="A4")`.

#### 2.3 API-Design & Beispiel
```python
# Python SDK
paper.export_pdf(
    filename="chronicle_print.pdf",
    page_format="A4",        # A4, A3, Letter
    orientation="portrait",  # portrait, landscape
    enable_print_marks=False
)

# REST API Endpoint
# POST /api/newspaper/<id>/export {"format": "pdf", "page_format": "A4"}

# MCP Tool
# export_newspaper(newspaper_id="np_0", format="pdf")
```

#### 2.4 Nutzen- & Aufwandseinschätzung
- **Priorität**: Hoch (P1)
- **Komplexität**: Mittel (3–4 Tage)
- **Mehrwert**: Ermöglicht reale Druckausgaben, Archivierung und Corporate-Executive-Briefings.

---

### Feature 3: Quellen-, Zitations- & Fact-Checking-Metadaten

#### 2.1 Motivation & Anforderungskontext
Ein Hauptproblem bei KI-generierten Inhalten ("Halluzinationen") ist die mangelnde Nachvollziehbarkeit. In journalistischen Kontexten müssen Aussagen überprüfbar sein. Bislang speichert das `Article`-Modell lediglich `author` und `category`. Metadaten zu verwendeten Quellen, URLs, Fact-Checking-Scores oder Zeitstempeln der Recherche fehlen.

#### 2.2 Technische Konzeption & Architektur
- **Modell-Erweiterung (`src/newspaper/models.py`)**:
  - `SourceReference`: Dataclass mit `title`, `url`, `publisher`, `retrieved_at`, `confidence_score`.
  - `FactCheckInfo`: Dataclass mit `verified: bool`, `checker_agent: str`, `verification_notes: str`.
  - Erweiterung von `Article` um `sources: List[SourceReference]` und `fact_check: Optional[FactCheckInfo]`.
- **UI-Darstellung im Template**:
  - Unaufdringliche Fußnoten oder ein ausklappbares Quellenverzeichnis ("Transparenz & Quellen") am Ende jedes Artikels.
  - Optionales "Verifiziert von Agent X"-Badge mit optischem Indikator.

#### 2.3 API-Design & Beispiel
```python
from src.newspaper.models import SourceReference, FactCheckInfo

paper.add_article(
    title="Durchbruch in der Fusionsenergie vermeldet",
    content="Forscher am National Ignition Facility erzielten erneut Nettoenergiegewinn...",
    sources=[
        SourceReference(
            title="NIF Research Paper 2025",
            url="https://doi.org/10.1038/example",
            publisher="Nature Energy",
            confidence_score=0.98
        )
    ],
    fact_check=FactCheckInfo(
        verified=True,
        checker_agent="FactChecker-Llama-3",
        verification_notes="Daten gegen Nature-Veröffentlichung abgeglichen."
    )
)
```

#### 2.4 Nutzen- & Aufwandseinschätzung
- **Priorität**: Hoch (P2)
- **Komplexität**: Gering bis Mittel (2 Tage)
- **Mehrwert**: Schafft Vertrauen, Transparenz und entspricht modernen journalistischen Qualitätsstandards bei KI-Inhalten.

---

### Feature 4: Dynamische Daten-Widgets (Wetter, Börse/Märkte, Ticker)

#### 4.1 Motivation & Anforderungskontext
Klassische Zeitungen bieten neben Leitartikeln essenzielle Informationsspalten: Wetterberichte, Finanzmarktdaten (Aktien, Devisen, Rohstoffe) und Kurzmeldungen (Ticker/Eilmeldungen). Aktuell unterstützt das Framework nur Quizzes, Sudoku und Kreuzworträtsel. Einbindung von Marktdaten oder Wetterberichten macht die generierte Zeitung zu einem vollständigen Tagesbegleiter.

#### 4.2 Technische Konzeption & Architektur
- **Modul**: `src/newspaper/content/widgets.py`
- **Neue Generatoren/Modelle**:
  - `WeatherWidget`: Darstellung von Wetterstationen (Stadt, Temperatur, Icon, Vorhersage).
  - `MarketTickerWidget`: Liste von Symbolen (z. B. S&P 500, DAX, Bitcoin, EUR/USD) mit aktuellem Kurs und Veränderung (+/- in Prozent).
  - `BreakingNewsTicker`: Lauftext oder Banner für Eilmeldungen am Kopf der Seite.
- **HTML/CSS-Integration**: Responsive Grid-Cards, die sich optisch harmonisch in das "Chronicle Modern Editorial"-Design einfügen.

#### 4.3 API-Design & Beispiel
```python
from src.newspaper.content.widgets import WeatherWidget, MarketTickerWidget

# Wetter-Widget
weather = WeatherWidget(city="Zürich", condition="Sonnig", temp_c=18, forecast=["Sa: 19°C", "So: 16°C"])
paper.add_widget(weather)

# Finanz-Ticker
market = MarketTickerWidget(entries=[
    {"symbol": "DAX", "value": "18.450", "change": "+0.6%"},
    {"symbol": "BTC/EUR", "value": "62.300", "change": "-1.2%"},
    {"symbol": "EUR/USD", "value": "1.085", "change": "+0.1%"}
])
paper.add_widget(market)
```

#### 4.4 Nutzen- & Aufwandseinschätzung
- **Priorität**: Mittel (P2)
- **Komplexität**: Mittel (2–3 Tage)
- **Mehrwert**: Signifikante Aufwertung des Informationswerts für den täglichen Leser.

---

### Feature 5: Multi-Seiten- & Ressort-Architektur (Sections / Pages)

#### 5.1 Motivation & Anforderungskontext
Derzeit werden alle Artikel in einer flachen Liste gesammelt und lediglich nach Priorität sortiert. Große Tageszeitungen gliedern Inhalte jedoch zwingend in Ressorts (z. B. Titelseite, Politik & Weltgeschehen, Wirtschaft, Kultur & Wissen, Sport, Feuilleton/Rätsel). Eine feste Ressort-Strukturierung ermöglicht agentischen Redaktionssystemen, spezialisierte Sub-Agenten für einzelne Ressorts arbeiten zu lassen.

#### 5.2 Technische Konzeption & Architektur
- **Modell-Erweiterung (`src/newspaper/models.py`)**:
  - `Section` / `Ressort`: Besitzt `name`, `slug`, `lead_article`, `articles: List[Article]`, `widgets: List[Any]`.
  - `Newspaper.add_section(name="Wirtschaft")` oder automatische Gruppierung nach `article.category`.
- **Navigation & Layout**:
  - Im Web: Tab-Navigation oder strukturierte Kapitelnavigation mit Sprungmarken und Ressort-Köpfen.
  - Im Druck/PDF: Automatischer Seitenumbruch (`break-before: page`) bei Beginn eines neuen Ressorts.

#### 5.3 API-Design & Beispiel
```python
# Explizite Ressort-Steuerung
titelseite = paper.create_section("Titelseite", priority=1)
titelseite.add_article(lead_story)

wirtschaft = paper.create_section("Wirtschaft & Finanzen", priority=2)
wirtschaft.add_article(market_analysis)
wirtschaft.add_widget(market_ticker)

feuilleton = paper.create_section("Rätsel & Freizeit", priority=3)
feuilleton.add_crossword(cw)
feuilleton.add_sudoku("hard")
```

#### 5.4 Nutzen- & Aufwandseinschätzung
- **Priorität**: Hoch (P1)
- **Komplexität**: Mittel (3–4 Tage)
- **Mehrwert**: Skalierbarkeit für vollwertige, vielseitige Zeitungsausgaben; perfekte Schnittstelle für modulare Multi-Agenten-Architekturen.

---

### Feature 6: Template-Engine & Theme-Presettings

#### 6.1 Motivation & Anforderungskontext
Das aktuelle HTML-Template bietet ein modernes Dark/Light-Editorial-Layout. Zeitungen und Magazine besitzen jedoch stark divergierende visuelle Identitäten:
- **Klassische Tageszeitung (Broadsheet)**: Serifenschriften, vertikale Trennlinien, kompakte Kolumnen (FAZ-, NYT- oder NZZ-Stil).
- **Tech-Magazin (Modern Clean)**: Sans-Serif, großzügiges Spacing, Monospace-Badges (Wired- oder The Verge-Stil).
- **Minimalistisches Newsletter-Format**: Einspaltig, hochgradig lesbar auf Smartphones (Substack- oder Morning-Brew-Stil).

#### 6.2 Technische Konzeption & Architektur
- **Modul**: `src/newspaper/export/themes/`
- **Konzept**: Entkopplung von HTML-Skelett und Styling über Theme-Registrierungen.
- **Vordefinierte Themes**:
  - `Theme.BROADSHEET`
  - `Theme.TECH_DIGEST`
  - `Theme.MINIMAL_NEWSLETTER`
- Das `LayoutConfig`-Objekt wird um das Attribut `theme: str = "modern_editorial"` erweitert; eigene Template-Pfade können benutzerdefiniert injiziert werden.

#### 6.3 API-Design & Beispiel
```python
from src.newspaper.models import LayoutConfig, Theme

# Auswahl eines vordefinierten Themes
paper = Newspaper(
    title="The Daily Tech Wire",
    layout=LayoutConfig(
        theme=Theme.TECH_DIGEST,
        primary_color="#0066cc",
        columns=3
    )
)

# Oder benutzerdefiniertes Template:
paper.set_custom_template("path/to/my_custom_template.html")
```

#### 6.4 Nutzen- & Aufwandseinschätzung
- **Priorität**: Mittel (P2)
- **Komplexität**: Mittel (2–3 Tage)
- **Mehrwert**: Hohe Flexibilität für unterschiedliche Anwendungsbereiche (Unternehmenszeitung, Fachmagazin, Schülerzeitung).

---

### Feature 7: Redaktionelle Pipeline-Hooks & Auto-Editing (Lektorat)

#### 7.1 Motivation & Anforderungskontext
Wenn autonome LLM-Agenten Zeitungen füllen, entstehen gelegentlich Texte mit redundanten Phrasen, unpassenden Längen für das gewählte Layout oder Stilbrüchen. Derzeit gibt es nur eine rudimentäre Prüfung (`len(content) >= 10`). Ein erweiterbares Hook-System ermöglicht automatische Vor- und Nachbereitung von Beiträgen.

#### 7.2 Technische Konzeption & Architektur
- **Modul**: `src/newspaper/pipeline.py`
- **Hook-Schnittstellen**:
  - `pre_add_article_hook(article: Article) -> Article`
  - `post_generate_hook(newspaper_data: dict) -> dict`
- **Integrierte Beispiel-Hooks**:
  - `ReadingTimeEstimator`: Berechnet die geschätzte Lesezeit ("3 Min. Lesezeit") basierend auf der Wortanzahl und fügt sie den Metadaten hinzu.
  - `HeadlineSanitizer`: Bereinigt automatisch Clickbait- oder LLM-typische Füllfloskeln.
  - `SummaryGenerator`: Generiert bei Bedarf automatisch einen 2-Satz-Teaser/Abstract, falls das Modell diesen nicht mitgeliefert hat.

#### 7.3 API-Design & Beispiel
```python
from src.newspaper.pipeline import ReadingTimeCalculator, ContentTrimmer

# Pipeline-Hooks an die Zeitung binden
paper.register_hook(ReadingTimeCalculator(wpm=220))
paper.register_hook(ContentTrimmer(max_words=800, add_ellipsis=True))

# Beim Hinzufügen des Artikels wird die Lesezeit automatisch berechnet
art = paper.add_article(title="Quantencomputing", content="...")
print(art.reading_time_minutes) # -> 4
```

#### 7.4 Nutzen- & Aufwandseinschätzung
- **Priorität**: Mittel (P3)
- **Komplexität**: Gering bis Mittel (2 Tage)
- **Mehrwert**: Erhöht die redaktionelle Konsistenz und Reife im autonomen KI-Agenten-Betrieb.

---

### Feature 8: EPUB3- & E-Reader-Export

#### 8.1 Motivation & Anforderungskontext
Viele Leser konsumieren längere Artikel und Wochenendzeitungen bevorzugt auf E-Book-Readern (z. B. Kindle, Kobo, Tolino) aufgrund der augenschonenden E-Ink-Displays und langen Akkulaufzeiten. Weder HTML noch klassisches DIN-A4-PDF lassen sich auf 6- oder 7-Zoll-E-Readern angenehm lesen, da dort responsiver E-Book-Textfluss (Reflowable Content) benötigt wird.

#### 8.2 Technische Konzeption & Architektur
- **Modul**: `src/newspaper/export/epub_exporter.py`
- **Bibliothek**: `EbookLib` (Standardbibliothek für EPUB2/EPUB3 in Python).
- **Aufbau**:
  - Jedes Ressort oder jeder Hauptartikel wird als separates XHTML-Kapitel (`EpubHtml`) eingebunden.
  - Generierung eines standardkonformen Inhaltsverzeichnisses (TOC) und Metadaten (Dublin Core: Titel, Datum, Autor, Sprache).
  - Einbettung von Bildern und CSS für E-Ink-Optimierung (hoher Kontrast, keine überflüssigen Animationen).

#### 8.3 API-Design & Beispiel
```python
# Python SDK
paper.export_epub(
    filename="meine_zeitung.epub",
    cover_image="assets/cover.jpg",
    language="de"
)

# REST API & MCP
# POST /api/newspaper/<id>/export {"format": "epub"}
```

#### 8.4 Nutzen- & Aufwandseinschätzung
- **Priorität**: Mittel (P3)
- **Komplexität**: Mittel (2–3 Tage)
- **Mehrwert**: Erschließt E-Ink- und Mobile-Reader-Zielgruppen; ideale Ergänzung für morgendliche automatische E-Paper-Zustellung.

---

## 3. Priorisierungs- & Roadmap-Matrix

In folgender Übersicht werden die vorgeschlagenen Features anhand von geschätztem Entwicklungsaufwand, strategischem Mehrwert und Implementierungspriorität eingeordnet:

| Nr. | Feature-Vorschlag | Priorität | Entwicklungsaufwand | Redaktioneller & Technischer Mehrwert |
|:---:|:------------------|:---------:|:-------------------:|:--------------------------------------|
| **1** | **Markdown- & Rich-Text-Rendering** | **P1 (Sofort)** | Gering (1–2 Tage) | **Sehr hoch**: Beseitigt sofort die größte Formatierungslücke bei LLM-generierten Texten. |
| **2** | **Print- & PDF-Engine (WeasyPrint)** | **P1 (Sofort)** | Mittel (3–4 Tage) | **Sehr hoch**: Ergänzt die Zeitung um das essenzielle klassische Druck- und Archivformat. |
| **3** | **Quellen & Fact-Checking-Metadaten** | **P2 (Kurzfristig)** | Gering (2 Tage) | **Hoch**: Schafft Glaubwürdigkeit und Transparenz für KI-generierte Inhalte. |
| **4** | **Multi-Seiten- & Ressort-Architektur** | **P1 (Sofort)** | Mittel (3–4 Tage) | **Sehr hoch**: Grundvoraussetzung für vollwertige Zeitungen mit Multi-Agenten-Workflows. |
| **5** | **Dynamische Widgets (Wetter, Börse)** | **P2 (Kurzfristig)** | Mittel (2–3 Tage) | **Mittel bis Hoch**: Rundet das Erscheinungsbild einer vollwertigen Tageszeitung ab. |
| **6** | **Template- & Theming-Engine** | **P2 (Kurzfristig)** | Mittel (2–3 Tage) | **Hoch**: Ermöglicht individuelle Markenauftritte (Broadsheet, Tech-News, Minimal). |
| **7** | **Lektorats- & Pipeline-Hooks** | **P3 (Mittelfristig)** | Gering bis Mittel (2 Tage) | **Mittel**: Erhöht Textqualität und berechnet Metadaten (z. B. Lesezeit) autonom. |
| **8** | **EPUB3- / E-Reader-Export** | **P3 (Mittelfristig)** | Mittel (2–3 Tage) | **Mittel bis Hoch**: Erschließt Offline-E-Ink-Hardware für E-Paper-Abonnenten. |

---

## 4. Konkrete Handlungsempfehlung für die nächste Iteration

Für den direkten nächsten Entwicklungssprint wird empfohlen, mit den drei **P1-Features** zu beginnen:

1. **Sprint 1: Markdown-Integration**: Implementierung eines sicheren Markdown-Renders für `Article.content`, sodass Fettungen, Zwischenüberschriften, Zitate und Listen sofort in HTML sauber dargestellt werden.
2. **Sprint 2: Ressort-/Sektions-Architektur**: Erweiterung der Datenstruktur um `Section`, um Artikel nicht nur nach Priorität, sondern thematisch gegliedert darzustellen.
3. **Sprint 3: PDF-Export via WeasyPrint**: Bereitstellung eines druckfertigen PDF-Layouts inklusive CSS Paged Media `@page`-Regeln für A4-Druck.

Mit diesen Erweiterungen wächst das **Chronicle AI Newspaper Framework** von einem Proof-of-Concept-Generator zu einem professionellen, industrietauglichen Publikationssystem für autonome Redaktionen heran.
