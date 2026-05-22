import json
import pytest
from src.api.rest import app, api


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_api():
    api.newspapers.clear()


class TestCreateNewspaper:
    def test_create_success(self, client):
        resp = client.post("/api/newspaper", json={"title": "Test Paper"})
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["title"] == "Test Paper"
        assert "id" in data

    def test_create_missing_title(self, client):
        resp = client.post("/api/newspaper", json={})
        assert resp.status_code == 400

    def test_create_empty_title(self, client):
        resp = client.post("/api/newspaper", json={"title": ""})
        assert resp.status_code == 400


class TestAddArticle:
    def test_add_success(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        resp = client.post("/api/newspaper/np_0/article", json={
            "title": "News",
            "content": "Some article content here...",
        })
        assert resp.status_code == 201

    def test_add_short_content_without_force(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        resp = client.post("/api/newspaper/np_0/article", json={
            "title": "Short",
            "content": "hi",
        })
        assert resp.status_code == 400

    def test_add_short_content_with_force(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        resp = client.post("/api/newspaper/np_0/article", json={
            "title": "Short",
            "content": "hi",
            "force": True,
        })
        assert resp.status_code == 201

    def test_add_missing_fields(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        resp = client.post("/api/newspaper/np_0/article", json={"title": "No content"})
        assert resp.status_code == 400

    def test_add_to_nonexistent_newspaper(self, client):
        resp = client.post("/api/newspaper/np_99/article", json={
            "title": "T", "content": "Content here..."
        })
        assert resp.status_code == 404


class TestAddQuiz:
    def test_add_success(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        resp = client.post("/api/newspaper/np_0/quiz", json={
            "title": "Quiz",
            "questions": [
                {"question": "What is AI?", "options": ["AI", "BI"], "correct_index": 0}
            ],
        })
        assert resp.status_code == 201

    def test_add_missing_questions(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        resp = client.post("/api/newspaper/np_0/quiz", json={"title": "Quiz"})
        assert resp.status_code == 400


class TestAddSudoku:
    def test_add_success(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        resp = client.post("/api/newspaper/np_0/sudoku", json={"difficulty": "easy"})
        assert resp.status_code == 201

    def test_add_default_difficulty(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        resp = client.post("/api/newspaper/np_0/sudoku", json={})
        assert resp.status_code == 201

    def test_add_invalid_difficulty(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        resp = client.post("/api/newspaper/np_0/sudoku", json={"difficulty": "impossible"})
        assert resp.status_code == 400


class TestAddCrossword:
    def test_add_success(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        resp = client.post("/api/newspaper/np_0/crossword", json={
            "words": ["python", "html"],
            "clues": {"python": "A language", "html": "A markup"},
        })
        assert resp.status_code == 201

    def test_add_missing_fields(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        resp = client.post("/api/newspaper/np_0/crossword", json={"words": ["test"]})
        assert resp.status_code == 400


class TestExport:
    def test_export_html(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        client.post("/api/newspaper/np_0/article", json={
            "title": "News", "content": "Content here..."
        })
        resp = client.post("/api/newspaper/np_0/export", json={"format": "html"})
        assert resp.status_code == 200
        assert resp.get_json()["success"] is True

    def test_export_json(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        client.post("/api/newspaper/np_0/article", json={
            "title": "News", "content": "Content here..."
        })
        resp = client.post("/api/newspaper/np_0/export", json={"format": "json"})
        assert resp.status_code == 200

    def test_export_unsupported_format(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        client.post("/api/newspaper/np_0/article", json={
            "title": "News", "content": "Content here..."
        })
        resp = client.post("/api/newspaper/np_0/export", json={"format": "pdf"})
        assert resp.status_code == 400

    def test_export_empty_newspaper(self, client):
        client.post("/api/newspaper", json={"title": "Test"})
        resp = client.post("/api/newspaper/np_0/export", json={"format": "html"})
        assert resp.status_code == 400
