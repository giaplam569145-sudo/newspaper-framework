"""Core Newspaper class."""

import datetime
import logging
import os
from dataclasses import asdict
from typing import List, Optional, Dict

from .models import Article, LayoutConfig, MediaConfig
from .exceptions import NewspaperFrameworkError
from .content.quiz import QuizSystem
from .content.sudoku import SudokuGenerator
from .content.crossword import Crossword, CrosswordGenerator
from .export.html_exporter import HtmlExporter
from .export.json_exporter import JsonExporter

logger = logging.getLogger(__name__)


class Newspaper:
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
        crosswords (List[Crossword]): A list of crossword puzzles.
        date (str): The publication date of the newspaper.
    """

    def __init__(self, title: str = "Morgenzeitung", layout: Optional[LayoutConfig] = None, media: Optional[MediaConfig] = None):
        """Initializes the Newspaper.

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
        self.crosswords: List[Crossword] = []
        self.date = datetime.datetime.now().strftime("%d.%m.%Y")

        # Validation
        if not self.title:
            raise NewspaperFrameworkError("Newspaper title cannot be empty.")

    def set_logo(self, logo_path: str) -> bool:
        """Sets the logo for the newspaper.

        Args:
            logo_path (str): The file path to the logo image.

        Returns:
            bool: True if the logo was set successfully, False otherwise.
        """
        if not os.path.exists(logo_path):
            logger.warning("Logo file not found: %s", logo_path)
            return False

        self.media.logo_path = logo_path
        logger.info("Logo set: %s", logo_path)
        return True

    def add_article(self, title: str, content: str, force: bool = False, **kwargs) -> Article:
        """Adds an article to the newspaper.

        Args:
            title (str): The title of the article.
            content (str): The main content of the article.
            force (bool): If True, auto-correct short content instead of raising.
            **kwargs: Additional keyword arguments for the Article.

        Returns:
            Article: The created and added Article object.

        Raises:
            NewspaperFrameworkError: If validation fails and force=False.
        """
        try:
            article = Article(title=title, content=content, **kwargs)
            self.articles.append(article)
            return article
        except NewspaperFrameworkError as e:
            if not force:
                raise
            corrected_content = content + " (Content automatically completed)"
            article = Article(title=title, content=corrected_content, **kwargs)
            self.articles.append(article)
            return article

    def add_quiz(self, quiz: QuizSystem) -> QuizSystem:
        """Adds a quiz to the newspaper."""
        self.quizzes.append(quiz)
        logger.info("Quiz '%s' added.", quiz.title)
        return quiz

    def add_sudoku(self, difficulty: str = "medium") -> SudokuGenerator:
        """Adds a Sudoku puzzle to the newspaper."""
        sudoku = SudokuGenerator(difficulty)
        sudoku.generate()
        self.sudokus.append(sudoku)
        logger.info("Sudoku (%s) added.", difficulty)
        return sudoku

    def add_crossword(self, crossword: Crossword) -> Crossword:
        """Adds a crossword puzzle to the newspaper."""
        self.crosswords.append(crossword)
        logger.info("Crossword added.")
        return crossword

    def generate(self) -> Dict:
        """Generates a structured dictionary of the entire newspaper."""
        if not any([self.articles, self.quizzes, self.sudokus, self.crosswords]):
            raise NewspaperFrameworkError(
                "No content available. Please add articles, quizzes or sudoku."
            )

        sorted_articles = sorted(self.articles, key=lambda x: x.priority)

        newspaper_data = {
            "title": self.title,
            "date": self.date,
            "layout": asdict(self.layout),
            "media": asdict(self.media),
            "articles": [asdict(article) for article in sorted_articles],
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "sudokus": [s.to_dict() for s in self.sudokus],
            "crosswords": [asdict(cw) for cw in self.crosswords],
            "statistics": {
                "total_articles": len(self.articles),
                "total_quizzes": len(self.quizzes),
                "total_sudokus": len(self.sudokus),
                "total_crosswords": len(self.crosswords),
                "categories": list(set(a.category for a in self.articles)),
                "authors": list(set(a.author for a in self.articles))
            }
        }

        return newspaper_data

    def export_html(self, filename: str = "zeitung.html") -> str:
        """Exports the newspaper as an HTML file."""
        exporter = HtmlExporter()
        return exporter.export(self.generate(), filename)

    def export_json(self, filename: str = "zeitung.json") -> str:
        """Exports the newspaper as a JSON file."""
        exporter = JsonExporter()
        return exporter.export(self.generate(), filename)
