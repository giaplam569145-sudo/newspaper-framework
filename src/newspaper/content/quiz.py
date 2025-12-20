"""Quiz system implementation."""

from typing import List, Dict
from dataclasses import asdict
from ..models import Question
from ..exceptions import NewspaperFrameworkWarning
from .base import ContentGenerator

class QuizSystem(ContentGenerator):
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

    def generate(self) -> Dict:
        """Generates a dictionary representation of the quiz.

        Returns:
            Dict: A dictionary containing the quiz title, a list of questions,
                and the total number of questions.
        """
        return self.to_dict()

    def to_dict(self) -> Dict:
        """Returns dictionary representation of the quiz for JSON export."""
        return {
            "title": self.title,
            "questions": [asdict(q) for q in self.questions],
            "total_questions": len(self.questions)
        }
