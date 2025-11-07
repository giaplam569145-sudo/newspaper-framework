# Newspaper Framework REST API Server
# Enables remote access to framework functionalities

"""
REST-API FOR NEWSPAPER FRAMEWORK

FUNCTIONALITY:
- HTTP endpoints for all framework methods
- JSON-based communication
- Reuse of the existing framework

USAGE FOR LLM:
1. Start the server: python api_server.py
2. Use API endpoints: POST /api/newspaper
3. Call framework functions via HTTP
"""

from flask import Flask, request, jsonify
from newspaper_framework import NewspaperFrameWork

app = Flask(__name__)

class NewspaperAPI:
    """A RESTful API wrapper for the Newspaper Framework.

    This class provides methods to create and manage newspapers via an API,
    allowing for remote, HTTP-based interaction with the framework.

    Attributes:
        newspapers (Dict[str, NewspaperFrameWork]): A dictionary to store
            and manage newspaper instances, with newspaper IDs as keys.
    """

    def __init__(self):
        """Initializes the NewspaperAPI."""
        self.newspapers = {}
    
    def create_newspaper(self, title: str) -> Dict:
        """Creates a new newspaper instance.

        Args:
            title (str): The title for the new newspaper.

        Returns:
            Dict: A dictionary containing the ID and title of the new newspaper.
        """
        newspaper_id = f"np_{len(self.newspapers)}"
        paper = NewspaperFrameWork(title)
        self.newspapers[newspaper_id] = paper
        return {"id": newspaper_id, "title": title}

api = NewspaperAPI()

@app.route('/api/newspaper', methods=['POST'])
def create_newspaper_endpoint():
    """API endpoint to create a new newspaper.

    This endpoint expects a JSON payload with a "title" field.

    Returns:
        A JSON response with the new newspaper's ID and title, or an
        error message.
    """
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    newspaper = api.create_newspaper(data["title"])
    return jsonify(newspaper), 201

@app.route('/api/newspaper/<newspaper_id>/article', methods=['POST'])
def add_article_endpoint(newspaper_id):
    """API endpoint to add an article to a newspaper.

    This endpoint expects a JSON payload with article data.

    Args:
        newspaper_id (str): The ID of the newspaper to add the article to.

    Returns:
        A JSON response confirming the article was added, or an error message.
    """
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
    """API endpoint to export a newspaper.

    This endpoint expects a JSON payload with an export format ('html' or 'json').

    Args:
        newspaper_id (str): The ID of the newspaper to export.

    Returns:
        A JSON response with the filename of the exported newspaper, or an
        error message.
    """
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

if __name__ == '__main__':
    print("Starting Newspaper Framework API Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
