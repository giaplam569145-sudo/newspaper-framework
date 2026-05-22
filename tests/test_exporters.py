import json
import os
import pytest
from src.newspaper.core import Newspaper
from src.newspaper.export.html_exporter import HtmlExporter
from src.newspaper.export.json_exporter import JsonExporter


class TestHtmlExporter:
    def test_export_creates_file(self, tmp_path):
        n = Newspaper("Export Test")
        n.add_article(title="Headline", content="Article body content here...")
        out = str(tmp_path / "out.html")
        exporter = HtmlExporter()
        data = n.generate()
        result = exporter.export(data, out)
        assert os.path.exists(out)

    def test_export_contains_title(self, tmp_path):
        n = Newspaper("My Newspaper")
        n.add_article(title="Breaking", content="Some news content here...")
        out = str(tmp_path / "out.html")
        exporter = HtmlExporter()
        result = exporter.export(n.generate(), out)
        assert "My Newspaper" in result
        assert "Breaking" in result

    def test_export_contains_article_content(self, tmp_path):
        n = Newspaper("Test")
        n.add_article(title="T", content="Unique content XYZ 123")
        out = str(tmp_path / "out.html")
        exporter = HtmlExporter()
        result = exporter.export(n.generate(), out)
        assert "Unique content XYZ 123" in result

    def test_export_contains_quiz(self, tmp_path):
        from src.newspaper.content.quiz import QuizSystem
        n = Newspaper("Test")
        n.add_article(title="T", content="Content padding here...")
        quiz = QuizSystem("Quiz Title")
        quiz.add_question("What is 2+2?", ["3", "4", "5"], 1)
        n.add_quiz(quiz)
        out = str(tmp_path / "out.html")
        exporter = HtmlExporter()
        result = exporter.export(n.generate(), out)
        assert "Quiz Title" in result
        assert "What is 2+2?" in result

    def test_export_contains_sudoku_with_solution(self, tmp_path):
        n = Newspaper("Test")
        n.add_article(title="T", content="Content padding here...")
        n.add_sudoku("easy")
        out = str(tmp_path / "out.html")
        exporter = HtmlExporter()
        result = exporter.export(n.generate(), out)
        assert "Sudoku" in result
        assert "data-solution" in result

    def test_export_returns_string(self, tmp_path):
        n = Newspaper("Test")
        n.add_article(title="T", content="Content here...")
        out = str(tmp_path / "out.html")
        exporter = HtmlExporter()
        result = exporter.export(n.generate(), out)
        assert isinstance(result, str)
        assert len(result) > 0


class TestJsonExporter:
    def test_export_creates_file(self, tmp_path):
        n = Newspaper("JSON Test")
        n.add_article(title="News", content="Content here...")
        out = str(tmp_path / "out.json")
        exporter = JsonExporter()
        result = exporter.export(n.generate(), out)
        assert os.path.exists(out)

    def test_export_valid_json(self, tmp_path):
        n = Newspaper("Test")
        n.add_article(title="T", content="Content here...")
        out = str(tmp_path / "out.json")
        exporter = JsonExporter()
        result = exporter.export(n.generate(), out)
        data = json.loads(result)
        assert data["title"] == "Test"

    def test_export_has_all_keys(self, tmp_path):
        n = Newspaper("Test")
        n.add_article(title="T", content="Content here...")
        out = str(tmp_path / "out.json")
        exporter = JsonExporter()
        result = exporter.export(n.generate(), out)
        data = json.loads(result)
        for key in ["title", "date", "layout", "media", "articles", "quizzes", "sudokus", "crosswords", "statistics"]:
            assert key in data

    def test_export_sudoku_includes_solution(self, tmp_path):
        n = Newspaper("Test")
        n.add_article(title="T", content="Content here...")
        n.add_sudoku("medium")
        out = str(tmp_path / "out.json")
        exporter = JsonExporter()
        result = exporter.export(n.generate(), out)
        data = json.loads(result)
        sudoku = data["sudokus"][0]
        assert "solution" in sudoku
        assert len(sudoku["solution"]) == 9

    def test_export_returns_string(self, tmp_path):
        n = Newspaper("Test")
        n.add_article(title="T", content="Content here...")
        out = str(tmp_path / "out.json")
        exporter = JsonExporter()
        result = exporter.export(n.generate(), out)
        assert isinstance(result, str)
