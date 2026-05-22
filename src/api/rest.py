"""Rest API Server entry point."""

import logging

from flask import Flask, request, jsonify
from src.newspaper.core import Newspaper
from src.newspaper.content.quiz import QuizSystem
from src.newspaper.content.crossword import CrosswordGenerator
from src.newspaper.exceptions import NewspaperFrameworkError

app = Flask(__name__)
logger = logging.getLogger(__name__)


class NewspaperAPI:
    """A RESTful API wrapper for the Newspaper Framework."""

    def __init__(self):
        self.newspapers: dict[str, Newspaper] = {}

    def create_newspaper(self, title: str) -> dict:
        newspaper_id = f"np_{len(self.newspapers)}"
        paper = Newspaper(title)
        self.newspapers[newspaper_id] = paper
        return {"id": newspaper_id, "title": title}


api = NewspaperAPI()


@app.route('/api/newspaper', methods=['POST'])
def create_newspaper_endpoint():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    try:
        newspaper = api.create_newspaper(data["title"])
        return jsonify(newspaper), 201
    except NewspaperFrameworkError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/newspaper/<newspaper_id>/article', methods=['POST'])
def add_article_endpoint(newspaper_id):
    if newspaper_id not in api.newspapers:
        return jsonify({"error": "Newspaper not found"}), 404

    data = request.get_json()
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Title and content are required"}), 400

    paper = api.newspapers[newspaper_id]
    try:
        paper.add_article(
            title=data["title"],
            content=data["content"],
            author=data.get("author", "Unknown"),
            category=data.get("category", "General"),
            priority=data.get("priority", 1),
            force=data.get("force", False),
        )
        return jsonify({"success": True, "message": "Article added."}), 201
    except NewspaperFrameworkError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/newspaper/<newspaper_id>/quiz', methods=['POST'])
def add_quiz_endpoint(newspaper_id):
    if newspaper_id not in api.newspapers:
        return jsonify({"error": "Newspaper not found"}), 404

    data = request.get_json()
    if not data or "questions" not in data:
        return jsonify({"error": "Questions are required"}), 400

    paper = api.newspapers[newspaper_id]
    try:
        quiz = QuizSystem(title=data.get("title", "Quiz"))
        for q in data["questions"]:
            quiz.add_question(
                question=q["question"],
                options=q["options"],
                correct_index=q["correct_index"],
                category=q.get("category", "General"),
            )
        paper.add_quiz(quiz)
        return jsonify({"success": True, "message": "Quiz added."}), 201
    except (NewspaperFrameworkError, KeyError) as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/newspaper/<newspaper_id>/sudoku', methods=['POST'])
def add_sudoku_endpoint(newspaper_id):
    if newspaper_id not in api.newspapers:
        return jsonify({"error": "Newspaper not found"}), 404

    data = request.get_json() or {}
    difficulty = data.get("difficulty", "medium")

    if difficulty not in ("easy", "medium", "hard"):
        return jsonify({"error": "Difficulty must be easy, medium, or hard"}), 400

    paper = api.newspapers[newspaper_id]
    paper.add_sudoku(difficulty)
    return jsonify({"success": True, "message": f"Sudoku ({difficulty}) added."}), 201


@app.route('/api/newspaper/<newspaper_id>/crossword', methods=['POST'])
def add_crossword_endpoint(newspaper_id):
    if newspaper_id not in api.newspapers:
        return jsonify({"error": "Newspaper not found"}), 404

    data = request.get_json()
    if not data or "words" not in data or "clues" not in data:
        return jsonify({"error": "words and clues are required"}), 400

    paper = api.newspapers[newspaper_id]
    try:
        generator = CrosswordGenerator(
            words=data["words"],
            clues=data["clues"],
        )
        crossword = generator.generate()
        paper.add_crossword(crossword)
        return jsonify({"success": True, "message": "Crossword added."}), 201
    except NewspaperFrameworkError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/newspaper/<newspaper_id>/export', methods=['POST'])
def export_newspaper_endpoint(newspaper_id):
    if newspaper_id not in api.newspapers:
        return jsonify({"error": "Newspaper not found"}), 404

    data = request.get_json() or {}
    export_format = data.get("format", "html")

    paper = api.newspapers[newspaper_id]
    filename = f"{newspaper_id}_newspaper.{export_format}"

    try:
        if export_format == "html":
            paper.export_html(filename)
        elif export_format == "json":
            paper.export_json(filename)
        else:
            return jsonify({"error": "Unsupported format. Use html or json."}), 400
        return jsonify({"success": True, "filename": filename})
    except NewspaperFrameworkError as e:
        return jsonify({"error": str(e)}), 400


def run_server():
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting Newspaper Framework API Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
