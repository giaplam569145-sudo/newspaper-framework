"""Data models for the Newspaper Framework."""

import os
import warnings
from dataclasses import dataclass
from typing import List, Optional
from .exceptions import NewspaperFrameworkError, NewspaperFrameworkWarning


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
    priority: int = 1  # 1-5, 1 = highest priority
    image_path: Optional[str] = None
    image_caption: Optional[str] = None

    def __post_init__(self):
        """Performs validation and sanitization after initialization."""
        self.title = self.title.strip()

        if not self.content or len(self.content.strip()) < 10:
            raise NewspaperFrameworkError(
                f"Article content is too short (min. 10 characters). Title: '{self.title}'"
            )

        self.priority = max(1, min(5, self.priority))

        if self.image_path and not os.path.exists(self.image_path):
            warnings.warn(f"Image not found: {self.image_path}", NewspaperFrameworkWarning)
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
    supported_formats: Optional[List[str]] = None

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
            raise NewspaperFrameworkError("Question is too short (min. 5 characters).")

        if len(self.options) < 2:
            raise NewspaperFrameworkError("At least 2 answer options are required.")

        if not (0 <= self.correct_index < len(self.options)):
            raise NewspaperFrameworkError("Correct answer index is out of bounds.")
