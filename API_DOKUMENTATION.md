# Newspaper Framework für LLMs - API-Dokumentation

## Übersicht

Das Newspaper Framework ist eine LLM-optimierte Python-Bibliothek zur Erstellung hochwertiger Zeitungen mit minimalen Aufwand.

## Schnellstart

```python
from newspaper_framework import NewspaperFrameWork

# Zeitung erstellen
paper = NewspaperFrameWork("Meine Morgenzeitung")

# Artikel hinzufügen
paper.add_article(
    title="Ihr Artikel-Titel",
    content="Ihr ausführlicher Artikelinhalt...",
    author="Ihr Name",
    category="Ihre Kategorie",
    priority=1
)

# Exportieren
paper.export_html("zeitung.html")
```

## Hauptklassen

### NewspaperFrameWork

Die Hauptklasse für Zeitungserstellung.

**Konstruktor:**
```python
NewspaperFrameWork(title="Morgenzeitung", layout=None, media=None)
```

**Methoden:**

#### `add_article(title, content, **kwargs)`
Fügt einen Artikel zur Zeitung hinzu.

**Parameter:**
- `title` (str): Artikel-Titel
- `content` (str): Artikel-Inhalt (min. 10 Zeichen)
- `author` (str, optional): Autorname (Standard: "Unbekannt")
- `category` (str, optional): Artikel-Kategorie (Standard: "Allgemein")
- `priority` (int, optional): Priorität 1-5 (Standard: 1)
- `image_path` (str, optional): Pfad zum Artikelbild
- `image_caption` (str, optional): Bildunterschrift

**Rückgabe:** `Article` Objekt

**Beispiel:**
```python
paper.add_article(
    title="KI revolutioniert Zeitungswesen",
    content="Neue Framework erleichtert KI-gestützte Zeitungsproduktion...",
    author="KI-Redakteur",
    category="Technologie",
    priority=1,
    image_path="tech_image.jpg",
    image_caption="KI in der Medienproduktion"
)
```

#### `set_logo(logo_path)`
Setzt ein Logo für die Zeitung.

**Parameter:**
- `logo_path` (str): Pfad zur Logo-Datei

**Rückgabe:** `bool` - True bei Erfolg

#### `add_quiz(quiz)`
Fügt ein Quiz zur Zeitung hinzu.

**Parameter:**
- `quiz` (QuizSystem): QuizSystem-Instanz

**Rückgabe:** `QuizSystem` Objekt

#### `add_sudoku(difficulty="medium")`
Fügt ein Sudoku-Rätsel hinzu.

**Parameter:**
- `difficulty` (str): "easy", "medium", "hard"

**Rückgabe:** `SudokuGenerator` Objekt

#### `export_html(filename="zeitung.html")`
Exportiert die Zeitung als HTML-Datei.

**Parameter:**
- `filename` (str): Dateiname

**Rückgabe:** `str` - HTML-Inhalt

#### `export_json(filename="zeitung.json")`
Exportiert die Zeitung als JSON-Datei.

**Parameter:**
- `filename` (str): Dateiname

**Rückgabe:** `str` - JSON-String

### QuizSystem

Klasse für interaktive Quiz-Inhalte.

**Konstruktor:**
```python
QuizSystem(title="Tagesquiz")
```

**Methoden:**

#### `add_question(question, options, correct_index, category="Allgemein")`
Fügt eine Frage zum Quiz hinzu.

**Parameter:**
- `question` (str): Die Frage (min. 5 Zeichen)
- `options` (List[str]): Liste der Antwortoptionen (min. 2)
- `correct_index` (int): Index der korrekten Antwort
- `category` (str, optional): Frage-Kategorie

**Rückgabe:** `Question` Objekt

**Beispiel:**
```python
quiz = QuizSystem("Technologie-Quiz")
quiz.add_question(
    "Was ist KI?",
    ["Künstliche Intelligenz", "Küche International", "Kaufmanns-Institut"],
    0,
    "Technologie"
)
```

### SudokuGenerator

Klasse für Sudoku-Rätsel.

**Konstruktor:**
```python
SudokuGenerator(difficulty="medium")
```

**Methoden:**

#### `generate()`
Generiert ein neues Sudoku-Rätsel.

**Rückgabe:** `List[List[int]]` - 9x9 Sudoku-Grid

#### `to_html()`
Konvertiert das Sudoku in HTML-Format.

**Rückgabe:** `str` - HTML-Tabelle

## Konfigurationsklassen

### LayoutConfig

Konfiguration für das Zeitungslayout.

**Attribute:**
- `font_family` (str): Schriftart (Standard: "Arial")
- `primary_color` (str): Primärfarbe (Standard: "#2c3e50")
- `secondary_color` (str): Sekundärfarbe (Standard: "#3498db")
- `max_width` (int): Maximale Breite in Pixeln (Standard: 800)
- `columns` (int): Spaltenanzahl (Standard: 2)
- `spacing` (int): Abstand zwischen Elementen (Standard: 20)

### MediaConfig

Konfiguration für Medieninhalte.

**Attribute:**
- `logo_path` (str, optional): Pfad zum Logo
- `logo_width` (int): Logo-Breite in Pixeln (Standard: 200)
- `logo_height` (int): Logo-Höhe in Pixeln (Standard: 60)
- `image_quality` (int): Bildqualität (Standard: 85)
- `supported_formats` (List[str]): Unterstützte Bildformate

## Fehlerbehandlung

Das Framework verwendet `NewspaperFrameworkWarning` für LLM-freundliche Fehlermeldungen:

- **Kurze Artikel**: Werden automatisch ergänzt
- **Fehlende Bilder**: Erzeugen Warnungen, brechen aber nicht den Prozess
- **Ungültige Quiz-Fragen**: Werden vor dem Hinzufügen validiert
- **Dateifehler**: Werden abgefangen mit hilfreichen Meldungen

## Beispiele

### Vollständige Zeitung mit allen Features

```python
from newspaper_framework import NewspaperFrameWork, QuizSystem

# Zeitung erstellen
paper = NewspaperFrameWork("AI Morgenzeitung")

# Logo setzen
paper.set_logo("logo.png")

# Artikel mit Bild hinzufügen
paper.add_article(
    title="KI revolutioniert Zeitungswesen",
    content="Das Newspaper Framework ermöglicht...",
    author="KI-Redakteur",
    category="Technologie",
    priority=1,
    image_path="ai_image.jpg",
    image_caption="KI in der Medienproduktion"
)

# Quiz erstellen und hinzufügen
quiz = QuizSystem("Tagesquiz")
quiz.add_question(
    "Was ist KI?",
    ["Künstliche Intelligenz", "Küche International"],
    0
)
paper.add_quiz(quiz)

# Sudoku hinzufügen
paper.add_sudoku("medium")

# Exportieren
paper.export_html("complete_newspaper.html")
paper.export_json("complete_newspaper.json")
```

### Zeitungskonfiguration anpassen

```python
from newspaper_framework import NewspaperFrameWork, LayoutConfig, MediaConfig

# Layout anpassen
layout = LayoutConfig(
    font_family="Times New Roman",
    primary_color="#1a1a1a",
    secondary_color="#e74c3c",
    max_width=1000,
    columns=3
)

# Medienkonfiguration
media = MediaConfig(
    logo_width=300,
    logo_height=100,
    image_quality=90
)

# Zeitung mit angepasster Konfiguration
paper = NewspaperFrameWork("Premium Zeitung", layout=layout, media=media)
```

## Best Practices für LLMs

1. **Titel prägnant halten**: Kurze, aussagekräftige Titel
2. **Inhalte validieren**: Mindestlänge von 10 Zeichen beachten
3. **Prioritäten nutzen**: Wichtige Artikel mit priority=1 markieren
4. **Kategorien konsistent**: Gleiche Kategorienamen verwenden
5. **Bilder prüfen**: Pfadangaben vor dem Hinzufügen validieren
6. **Quiz-Fragen testen**: Korrekte Antwortindizes sicherstellen

## Export-Formate

### HTML
- Responsives Design
- Automatische Themes
- Druckoptimiert
- Interaktive Quiz und Sudoku

### JSON
- Strukturierte Daten
- Vollständige Metadaten
- Maschinenlesbar
- API-kompatibel