import asyncio
from typing import Dict
from newspaper_framework import NewspaperFrameWork, QuizSystem


class NewspaperMCPServer:
    def __init__(self):
        self.newspapers: Dict = {}
    
    def create_newspaper(self, title: str) -> Dict:
        paper = NewspaperFrameWork(title)
        newspaper_id = f"np_{len(self.newspapers)}"
        self.newspapers[newspaper_id] = paper
        return {"id": newspaper_id, "title": title}
    
    def add_article(self, newspaper_id: str, article_data: Dict) -> Dict:
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
    
    def export_newspaper(self, newspaper_id: str, fmt: str = "html") -> Dict:
        if newspaper_id not in self.newspapers:
            return {"error": "Newspaper not found"}
        
        paper = self.newspapers[newspaper_id]
        filename = f"{newspaper_id}_zeitung.{fmt}"
        
        if fmt == "html":
            paper.export_html(filename)
        elif fmt == "json":
            paper.export_json(filename)
        
        return {"success": True, "filename": filename}


def get_tools():
    mcp = NewspaperMCPServer()
    return {
        "create_newspaper": mcp.create_newspaper,
        "add_article": mcp.add_article,
        "export_newspaper": mcp.export_newspaper,
    }


if __name__ == "__main__":
    print("Newspaper Framework MCP Server bereit.")
    print("Verfuegbare Tools:", list(get_tools().keys()))
