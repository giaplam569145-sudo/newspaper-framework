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
    """Custom exception for framework-specific warnings.

    This exception is raised for non-critical errors that should be
    communicated to the LLM in a user-friendly manner.
    """
    pass


@dataclass
class Article:
    """Represents a single article in the newspaper.

    Attributes:
        title (str): The title of the article.
        content (str): The main body content of the article.
        author (str): The author of the article. Defaults to "Unbekannt".
        category (str): The category of the article. Defaults to "Allgemein".
        priority (int): The priority of the article (1-5), where 1 is the highest.
        image_path (Optional[str]): The local path to an optional image.
        image_caption (Optional[str]): The caption for the image.
    """
    title: str
    content: str
    author: str = "Unbekannt"
    category: str = "Allgemein"
    priority: int = 1  # 1-5, 1 = höchste Priorität
    image_path: Optional[str] = None
    image_caption: Optional[str] = None
    
    def __post_init__(self):
        """Performs validation and sanitization after initialization."""
        self.title = self.title.strip()
        
        if not self.content or len(self.content.strip()) < 10:
            raise NewspaperFrameworkWarning(
                f"Article content is too short (min. 10 characters). Title: '{self.title}'"
            )
        
        self.priority = max(1, min(5, self.priority))
        
        if self.image_path and not os.path.exists(self.image_path):
            print(f"Warning: Image not found: {self.image_path}")
            self.image_path = None


@dataclass
class LayoutConfig:
    """Configures the visual layout and design of the newspaper.

    Attributes:
        font_family (str): The primary font family for the newspaper.
        primary_color (str): The main color used for headers and accents.
        secondary_color (str): The secondary color for links and sub-elements.
        max_width (int): The maximum width of the newspaper content in pixels.
        columns (int): The number of columns for the main content.
        spacing (int): The spacing between elements in pixels.
    """
    font_family: str = "Arial"
    primary_color: str = "#2c3e50"
    secondary_color: str = "#3498db"
    max_width: int = 800
    columns: int = 2
    spacing: int = 20


@dataclass
class MediaConfig:
    """Configures media settings, including logos and images.

    Attributes:
        logo_path (Optional[str]): The path to the newspaper's logo file.
        logo_width (int): The maximum width of the logo in pixels.
        logo_height (int): The maximum height of the logo in pixels.
        image_quality (int): The quality setting for images (1-100).
        supported_formats (List[str]): A list of supported image file formats.
    """
    logo_path: Optional[str] = None
    logo_width: int = 200
    logo_height: int = 60
    image_quality: int = 85
    supported_formats: List[str] = None
    
    def __post_init__(self):
        """Initializes default supported formats if not provided."""
        if self.supported_formats is None:
            self.supported_formats = ["png", "jpg", "jpeg", "gif", "svg"]


@dataclass
class Question:
    """Represents a single question in a quiz.

    Attributes:
        question (str): The text of the question.
        options (List[str]): A list of possible answers.
        correct_index (int): The index of the correct answer in the options list.
        category (str): The category of the question. Defaults to "Allgemein".
    """
    question: str
    options: List[str]
    correct_index: int
    category: str = "Allgemein"
    
    def __post_init__(self):
        """Validates the question's integrity after initialization."""
        if not self.question or len(self.question.strip()) < 5:
            raise NewspaperFrameworkWarning("Question is too short (min. 5 characters).")
        
        if len(self.options) < 2:
            raise NewspaperFrameworkWarning("At least 2 answer options are required.")
        
        if not (0 <= self.correct_index < len(self.options)):
            raise NewspaperFrameworkWarning("Correct answer index is out of bounds.")


class SudokuGenerator:
    """Generates and formats Sudoku puzzles.

    Attributes:
        difficulty (str): The difficulty of the puzzle ('easy', 'medium', 'hard').
        grid (List[List[int]]): The 9x9 Sudoku grid.
    """
    
    def __init__(self, difficulty: str = "medium"):
        """Initializes the SudokuGenerator with a specified difficulty.

        Args:
            difficulty (str): The difficulty of the puzzle. Can be 'easy',
                'medium', or 'hard'. Defaults to 'medium'.
        """
        self.difficulty = difficulty
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
    
    def generate(self) -> List[List[int]]:
        """Generates a new Sudoku grid based on the specified difficulty.

        This method uses a shuffling algorithm to create a valid, complete
        Sudoku grid and then removes a number of cells based on the
        difficulty level to create the puzzle.

        Returns:
            List[List[int]]: The generated 9x9 Sudoku grid with some cells
                set to 0 to represent empty spaces.
        """
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
        
        self.grid = [[nums[pattern(r, c)] for c in cols] for r in rows]
        
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
        """Formats the Sudoku grid as an HTML table.

        Returns:
            str: An HTML string representing the Sudoku puzzle.
        """
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
    """Manages a collection of questions to create a quiz.

    Attributes:
        title (str): The title of the quiz.
        questions (List[Question]): A list of Question objects.
    """
    
    def __init__(self, title: str = "Tagesquiz"):
        """Initializes the QuizSystem with a title.

        Args:
            title (str): The title of the quiz. Defaults to "Tagesquiz".
        """
        self.title = title
        self.questions: List[Question] = []
    
    def add_question(self, question: str, options: List[str], correct_index: int, category: str = "Allgemein") -> Question:
        """Adds a new question to the quiz.

        Args:
            question (str): The text of the question.
            options (List[str]): A list of possible answers.
            correct_index (int): The index of the correct answer.
            category (str): The category of the question.

        Returns:
            Question: The newly created and added Question object.
        """
        q = Question(question=question, options=options, correct_index=correct_index, category=category)
        self.questions.append(q)
        return q
    
    def generate_quiz(self) -> Dict:
        """Generates a dictionary representation of the quiz.

        Returns:
            Dict: A dictionary containing the quiz title, a list of questions,
                and the total number of questions.
        """
        return {
            "title": self.title,
            "questions": [asdict(q) for q in self.questions],
            "total_questions": len(self.questions)
        }
    
    def to_html(self) -> str:
        """Formats the quiz as an HTML block.

        Returns:
            str: An HTML string representing the quiz.
        """
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
    """The main class for creating and managing a newspaper.

    This class provides a high-level API for LLMs to construct a newspaper
    by adding articles, quizzes, Sudoku puzzles, and other media. It handles
    validation, layout, and exporting to various formats.

    Attributes:
        title (str): The title of the newspaper.
        layout (LayoutConfig): The layout configuration object.
        media (MediaConfig): The media configuration object.
        articles (List[Article]): A list of articles in the newspaper.
        quizzes (List[QuizSystem]): A list of quizzes.
        sudokus (List[SudokuGenerator]): A list of Sudoku puzzles.
        date (str): The publication date of the newspaper.
        logo_content (Optional[str]): The HTML content for the logo.
    """
    
    def __init__(self, title: str = "Morgenzeitung", layout: Optional[LayoutConfig] = None, media: Optional[MediaConfig] = None):
        """Initializes the NewspaperFrameWork.

        Args:
            title (str): The title of the newspaper.
            layout (Optional[LayoutConfig]): A custom layout configuration.
                If None, a default layout is used.
            media (Optional[MediaConfig]): A custom media configuration.
                If None, a default configuration is used.
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
            raise NewspaperFrameworkWarning("Newspaper title cannot be empty.")
    
    def set_logo(self, logo_path: str) -> bool:
        """Sets the logo for the newspaper.

        Args:
            logo_path (str): The file path to the logo image.

        Returns:
            bool: True if the logo was set successfully, False otherwise.
        """
        if not os.path.exists(logo_path):
            print(f"Warning: Logo file not found: {logo_path}")
            return False
        
        self.media.logo_path = logo_path
        self.logo_content = self._generate_logo_html()
        print(f"Logo set: {logo_path}")
        return True
    
    def _generate_logo_html(self) -> str:
        """Generates the HTML for the logo.

        Returns:
            str: The HTML `<img>` tag for the logo, or an empty string
                if no logo is set.
        """
        if not self.media.logo_path:
            return ""
        
        return f'<img src="{self.media.logo_path}" alt="Logo" style="max-width: {self.media.logo_width}px; max-height: {self.media.logo_height}px;">'
    
    def add_article(self, title: str, content: str, **kwargs) -> Article:
        """Adds an article to the newspaper.

        This method will attempt to automatically correct invalid article
        content by appending a note to it.

        Args:
            title (str): The title of the article.
            content (str): The main content of the article.
            **kwargs: Additional keyword arguments for the Article, such as
                `author`, `category`, `priority`, `image_path`, and
                `image_caption`.

        Returns:
            Article: The created and added Article object.
        """
        try:
            article = Article(title=title, content=content, **kwargs)
            self.articles.append(article)
            print(f"Article '{title[:30]}...' added successfully.")
            return article
        except NewspaperFrameworkWarning as e:
            print(f"Warning: {e}")
            corrected_content = content + " (Content automatically completed)"
            article = Article(title=title, content=corrected_content, **kwargs)
            self.articles.append(article)
            print(f"Article added with automatic correction.")
            return article
    
    def add_quiz(self, quiz: QuizSystem) -> QuizSystem:
        """Adds a quiz to the newspaper.

        Args:
            quiz (QuizSystem): The QuizSystem object to add.

        Returns:
            QuizSystem: The added QuizSystem object.
        """
        self.quizzes.append(quiz)
        print(f"Quiz '{quiz.title}' added.")
        return quiz
    
    def add_sudoku(self, difficulty: str = "medium") -> SudokuGenerator:
        """Adds a Sudoku puzzle to the newspaper.

        Args:
            difficulty (str): The difficulty of the Sudoku puzzle. Can be
                'easy', 'medium', or 'hard'.

        Returns:
            SudokuGenerator: The newly created and added SudokuGenerator object.
        """
        sudoku = SudokuGenerator(difficulty)
        sudoku.generate()
        self.sudokus.append(sudoku)
        print(f"Sudoku ({difficulty}) added.")
        return sudoku
    
    def generate(self) -> Dict:
        """Generates a structured dictionary of the entire newspaper.

        This method validates the newspaper content, sorts articles by
        priority, and compiles all data into a single dictionary.

        Returns:
            Dict: A dictionary containing all newspaper data.

        Raises:
            NewspaperFrameworkWarning: If no content has been added to the
                newspaper.
        """
        print("Generating newspaper...")
        
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
        print(f"Newspaper generated successfully: {total_content} content elements.")
        return newspaper_data
    
    def export_html(self, filename: str = "zeitung.html") -> str:
        """Exports the newspaper as an HTML file.

        Args:
            filename (str): The name of the output HTML file.

        Returns:
            str: The generated HTML content as a string.
        """
        data = self.generate()
        
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
        
        print(f"HTML exported: {filename}")
        return html_content
    
    def export_json(self, filename: str = "zeitung.json") -> str:
        """Exports the newspaper as a JSON file.

        Args:
            filename (str): The name of the output JSON file.

        Returns:
            str: The generated JSON content as a string.
        """
        data = self.generate()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"JSON exported: {filename}")
        return json.dumps(data, indent=2, ensure_ascii=False)


def create_sample_newspaper():
    """Creates a sample newspaper to demonstrate the framework's usage.

    This function serves as a simple, LLM-friendly example of how to use
    the NewspaperFrameWork to create a newspaper with articles, a quiz,
    and a Sudoku puzzle.

    Returns:
        NewspaperFrameWork: The generated NewspaperFrameWork object.
    """
    paper = NewspaperFrameWork("AI Morning News")
    
    paper.add_article(
        title="New Framework Revolutionizes AI-Powered Newspaper Production",
        content="The Newspaper Framework allows LLMs to create high-quality newspapers with minimal effort. With integrated features for images, quizzes, and Sudoku, newspaper creation becomes a breeze.",
        author="AI Editor",
        category="Technology",
        priority=1
    )
    
    paper.add_article(
        title="Economy in Transition: AI-Based Analyses Gain Importance",
        content="New algorithms enable in-depth economic analyses in real-time. Companies are increasingly using AI systems for strategic decisions.",
        author="Economics AI",
        category="Business",
        priority=2
    )
    
    quiz = QuizSystem("Technology Quiz")
    quiz.add_question(
        "What is AI?",
        ["Artificial Intelligence", "Kitchen International", "Merchant Institute", "No Idea"],
        0,
        "Technology"
    )
    paper.add_quiz(quiz)
    
    paper.add_sudoku("medium")
    
    paper.export_html("sample_newspaper.html")
    paper.export_json("sample_newspaper.json")
    
    return paper


if __name__ == "__main__":
    print("Starting Newspaper Framework Demo...")
    create_sample_newspaper()
    print("Demo successfully completed!")
    print("Files created: sample_newspaper.html, sample_newspaper.json")