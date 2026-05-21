import json
import os
import pytest
from src.newspaper.core import Newspaper
from src.newspaper.content.quiz import QuizSystem
from src.newspaper.exceptions import NewspaperFrameworkError


class TestNewspaperInit:
    def test_default_title(self):
        n = Newspaper()
        assert n.title == "Morgenzeitung"

    def test_custom_title(self):
        n = Newspaper("My Paper")
        assert n.title == "My Paper"

    def test_empty_title_raises(self):
        with pytest.raises(NewspaperFrameworkError):
            Newspaper("")

    def test_whitespace_title_raises(self):
        with pytest.raises(NewspaperFrameworkError):
            Newspaper("   ")

    def test_title_trimmed(self):
        n = Newspaper("  My Paper  ")
        assert n.title == "My Paper"


class TestNewspaperAddArticle:
    def test_add_valid_article(self):
        n = Newspaper("Test")
        a = n.add_article(title="News", content="Some article content here...")
        assert len(n.articles) == 1
        assert a.title == "News"

    def test_short_content_auto_corrected(self):
        n = Newspaper("Test")
        a = n.add_article(title="Short", content="hi")
        assert len(n.articles) == 1
        assert "automatically completed" in a.content or "vervollst" in a.content


class TestNewspaperGenerate:
    def test_empty_newspaper_raises(self):
        n = Newspaper("Empty")
        with pytest.raises(NewspaperFrameworkError):
            n.generate()

    def test_articles_sorted_by_priority(self):
        n = Newspaper("Test")
        n.add_article(title="Low", content="Low priority content...", priority=5)
        n.add_article(title="High", content="High priority content...", priority=1)
        n.add_article(title="Med", content="Med priority content...", priority=3)
        data = n.generate()
        assert data["articles"][0]["title"] == "High"
        assert data["articles"][1]["title"] == "Med"
        assert data["articles"][2]["title"] == "Low"

    def test_generate_does_not_mutate_articles(self):
        n = Newspaper("Test")
        n.add_article(title="P5", content="Content here...", priority=5)
        n.add_article(title="P1", content="Content here...", priority=1)
        n.generate()
        assert n.articles[0].title == "P5"
        assert n.articles[1].title == "P1"

    def test_statistics(self):
        n = Newspaper("Test")
        n.add_article(title="A1", content="Content...", author="X", category="Tech")
        n.add_article(title="A2", content="Content...", author="Y", category="Biz")
        data = n.generate()
        assert data["statistics"]["total_articles"] == 2
        assert "Tech" in data["statistics"]["categories"]
        assert "X" in data["statistics"]["authors"]


class TestNewspaperExport:
    def test_export_json(self, tmp_path):
        n = Newspaper("Test")
        n.add_article(title="News", content="Article content here...")
        out = str(tmp_path / "test.json")
        result = n.export_json(out)
        assert os.path.exists(out)
        data = json.loads(result)
        assert data["title"] == "Test"
        assert len(data["articles"]) == 1

    def test_export_html(self, tmp_path):
        n = Newspaper("Test")
        n.add_article(title="News", content="Article content here...")
        out = str(tmp_path / "test.html")
        result = n.export_html(out)
        assert os.path.exists(out)
        assert "<html" in result
        assert "Test" in result

    def test_export_with_quiz_and_sudoku(self, tmp_path):
        n = Newspaper("Full")
        n.add_article(title="Art", content="Content here...")
        quiz = QuizSystem("Q")
        quiz.add_question("Question text here?", ["A", "B"], 0)
        n.add_quiz(quiz)
        n.add_sudoku("easy")

        html_out = str(tmp_path / "full.html")
        json_out = str(tmp_path / "full.json")

        n.export_html(html_out)
        n.export_json(json_out)

        assert os.path.exists(html_out)
        data = json.loads(n.export_json(str(tmp_path / "full2.json")))
        assert data["statistics"]["total_quizzes"] == 1
        assert data["statistics"]["total_sudokus"] == 1
