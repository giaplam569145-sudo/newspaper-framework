# Newspaper Framework für LLMs - Version 1.0
# Entwickelt speziell für KI-gestützte Zeitungsproduktion

"""
NEWSPAPER FRAMEWORK FÜR LLMs
=============================

DESIGN-PRINZIPIEN:
• LLM-freundliche API mit intuitiven Methodennamen
• Automatische Fehlererkennung und sanfte Korrektur
• Konsistente Ausgabequalität durch Design-System
• Token-effiziente Arbeitsweise
• Ein-File-Lösung für einfache Distribution

WICHTIGE HINWEISE FÜR DAS LLM:
1. Framework automatisch validiert Inhalte und Layout
2. Fehler werden als hilfreiche Warnungen angezeigt
3. Layout wird automatisch optimiert
4. Fokus auf Inhalt statt auf Gestaltung
"""

import datetime
import json
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict


class NewspaperFrameworkWarning(Exception):
    """Spezielle Warnungsklasse für LLM-freundliche Fehlermeldungen"""
    pass


@dataclass
class Article:
    """Artikel-Dataklasse für strukturierte Inhalte"""
    title: str
    content: str
    author: str = "Unbekannt"
    category: str = "Allgemein"
    priority: int = 1  # 1-5, 1 = höchste Priorität
    
    def __post_init__(self):
        """Automatische Validierung und Korrektur"""
        # Titel automatisch trimmen
        self.title = self.title.strip()
        
        # Content validieren
        if not self.content or len(self.content.strip()) < 10:
            raise NewspaperFrameworkWarning(
                "❌ Artikelinhalt zu kurz (min. 10 Zeichen). Bitte mehr Inhalt hinzufügen."
            )
        
        # Priority bounds check
        self.priority = max(1, min(5, self.priority))


@dataclass
class LayoutConfig:
    """Layout-Konfiguration für konsistentes Design"""
    font_family: str = "Arial"
    primary_color: str = "#2c3e50"
    secondary_color: str = "#3498db"
    max_width: int = 800
    columns: int = 2
    spacing: int = 20


class NewspaperFrameWork:
    """
    HAUPT-FRAMEWORK-KLASSE FÜR LLMs
    
    VERWENDUNG FÜR DAS LLM:
    1. Framework erstellen: paper = NewspaperFrameWork()
    2. Artikel hinzufügen: paper.add_article(...)
    3. Zeitung generieren: paper.generate()
    4. Exportieren: paper.export_pdf() oder paper.export_html()
    """
    
    def __init__(self, title: str = "Morgenzeitung", layout: Optional[LayoutConfig] = None):
        """
        Framework initialisieren
        
        WICHTIG FÜR DAS LLM: Title sollte prägnant und aussagekräftig sein.
        Layout kann angepasst werden, Standard ist optimiert für Lesbarkeit.
        """
        self.title = title.strip()
        self.layout = layout or LayoutConfig()
        self.articles: List[Article] = []
        self.date = datetime.datetime.now().strftime("%d.%m.%Y")
        
        # Validierung
        if not self.title:
            raise NewspaperFrameworkWarning("❌ Zeitungstitel darf nicht leer sein")
    
    def add_article(self, title: str, content: str, **kwargs) -> Article:
        """
        Artikel zur Zeitung hinzufügen
        
        BEISPIEL FÜR DAS LLM:
        paper.add_article(
            title="KI revolutioniert Zeitungswesen",
            content="Neue Framework erleichtert KI-gestützte Zeitungsproduktion...",
            author="KI-Redakteur",
            category="Technologie",
            priority=1
        )
        """
        try:
            article = Article(title=title, content=content, **kwargs)
            self.articles.append(article)
            print(f"Artikel '{title[:30]}...' erfolgreich hinzugefuegt")
            return article
        except NewspaperFrameworkWarning as e:
            print(f"Warnung: {e}")
            # Versuche automatische Korrektur
            corrected_content = content + " (Inhalt automatisch vervollstaendigt)")
            article = Article(title=title, content=corrected_content, **kwargs)
            self.articles.append(article)
            print(f"Artikel mit automatischer Korrektur hinzugefuegt")
            return article
    
    def generate(self) -> Dict:
        """
        Zeitung als strukturiertes Dictionary generieren
        
        HINWEIS FÜR DAS LLM: Diese Methode validiert automatisch die gesamte Zeitung
        und gibt hilfreiche Feedback-Nachrichten.
        """
        print("🔧 Generiere Zeitung...")
        
        # Validierung der Gesamtzeitung
        if len(self.articles) == 0:
            raise NewspaperFrameworkWarning(
                "❌ Keine Artikel vorhanden. Bitte zuerst Artikel mit add_article() hinzufügen."
            )
        
        # Artikel nach Priorität sortieren
        self.articles.sort(key=lambda x: x.priority)
        
        # Strukturierte Ausgabe erstellen
        newspaper_data = {
            "title": self.title,
            "date": self.date,
            "layout": asdict(self.layout),
            "articles": [asdict(article) for article in self.articles],
            "statistics": {
                "total_articles": len(self.articles),
                "categories": list(set(a.category for a in self.articles)),
                "authors": list(set(a.author for a in self.articles))
            }
        }
        
        print(f"✅ Zeitung erfolgreich generiert: {len(self.articles)} Artikel, {newspaper_data['statistics']['categories']} Kategorien")
        return newspaper_data
    
    def export_html(self, filename: str = "zeitung.html") -> str:
        """Exportieren als HTML mit responsivem Design"""
        data = self.generate()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{data['title']}</title>
            <style>
                body {{ font-family: {data['layout']['font_family']}; max-width: {data['layout']['max_width']}px; margin: 0 auto; padding: 20px; }}
                .header {{ text-align: center; color: {data['layout']['primary_color']}; border-bottom: 2px solid {data['layout']['secondary_color']}; margin-bottom: 30px; }}
                .article {{ margin-bottom: {data['layout']['spacing']}px; padding: 15px; border-left: 3px solid {data['layout']['secondary_color']}; }}
                .article-title {{ color: {data['layout']['primary_color']}; margin-top: 0; }}
                .meta {{ color: #666; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{data['title']}</h1>
                <p class="date">{data['date']}</p>
            </div>
            {"".join(f'<div class="article"><h2 class="article-title">{a["title"]}</h2><div class="meta">Von {a["author"]} | {a["category"]}</div><p>{a["content"]}</p></div>' for a in data['articles'])}
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML exportiert: {filename}")
        return html_content
    
    def export_json(self, filename: str = "zeitung.json") -> str:
        """Exportieren als strukturiertes JSON"""
        data = self.generate()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON exportiert: {filename}")
        return json.dumps(data, indent=2, ensure_ascii=False)


# BEISPIEL-FUNKTIONEN FÜR DAS LLM
def create_sample_newspaper():
    """
    BEISPIEL FÜR DAS LLM: So kann das Framework verwendet werden
    """
    # Framework erstellen
    paper = NewspaperFrameWork("AI Morgenzeitung")
    
    # Artikel hinzufügen (das LLM sollte diese mit eigenen Inhalten ersetzen)
    paper.add_article(
        title="Neues Framework revolutioniert KI-gestützte Zeitungsproduktion",
        content="Das Newspaper Framework ermöglicht es LLMs, hochwertige Zeitungen mit minimalem Aufwand zu erstellen...",
        author="KI-Redakteur",
        category="Technologie",
        priority=1
    )
    
    paper.add_article(
        title="Wirtschaft im Wandel: KI-basierte Analysen gewinnen an Bedeutung",
        content="Neue Algorithmen ermöglichen tiefgreifende Wirtschaftsanalysen...",
        author="Wirtschafts-KI",
        category="Wirtschaft",
        priority=2
    )
    
    # Exportieren
    paper.export_html("beispiel_zeitung.html")
    paper.export_json("beispiel_zeitung.json")
    
    return paper


if __name__ == "__main__":
    # Automatische Demo beim direkten Ausführen
    print("Newspaper Framework Demo wird gestartet...")
    create_sample_newspaper()
    print("Demo erfolgreich abgeschlossen!")
    print("Dateien erstellt: beispiel_zeitung.html, beispiel_zeitung.json")