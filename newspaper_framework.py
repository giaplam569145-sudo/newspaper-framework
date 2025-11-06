# Newspaper Framework für LLMs - Version 2.0
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
import random
import os
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod


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
    image_path: Optional[str] = None
    image_caption: Optional[str] = None
    
    def __post_init__(self):
        """Automatische Validierung und Korrektur"""
        # Titel automatisch trimmen
        self.title = self.title.strip()
        
        # Content validieren
        if not self.content or len(self.content.strip()) < 10:
            raise NewspaperFrameworkWarning(
                f"Artikelinhalt zu kurz (min. 10 Zeichen). Titel: '{self.title}'"
            )
        
        # Priority bounds check
        self.priority = max(1, min(5, self.priority))
        
        # Bildpfad validieren falls vorhanden
        if self.image_path and not os.path.exists(self.image_path):
            print(f"Warnung: Bild nicht gefunden: {self.image_path}")
            self.image_path = None


@dataclass
class LayoutConfig:
    """Layout-Konfiguration für konsistentes Design"""
    font_family: str = "Arial"
    primary_color: str = "#2c3e50"
    secondary_color: str = "#3498db"
    max_width: int = 800
    columns: int = 2
    spacing: int = 20


@dataclass
class MediaConfig:
    """Medien-Konfiguration für Bilder und Logo"""
    logo_path: Optional[str] = None
    logo_width: int = 200
    logo_height: int = 60
    image_quality: int = 85
    supported_formats: List[str] = None
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ["png", "jpg", "jpeg", "gif", "svg"]


@dataclass
class Question:
    """Frage für Quiz-System"""
    question: str
    options: List[str]
    correct_index: int
    category: str = "Allgemein"
    
    def __post_init__(self):
        """Validierung der Frage"""
        if not self.question or len(self.question.strip()) < 5:
            raise NewspaperFrameworkWarning("Frage zu kurz (min. 5 Zeichen)")
        
        if len(self.options) < 2:
            raise NewspaperFrameworkWarning("Mindestens 2 Antwortoptionen erforderlich")
        
        if not (0 <= self.correct_index < len(self.options)):
            raise NewspaperFrameworkWarning("Korrekte Antwort außerhalb des gültigen Bereichs")


class SudokuGenerator:
    """Sudoku-Generator für Zeitungs-Rätsel"""
    
    def __init__(self, difficulty: str = "medium"):
        """
        Sudoku-Generator initialisieren
        
        Args:
            difficulty: "easy", "medium", "hard"
        """
        self.difficulty = difficulty
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
    
    def generate(self) -> List[List[int]]:
        """Sudoku generieren"""
        # Einfache Sudoku-Implementierung
        base = 3
        side = base * base
        
        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side
        
        def shuffle(s):
            return random.sample(s, len(s))
        
        r_base = range(base)
        rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
        cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
        nums = shuffle(range(1, base * base + 1))
        
        # Vollständiges Sudoku erzeugen
        self.grid = [[nums[pattern(r, c)] for c in cols] for r in rows]
        
        # Zufällige Zellen entfernen basierend auf Schwierigkeit
        cells_to_remove = {
            "easy": 30,
            "medium": 40,
            "hard": 50
        }.get(self.difficulty, 40)
        
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        
        for i in range(cells_to_remove):
            r, c = cells[i]
            self.grid[r][c] = 0
        
        return self.grid
    
    def to_html(self) -> str:
        """Sudoku als HTML-Tabelle formatieren"""
        html = '<table class="sudoku" style="border-collapse: collapse; margin: 20px auto;">'
        
        for i, row in enumerate(self.grid):
            html += '<tr>'
            for j, cell in enumerate(row):
                border_style = ""
                if i % 3 == 0 and i != 0:
                    border_style += "border-top: 2px solid black;"
                if j % 3 == 0 and j != 0:
                    border_style += "border-left: 2px solid black;"
                
                if cell == 0:
                    html += f'<td style="width: 30px; height: 30px; border: 1px solid #ccc; text-align: center; {border_style}"><input type="text" maxlength="1" style="width: 100%; border: none; text-align: center;"></td>'
                else:
                    html += f'<td style="width: 30px; height: 30px; border: 1px solid #ccc; text-align: center; font-weight: bold; {border_style}">{cell}</td>'
            html += '</tr>'
        
        html += '</table>'
        return html


class QuizSystem:
    """Quiz-System für interaktive Zeitungsinhalte"""
    
    def __init__(self, title: str = "Tagesquiz"):
        """
        Quiz-System initialisieren
        
        Args:
            title: Titel des Quiz
        """
        self.title = title
        self.questions: List[Question] = []
    
    def add_question(self, question: str, options: List[str], correct_index: int, category: str = "Allgemein") -> Question:
        """
        Frage zum Quiz hinzufügen
        
        Args:
            question: Die Frage
            options: Liste der Antwortoptionen
            correct_index: Index der korrekten Antwort
            category: Kategorie der Frage
            
        Returns:
            Question: Erstellte Frage
        """
        q = Question(question=question, options=options, correct_index=correct_index, category=category)
        self.questions.append(q)
        return q
    
    def generate_quiz(self) -> Dict:
        """
        Quiz als Dictionary generieren
        
        Returns:
            Dict: Strukturierte Quiz-Daten
        """
        return {
            "title": self.title,
            "questions": [asdict(q) for q in self.questions],
            "total_questions": len(self.questions)
        }
    
    def to_html(self) -> str:
        """Quiz als HTML formatieren"""
        html = f'<div class="quiz" style="margin: 20px 0;"><h3>{self.title}</h3>'
        
        for i, q in enumerate(self.questions, 1):
            html += f'<div class="question" style="margin: 15px 0;">'
            html += f'<p><strong>Frage {i}:</strong> {q.question}</p>'
            html += '<div class="options">'
            
            for j, option in enumerate(q.options):
                html += f'<label style="display: block; margin: 5px 0;">'
                html += f'<input type="radio" name="q{i}" value="{j}"> {option}'
                html += '</label>'
            
            html += '</div></div>'
        
        html += '</div>'
        return html


class NewspaperFrameWork:
    """
    HAUPT-FRAMEWORK-KLASSE FÜR LLMs
    
    VERWENDUNG FÜR DAS LLM:
    1. Framework erstellen: paper = NewspaperFrameWork()
    2. Artikel hinzufügen: paper.add_article(...)
    3. Medien hinzufügen: paper.set_logo(...)
    4. Quiz/Sudoku hinzufügen: paper.add_quiz(...), paper.add_sudoku(...)
    5. Exportieren: paper.export_html() oder paper.export_json()
    """
    
    def __init__(self, title: str = "Morgenzeitung", layout: Optional[LayoutConfig] = None, media: Optional[MediaConfig] = None):
        """
        Framework initialisieren
        
        Args:
            title: Titel der Zeitung
            layout: Layout-Konfiguration
            media: Medien-Konfiguration
        """
        self.title = title.strip()
        self.layout = layout or LayoutConfig()
        self.media = media or MediaConfig()
        self.articles: List[Article] = []
        self.quizzes: List[QuizSystem] = []
        self.sudokus: List[SudokuGenerator] = []
        self.date = datetime.datetime.now().strftime("%d.%m.%Y")
        self.logo_content: Optional[str] = None
        
        # Validierung
        if not self.title:
            raise NewspaperFrameworkWarning("Zeitungstitel darf nicht leer sein")
    
    def set_logo(self, logo_path: str) -> bool:
        """
        Logo für die Zeitung setzen
        
        Args:
            logo_path: Pfad zur Logo-Datei
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if not os.path.exists(logo_path):
            print(f"Warnung: Logo-Datei nicht gefunden: {logo_path}")
            return False
        
        self.media.logo_path = logo_path
        self.logo_content = self._generate_logo_html()
        print(f"Logo gesetzt: {logo_path}")
        return True
    
    def _generate_logo_html(self) -> str:
        """HTML für Logo generieren"""
        if not self.media.logo_path:
            return ""
        
        return f'<img src="{self.media.logo_path}" alt="Logo" style="max-width: {self.media.logo_width}px; max-height: {self.media.logo_height}px;">'
    
    def add_article(self, title: str, content: str, **kwargs) -> Article:
        """
        Artikel zur Zeitung hinzufügen
        
        Args:
            title: Artikel-Titel
            content: Artikel-Inhalt
            **kwargs: Zusätzliche Parameter (author, category, priority, image_path, image_caption)
            
        Returns:
            Article: Erstellter Artikel
        """
        try:
            article = Article(title=title, content=content, **kwargs)
            self.articles.append(article)
            print(f"Artikel '{title[:30]}...' erfolgreich hinzugefügt")
            return article
        except NewspaperFrameworkWarning as e:
            print(f"Warnung: {e}")
            # Versuche automatische Korrektur
            corrected_content = content + " (Inhalt automatisch vervollständigt)"
            article = Article(title=title, content=corrected_content, **kwargs)
            self.articles.append(article)
            print(f"Artikel mit automatischer Korrektur hinzugefügt")
            return article
    
    def add_quiz(self, quiz: QuizSystem) -> QuizSystem:
        """
        Quiz zur Zeitung hinzufügen
        
        Args:
            quiz: QuizSystem-Instanz
            
        Returns:
            QuizSystem: Hinzugefügtes Quiz
        """
        self.quizzes.append(quiz)
        print(f"Quiz '{quiz.title}' hinzugefügt")
        return quiz
    
    def add_sudoku(self, difficulty: str = "medium") -> SudokuGenerator:
        """
        Sudoku zur Zeitung hinzufügen
        
        Args:
            difficulty: Schwierigkeitsgrad ("easy", "medium", "hard")
            
        Returns:
            SudokuGenerator: Erstellter Sudoku-Generator
        """
        sudoku = SudokuGenerator(difficulty)
        sudoku.generate()
        self.sudokus.append(sudoku)
        print(f"Sudoku ({difficulty}) hinzugefügt")
        return sudoku
    
    def generate(self) -> Dict:
        """
        Zeitung als strukturiertes Dictionary generieren
        
        Returns:
            Dict: Strukturierte Zeitungsdaten
        """
        print("Generiere Zeitung...")
        
        # Validierung der Gesamtzeitung
        if len(self.articles) == 0 and len(self.quizzes) == 0 and len(self.sudokus) == 0:
            raise NewspaperFrameworkWarning(
                "Keine Inhalte vorhanden. Bitte Artikel, Quiz oder Sudoku hinzufügen."
            )
        
        # Artikel nach Priorität sortieren
        self.articles.sort(key=lambda x: x.priority)
        
        # Strukturierte Ausgabe erstellen
        newspaper_data = {
            "title": self.title,
            "date": self.date,
            "layout": asdict(self.layout),
            "media": asdict(self.media),
            "articles": [asdict(article) for article in self.articles],
            "quizzes": [quiz.generate_quiz() for quiz in self.quizzes],
            "sudokus": [{"difficulty": s.difficulty, "grid": s.grid} for s in self.sudokus],
            "statistics": {
                "total_articles": len(self.articles),
                "total_quizzes": len(self.quizzes),
                "total_sudokus": len(self.sudokus),
                "categories": list(set(a.category for a in self.articles)),
                "authors": list(set(a.author for a in self.articles))
            }
        }
        
        total_content = len(self.articles) + len(self.quizzes) + len(self.sudokus)
        print(f"Zeitung erfolgreich generiert: {total_content} Inhaltselemente")
        return newspaper_data
    
    def export_html(self, filename: str = "zeitung.html") -> str:
        """
        Zeitung als HTML exportieren
        
        Args:
            filename: Dateiname für HTML-Export
            
        Returns:
            str: HTML-Inhalt
        """
        data = self.generate()
        
        # Design-Themes definieren
        themes = {
            "classic": {
                "primary": "#2c3e50",
                "secondary": "#3498db",
                "background": "#ffffff"
            },
            "modern": {
                "primary": "#1a1a1a",
                "secondary": "#e74c3c",
                "background": "#f8f9fa"
            },
            "minimal": {
                "primary": "#333333",
                "secondary": "#95a5a6",
                "background": "#ffffff"
            },
            "premium": {
                "primary": "#8e44ad",
                "secondary": "#f39c12",
                "background": "#fef9e7"
            }
        }
        
        theme = themes.get("classic", themes["classic"])
        
        # HTML-Header generieren
        html_content = f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{data['title']}</title>
            <style>
                body {{
                    font-family: {data['layout']['font_family']};
                    max-width: {data['layout']['max_width']}px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: {theme['background']};
                    line-height: 1.6;
                }}
                .header {{
                    text-align: center;
                    color: {theme['primary']};
                    border-bottom: 3px solid {theme['secondary']};
                    margin-bottom: 30px;
                    padding-bottom: 20px;
                }}
                .logo {{
                    margin-bottom: 15px;
                }}
                .article {{
                    margin-bottom: {data['layout']['spacing']}px;
                    padding: 20px;
                    border-left: 4px solid {theme['secondary']};
                    background-color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .article-title {{
                    color: {theme['primary']};
                    margin-top: 0;
                    font-size: 1.5em;
                }}
                .meta {{
                    color: #666;
                    font-size: 0.9em;
                    margin-bottom: 10px;
                }}
                .article-image {{
                    max-width: 100%;
                    height: auto;
                    margin: 10px 0;
                }}
                .quiz {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 5px;
                }}
                .sudoku {{
                    text-align: center;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    color: #666;
                }}
                @media (max-width: 768px) {{
                    body {{ padding: 10px; }}
                    .article {{ padding: 15px; }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                {self.logo_content or ''}
                <h1>{data['title']}</h1>
                <p class="date">{data['date']}</p>
            </div>
        """
        
        # Artikel hinzufügen
        for article in data['articles']:
            html_content += f"""
            <div class="article">
                <h2 class="article-title">{article['title']}</h2>
                <div class="meta">Von {article['author']} | {article['category']}</div>
                {f'<img src="{article["image_path"]}" alt="{article["image_caption"]}" class="article-image">' if article.get('image_path') else ''}
                <p>{article['content']}</p>
                {f'<p><em>{article["image_caption"]}</em></p>' if article.get('image_caption') else ''}
            </div>
            """
        
        # Quiz hinzufügen
        for quiz in self.quizzes:
            html_content += f'<div class="quiz">{quiz.to_html()}</div>'
        
        # Sudoku hinzufügen
        for sudoku in self.sudokus:
            html_content += f'<div class="sudoku"><h3>Sudoku ({sudoku.difficulty})</h3>{sudoku.to_html()}</div>'
        
        # Footer hinzufügen
        html_content += f"""
            <div class="footer">
                <p>Generiert mit Newspaper Framework für LLMs</p>
                <p>Statistik: {data['statistics']['total_articles']} Artikel, {data['statistics']['total_quizzes']} Quiz, {data['statistics']['total_sudokus']} Sudoku</p>
            </div>
        </body>
        </html>
        """
        
        # Datei schreiben
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML exportiert: {filename}")
        return html_content
    
    def export_json(self, filename: str = "zeitung.json") -> str:
        """
        Zeitung als JSON exportieren
        
        Args:
            filename: Dateiname für JSON-Export
            
        Returns:
            str: JSON-String
        """
        data = self.generate()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"JSON exportiert: {filename}")
        return json.dumps(data, indent=2, ensure_ascii=False)


# BEISPIEL-FUNKTIONEN FÜR DAS LLM
def create_sample_newspaper():
    """
    BEISPIEL FÜR DAS LLM: So kann das Framework verwendet werden
    """
    # Framework erstellen
    paper = NewspaperFrameWork("AI Morgenzeitung")
    
    # Artikel hinzufügen
    paper.add_article(
        title="Neues Framework revolutioniert KI-gestützte Zeitungsproduktion",
        content="Das Newspaper Framework ermöglicht es LLMs, hochwertige Zeitungen mit minimalem Aufwand zu erstellen. Mit integrierten Funktionen für Bilder, Quiz und Sudoku wird die Zeitungserstellung zum Kinderspiel.",
        author="KI-Redakteur",
        category="Technologie",
        priority=1
    )
    
    paper.add_article(
        title="Wirtschaft im Wandel: KI-basierte Analysen gewinnen an Bedeutung",
        content="Neue Algorithmen ermöglichen tiefgreifende Wirtschaftsanalysen in Echtzeit. Unternehmen nutzen immer häufiger KI-Systeme für strategische Entscheidungen.",
        author="Wirtschafts-KI",
        category="Wirtschaft",
        priority=2
    )
    
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
    paper.export_html("beispiel_zeitung.html")
    paper.export_json("beispiel_zeitung.json")
    
    return paper


if __name__ == "__main__":
    # Automatische Demo beim direkten Ausführen
    print("Newspaper Framework Demo wird gestartet...")
    create_sample_newspaper()
    print("Demo erfolgreich abgeschlossen!")
    print("Dateien erstellt: beispiel_zeitung.html, beispiel_zeitung.json")