"""MCP Server entry point."""

import asyncio
from mcp import MCPServer
from src.newspaper.core import Newspaper

class NewspaperMCPServer:
    """An MCP server for the Newspaper Framework."""

    def __init__(self):
        self.newspapers = {}

    def create_newspaper(self, title: str) -> dict:
        paper = Newspaper(title)
        newspaper_id = f"np_{len(self.newspapers)}"
        self.newspapers[newspaper_id] = paper
        return {"id": newspaper_id, "title": title}

    def add_article_via_mcp(self, newspaper_id: str, article_data: dict) -> dict:
        if newspaper_id not in self.newspapers:
            return {"error": "Newspaper not found"}

        paper = self.newspapers[newspaper_id]
        paper.add_article(
            title=article_data.get("title", ""),
            content=article_data.get("content", ""),
            author=article_data.get("author", "Unknown"),
            category=article_data.get("category", "General"),
            priority=article_data.get("priority", 1)
        )
        return {"success": True, "article_id": len(paper.articles)}

    def export_newspaper_via_mcp(self, newspaper_id: str, format: str = "html") -> dict:
        if newspaper_id not in self.newspapers:
            return {"error": "Newspaper not found"}

        paper = self.newspapers[newspaper_id]
        filename = f"{newspaper_id}_newspaper.{format}"

        if format == "html":
            paper.export_html(filename)
        elif format == "json":
            paper.export_json(filename)

        return {"success": True, "filename": filename}

async def run_server():
    print("Starting Newspaper Framework MCP Server...")

    server = MCPServer()
    mcp_server = NewspaperMCPServer()

    server.add_tool("create_newspaper", mcp_server.create_newspaper)
    server.add_tool("add_article", mcp_server.add_article_via_mcp)
    server.add_tool("export_newspaper", mcp_server.export_newspaper_via_mcp)

    await server.run()
