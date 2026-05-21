"""Rest API Server entry point."""

from flask import Flask, request, jsonify
from src.newspaper.core import Newspaper

app = Flask(__name__)

class NewspaperAPI:
    """A RESTful API wrapper for the Newspaper Framework."""

    def __init__(self):
        self.newspapers = {}

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

    newspaper = api.create_newspaper(data["title"])
    return jsonify(newspaper), 201

@app.route('/api/newspaper/<newspaper_id>/article', methods=['POST'])
def add_article_endpoint(newspaper_id):
    if newspaper_id not in api.newspapers:
        return jsonify({"error": "Newspaper not found"}), 404

    data = request.get_json()
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Title and content are required"}), 400

    paper = api.newspapers[newspaper_id]
    paper.add_article(
        title=data["title"],
        content=data["content"],
        author=data.get("author", "Unknown"),
        category=data.get("category", "General"),
        priority=data.get("priority", 1)
    )
    return jsonify({"success": True, "message": "Article added."}), 201

@app.route('/api/newspaper/<newspaper_id>/export', methods=['POST'])
def export_newspaper_endpoint(newspaper_id):
    if newspaper_id not in api.newspapers:
        return jsonify({"error": "Newspaper not found"}), 404

    data = request.get_json()
    export_format = data.get("format", "html")

    paper = api.newspapers[newspaper_id]
    filename = f"{newspaper_id}_newspaper.{export_format}"

    if export_format == "html":
        paper.export_html(filename)
    elif export_format == "json":
        paper.export_json(filename)
    else:
        return jsonify({"error": "Unsupported format"}), 400

    return jsonify({"success": True, "filename": filename})

def run_server():
    print("Starting Newspaper Framework API Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
