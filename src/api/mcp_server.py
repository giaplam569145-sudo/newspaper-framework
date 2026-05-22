"""MCP Server entry point."""

import logging

from src.newspaper.core import Newspaper
from src.newspaper.content.quiz import QuizSystem
from src.newspaper.exceptions import NewspaperFrameworkError

logger = logging.getLogger(__name__)


class NewspaperMCPServer:
    """An MCP server for the Newspaper Framework."""

    def __init__(self):
        self.newspapers: dict[str, Newspaper] = {}

    def create_newspaper(self, title: str) -> dict:
        try:
            paper = Newspaper(title)
            newspaper_id = f"np_{len(self.newspapers)}"
            self.newspapers[newspaper_id] = paper
            return {"id": newspaper_id, "title": title}
        except NewspaperFrameworkError as e:
            return {"error": str(e)}

    def add_article(self, newspaper_id: str, article_data: dict) -> dict:
        if newspaper_id not in self.newspapers:
            return {"error": "Newspaper not found"}

        paper = self.newspapers[newspaper_id]
        try:
            paper.add_article(
                title=article_data.get("title", ""),
                content=article_data.get("content", ""),
                author=article_data.get("author", "Unknown"),
                category=article_data.get("category", "General"),
                priority=article_data.get("priority", 1),
                force=article_data.get("force", False),
            )
            return {"success": True, "article_id": len(paper.articles)}
        except NewspaperFrameworkError as e:
            return {"error": str(e)}

    def add_quiz(self, newspaper_id: str, quiz_data: dict) -> dict:
        if newspaper_id not in self.newspapers:
            return {"error": "Newspaper not found"}

        paper = self.newspapers[newspaper_id]
        try:
            quiz = QuizSystem(title=quiz_data.get("title", "Quiz"))
            for q in quiz_data.get("questions", []):
                quiz.add_question(
                    question=q["question"],
                    options=q["options"],
                    correct_index=q["correct_index"],
                )
            paper.add_quiz(quiz)
            return {"success": True, "quiz_id": len(paper.quizzes)}
        except (NewspaperFrameworkError, KeyError) as e:
            return {"error": str(e)}

    def add_sudoku(self, newspaper_id: str, difficulty: str = "medium") -> dict:
        if newspaper_id not in self.newspapers:
            return {"error": "Newspaper not found"}

        if difficulty not in ("easy", "medium", "hard"):
            return {"error": "Difficulty must be easy, medium, or hard"}

        paper = self.newspapers[newspaper_id]
        paper.add_sudoku(difficulty)
        return {"success": True, "sudoku_id": len(paper.sudokus)}

    def export_newspaper(self, newspaper_id: str, format: str = "html") -> dict:
        if newspaper_id not in self.newspapers:
            return {"error": "Newspaper not found"}

        paper = self.newspapers[newspaper_id]
        filename = f"{newspaper_id}_newspaper.{format}"

        try:
            if format == "html":
                paper.export_html(filename)
            elif format == "json":
                paper.export_json(filename)
            else:
                return {"error": f"Unsupported format: {format}"}
            return {"success": True, "filename": filename}
        except NewspaperFrameworkError as e:
            return {"error": str(e)}


def get_tools():
    """Returns tool definitions for MCP integration."""
    return [
        {
            "name": "create_newspaper",
            "description": "Create a new newspaper with a title",
            "parameters": {"title": {"type": "string", "required": True}},
        },
        {
            "name": "add_article",
            "description": "Add an article to an existing newspaper",
            "parameters": {
                "newspaper_id": {"type": "string", "required": True},
                "title": {"type": "string", "required": True},
                "content": {"type": "string", "required": True},
                "author": {"type": "string"},
                "category": {"type": "string"},
                "priority": {"type": "integer"},
            },
        },
        {
            "name": "add_quiz",
            "description": "Add a quiz to an existing newspaper",
            "parameters": {
                "newspaper_id": {"type": "string", "required": True},
                "title": {"type": "string"},
                "questions": {"type": "array", "required": True},
            },
        },
        {
            "name": "add_sudoku",
            "description": "Add a sudoku puzzle to an existing newspaper",
            "parameters": {
                "newspaper_id": {"type": "string", "required": True},
                "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
            },
        },
        {
            "name": "export_newspaper",
            "description": "Export a newspaper as HTML or JSON",
            "parameters": {
                "newspaper_id": {"type": "string", "required": True},
                "format": {"type": "string", "enum": ["html", "json"]},
            },
        },
    ]


async def run_server():
    """Run the MCP server. Requires the mcp package to be installed."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting Newspaper Framework MCP Server...")

    try:
        from mcp import MCPServer
    except ImportError:
        logger.error(
            "MCP package not installed. Install with: pip install mcp"
        )
        return

    server = MCPServer()
    mcp_server = NewspaperMCPServer()

    server.add_tool("create_newspaper", mcp_server.create_newspaper)
    server.add_tool("add_article", mcp_server.add_article)
    server.add_tool("add_quiz", mcp_server.add_quiz)
    server.add_tool("add_sudoku", mcp_server.add_sudoku)
    server.add_tool("export_newspaper", mcp_server.export_newspaper)

    await server.run()
