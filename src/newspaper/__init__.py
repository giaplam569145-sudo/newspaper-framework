"""
Newspaper Framework
===================

A framework for AI-driven newspaper production.
"""

from .core import Newspaper
from .models import Article, LayoutConfig, MediaConfig, Question
from .content.quiz import QuizSystem
from .content.sudoku import SudokuGenerator
from .content.crossword import CrosswordGenerator, Crossword
from .exceptions import NewspaperFrameworkError, NewspaperFrameworkWarning

__all__ = [
    "Newspaper",
    "Article",
    "LayoutConfig",
    "MediaConfig",
    "Question",
    "QuizSystem",
    "SudokuGenerator",
    "CrosswordGenerator",
    "Crossword",
    "NewspaperFrameworkError",
    "NewspaperFrameworkWarning",
]
