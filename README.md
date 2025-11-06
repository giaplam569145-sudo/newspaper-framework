# Newspaper Framework für LLMs

Ein einfaches, fehlertolerantes Framework für KI-gestützte Zeitungsproduktion mit erweiterten Medienfunktionen.

##   Ziel

Ermöglicht es LLMs, hochwertige Morgenzeitungen mit minimalem Aufwand zu erstellen, während das Framework für konsistente Qualität und automatische Fehlerkorrektur sorgt.

##   Schnellstart

```python
from newspaper_framework import NewspaperFrameWork, QuizSystem

# Framework erstellen
paper = NewspaperFrameWork("AI Morgenzeitung")

# Artikel hinzufügen (das LLM ersetzt diese mit eigenen Inhalten)
paper.add_article(
    title="KI revolutioniert Zeitungswesen",
    content="Neue Framework erleichtert KI-gestützte Zeitungsproduktion...",
    author="KI-Redakteur",
    category="Technologie",
    priority=1,
    image_path="tech_image.jpg",
    image_caption="KI in der Medienproduktion"
)

# Logo setzen
paper.set_logo("logo.png")

# Quiz hinzufügen
quiz = QuizSystem("Technologie-Quiz")
quiz.add_question(
    "Was ist KI?",
    ["Künstliche Intelligenz", "Küche International", "Kaufmanns-Institut", "Keine Ahnung"],
    0,
    "Technologie"
)
paper.add_quiz(quiz)

# Sudoku hinzufügen
paper.add_sudoku("medium")

# Exportieren
paper.export_html("meine_zeitung.html")
paper.export_json("meine_zeitung.json")
```

##  📋 Features

- ✅ **LLM-freundliche API**: Intuitive Methodennamen und klare Rückmeldungen
- ✅ **Automatische Validierung**: Inhalte werden automatisch geprüft und korrigiert
- ✅ **Design-System**: Konsistente Layouts ohne Design-Overhead
- ✅ **Fehlertolerant**: Sanfte Korrekturen statt harter Fehler
- ✅ **Ein-File-Lösung**: Einfache Distribution per Chat-Nachricht
- ✅ **Responsive Export**: HTML, JSON, PDF (optional)
- ✅ **Token-effizient**: LLMs können sich auf Inhalt konzentrieren
- ✅ **Konsistente Qualität**: Garantierte Ausgabequalität
- ✅ **Logo/Banner-Integration**: Einfache Logo-Verwaltung
- ✅ **Bildunterstützung**: Artikelbilder mit Captions
- ✅ **Interaktive Quiz**: Frage-Antwort-Systeme
- ✅ **Sudoku-Rätsel**: Automatische Sudoku-Generierung
- ✅ **Responsive Design**: Mobile-optimierte Ausgabe

##  ️ Installation

```python
# Einfach die Datei herunterladen und importieren
import newspaper_framework
```

##   Design-Prinzipien

### 1. LLM-First
- Methodennamen wie `add_article()` statt `append_content()`
- Klare Erfolgs-/Fehlermeldungen mit Emojis
- Automatische Inhaltsvalidierung und -korrektur
- Hilfreiche Warnungen statt kryptischer Fehlermeldungen

### 2. Fehlertoleranz
- Kurze Artikel werden automatisch ergänzt
- Fehlerhafte Eingaben werden sanft korrigiert
- Fehlende Bilder erzeugen Warnungen, keine Abbrüche

### 3. Medienintegration
- Einfache Logo-Verwaltung
- Bildunterstützung für Artikel
- Interaktive Elemente (Quiz, Sudoku)

##  📖 Dokumentation für LLMs

### Wichtige Methoden:

#### `add_article(title, content, **kwargs)`
Fügt einen Artikel hinzu mit automatischer Validierung.

#### `set_logo(logo_path)`
Setzt ein Logo für die Zeitung.

#### `add_quiz(quiz)`
Fügt ein interaktives Quiz hinzu.

#### `add_sudoku(difficulty="medium")`
Fügt ein Sudoku-Rätsel hinzu.

#### `export_html(filename)`
Exportiert als responsive HTML-Datei.

#### `export_json(filename)`
Exportiert als strukturierte JSON-Datei.

### Fehlerbehandlung:
- `NewspaperFrameworkWarning` für LLM-freundliche Meldungen
- Automatische Korrekturen bei möglichen Fehlern
- Kontinuierliche Verarbeitung auch bei Teilfehlern

##  🎨 Beispiele

### Zeitung mit allen Features
```python
from newspaper_framework import NewspaperFrameWork, QuizSystem

paper = NewspaperFrameWork("Vollständige Zeitung")
paper.set_logo("logo.png")

# Mehrere Artikel
paper.add_article("Titel 1", "Inhalt 1...", priority=1, category="Politik")
paper.add_article("Titel 2", "Inhalt 2...", priority=2, category="Wirtschaft")

# Quiz
quiz = QuizSystem("Tagesquiz")
quiz.add_question("Frage?", ["Option 1", "Option 2"], 0)
paper.add_quiz(quiz)

# Sudoku
paper.add_sudoku("hard")

paper.export_html("complete.html")
```

### Angepasstes Layout
```python
from newspaper_framework import NewspaperFrameWork, LayoutConfig

layout = LayoutConfig(
    font_family="Times New Roman",
    primary_color="#1a1a1a",
    max_width=1000,
    columns=3
)

paper = NewspaperFrameWork("Premium Zeitung", layout=layout)
```

##  📄 Dateien

- `newspaper_framework.py` - Haupt-Framework
- `API_DOKUMENTATION.md` - Detaillierte API-Referenz
- `README.md` - Diese Übersicht
- `QWEN.md` - Projektkontext

##  🔄 Version 2.0 Features

- **Neu**: Logo/Banner-Integration
- **Neu**: Bildunterstützung für Artikel
- **Neu**: Interaktive Quiz-Systeme
- **Neu**: Sudoku-Rätsel-Generierung
- **Neu**: Verbesserte Fehlerbehandlung
- **Neu**: Responsive Design-Systeme
- **Neu**: Erweiterte Export-Formate

##  🤖 Für LLMs

Dieses Framework wurde speziell für KI-Systeme entwickelt:

1. **Einfache API**: Klare Methodennamen und Parameter
2. **Automatische Korrektur**: Fokus auf Inhalt statt auf Fehlerbehebung
3. **Konsistente Qualität**: Garantierte Ausgabequalität
4. **Token-Effizienz**: Minimale Overhead-Komplexität
5. **Fehlertoleranz**: Robuste Verarbeitung auch bei unvollständigen Daten

##  📞 Support

Bei Fragen oder Problemen:
1. Prüfen Sie die API-Dokumentation
2. Validieren Sie Ihre Eingabedaten
3. Nutzen Sie die automatische Fehlerkorrektur

---

*Entwickelt mit ❤️ für KI-gestützte Zeitungsproduktion*