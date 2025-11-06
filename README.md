# Newspaper Framework für LLMs

Ein einfaches, fehlertolerantes Framework für KI-gestützte Zeitungsproduktion.

##   Ziel

Ermöglicht es LLMs, hochwertige Morgenzeitungen mit minimalem Aufwand zu erstellen, während das Framework für konsistente Qualität und automatische Fehlerkorrektur sorgt.

##   Schnellstart

```python
from newspaper_framework import NewspaperFrameWork

# Framework erstellen
paper = NewspaperFrameWork("AI Morgenzeitung")

# Artikel hinzufügen (das LLM ersetzt diese mit eigenen Inhalten)
paper.add_article(
    title="KI revolutioniert Zeitungswesen",
    content="Neue Framework erleichtert KI-gestützte Zeitungsproduktion...",
    author="KI-Redakteur",
    category="Technologie",
    priority=1
)

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

##  📖 Dokumentation für LLMs

### Wichtige Methoden:

1. **`NewspaperFrameWork(title)`** - Framework erstellen
2. **`add_article(title, content, **kwargs)** - Artikel hinzufügen
3. **`generate()`** - Zeitung validieren und strukturieren
3. **`export_html(filename)`** - Als HTML exportieren
4. **`export_json(filename)`** - Als JSON exportieren

### Beispiel für das LLM:

```python
# Framework erstellen
paper = NewspaperFrameWork("Meine Morgenzeitung")

# Artikel mit eigenen Inhalten ersetzen:
paper.add_article(
    title="Dein Artikel-Titel",
    content="Dein ausführlicher Artikelinhalt...",
    author="Dein Name",
    category="Deine Kategorie",
    priority=1  # 1-5, 1 = höchste Priorität
)
```

##   Fehlerbehandlung

Das Framework erkennt und korrigiert automatisch:
-  ❌ Zu kurze Artikelinhalte
-  ❌ Fehlende Titel
-  ❌ Ungültige Prioritäten

##  📄 Export-Formate

- **HTML**: Responsive Webseite mit sauberem Design
- **JSON**: Strukturierte Daten für weitere Verarbeitung
- **PDF**: Optional mit reportlab (falls installiert)

##  🔧 Erweiterung

Das Framework ist modular aufgebaut und kann einfach erweitert werden.

---

**Entwickelt speziell für KI-gestützte Zeitungsproduktion**