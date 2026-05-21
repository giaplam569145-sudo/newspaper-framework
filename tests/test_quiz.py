import pytest
from src.newspaper.content.quiz import QuizSystem
from src.newspaper.exceptions import NewspaperFrameworkError


class TestQuizSystem:
    def test_add_question(self):
        qs = QuizSystem("Test Quiz")
        q = qs.add_question("What is 2+2?", ["3", "4", "5"], 1)
        assert q.question == "What is 2+2?"
        assert len(qs.questions) == 1

    def test_to_dict(self):
        qs = QuizSystem("Test Quiz")
        qs.add_question("Valid question here?", ["A", "B"], 0)
        d = qs.to_dict()
        assert d["title"] == "Test Quiz"
        assert d["total_questions"] == 1
        assert len(d["questions"]) == 1

    def test_generate_calls_to_dict(self):
        qs = QuizSystem("Q")
        qs.add_question("Valid question here?", ["A", "B"], 0)
        result = qs.generate()
        assert "title" in result

    def test_multiple_questions(self):
        qs = QuizSystem("Multi")
        qs.add_question("Q1 here?", ["A", "B"], 0)
        qs.add_question("Q2 here?", ["C", "D"], 1)
        assert len(qs.questions) == 2
