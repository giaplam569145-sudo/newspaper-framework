from flask import Flask, request, jsonify
from newspaper_framework import NewspaperFrameWork, QuizSystem

app = Flask(__name__)


class NewspaperAPI:
    def __init__(self):
        self.newspapers = {}
    
    def create_newspaper(self, title: str) -> dict:
        paper = NewspaperFrameWork(title)
        newspaper_id = f"np_{len(self.newspapers)}"
        self.newspapers[newspaper_id] = paper
        return {"id": newspaper_id, "title": title}
    
    def add_article(self, newspaper_id: str, article_data: dict) -> dict:
        if newspaper_id not in self.newspapers:
            return {"error": "Newspaper not found"}
        
        paper = self.newspapers[newspaper_id]
        article = paper.add_article(
            title=article_data.get("title", ""),
            content=article_data.get("content", ""),
            author=article_data.get("author", "Unbekannt"),
            category=article_data.get("category", "Allgemein"),
            priority=article_data.get("priority", 1)
        )
        return {"success": True, "article_id": len(paper.articles)}
    
    def export_newspaper(self, newspaper_id: str, fmt: str = "html") -> dict:
        if newspaper_id not in self.newspapers:
            return {"error": "Newspaper not found"}
        
        paper = self.newspapers[newspaper_id]
        filename = f"{newspaper_id}_zeitung.{fmt}"
        
        if fmt == "html":
            paper.export_html(filename)
        elif fmt == "json":
            paper.export_json(filename)
        else:
            return {"error": f"Unsupported format: {fmt}"}
        
        return {"success": True, "filename": filename}


api = NewspaperAPI()


@app.route('/api/newspaper', methods=['POST'])
def create_newspaper_endpoint():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "title is required"}), 400
    result = api.create_newspaper(data['title'])
    return jsonify(result), 201


@app.route('/api/newspaper/<newspaper_id>/article', methods=['POST'])
def add_article_endpoint(newspaper_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "request body required"}), 400
    result = api.add_article(newspaper_id, data)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 201


@app.route('/api/newspaper/<newspaper_id>/export', methods=['POST'])
def export_newspaper_endpoint(newspaper_id):
    data = request.get_json() or {}
    fmt = data.get("format", "html")
    result = api.export_newspaper(newspaper_id, fmt)
    if "error" in result:
        return jsonify(result), 404 if "not found" in result["error"] else 400
    return jsonify(result), 200


@app.route('/api/newspaper/<newspaper_id>', methods=['GET'])
def get_newspaper_endpoint(newspaper_id):
    if newspaper_id not in api.newspapers:
        return jsonify({"error": "Newspaper not found"}), 404
    paper = api.newspapers[newspaper_id]
    return jsonify(paper.generate())


if __name__ == '__main__':
    print("Newspaper Framework API Server startet...")
    app.run(debug=True, host='0.0.0.0', port=5000)
