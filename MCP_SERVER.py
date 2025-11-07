# Newspaper Framework MCP Server
# Ermöglicht Integration in AI-Agents und Entwicklungsumgebungen

"""
MCP-SERVER FÜR NEWSPAPER FRAMEWORK

FUNKTIONALITÄT:
- MCP-Protokoll für Framework-Zugriff
- Standardisierte Schnittstelle für LLMs
- Wiederverwendung des bestehenden Frameworks

VERWENDUNG FÜR DAS LLM:
1. Server starten: python MCP_SERVER.py
2. Framework-Funktionen über MCP verfügbar machen
"""

import asyncio
from mcp import MCPServer
from newspaper_framework import NewspaperFrameWork, QuizSystem

class NewspaperMCPServer:
    """An MCP server for the Newspaper Framework.

    This class exposes the framework's functionalities over the MCP protocol,
    allowing AI agents to interact with it through standardized tool calls.

    Attributes:
        newspapers (Dict[str, NewspaperFrameWork]): A dictionary to store
            and manage newspaper instances.
    """

    def __init__(self):
        """Initializes the NewspaperMCPServer."""
        self.newspapers = {}
    
    def create_newspaper(self, title: str) -> Dict:
        """Creates a new newspaper via an MCP tool call.

        Args:
            title (str): The title for the new newspaper.

        Returns:
            Dict: A dictionary containing the ID and title of the new newspaper.
        """
        paper = NewspaperFrameWork(title)
        newspaper_id = f"np_{len(self.newspapers)}"
        self.newspapers[newspaper_id] = paper
        return {"id": newspaper_id, "title": title}
    
    def add_article_via_mcp(self, newspaper_id: str, article_data: Dict) -> Dict:
        """Adds an article to a newspaper via an MCP tool call.

        Args:
            newspaper_id (str): The ID of the newspaper to add the article to.
            article_data (Dict): A dictionary containing the article's data.

        Returns:
            Dict: A confirmation dictionary with the new article's ID, or
                an error message.
        """
        if newspaper_id not in self.newspapers:
            return {"error": "Newspaper not found"}
        
        paper = self.newspapers[newspaper_id]
        article = paper.add_article(
            title=article_data.get("title", ""),
            content=article_data.get("content", ""),
            author=article_data.get("author", "Unknown"),
            category=article_data.get("category", "General"),
            priority=article_data.get("priority", 1)
        )
        return {"success": True, "article_id": len(paper.articles)}
    
    def export_newspaper_via_mcp(self, newspaper_id: str, format: str = "html") -> Dict:
        """Exports a newspaper via an MCP tool call.

        Args:
            newspaper_id (str): The ID of the newspaper to export.
            format (str): The export format ('html' or 'json').

        Returns:
            Dict: A confirmation dictionary with the exported file's name, or
                an error message.
        """
        if newspaper_id not in self.newspapers:
            return {"error": "Newspaper not found"}
        
        paper = self.newspapers[newspaper_id]
        filename = f"{newspaper_id}_newspaper.{format}"
        
        if format == "html":
            paper.export_html(filename)
        elif format == "json":
            paper.export_json(filename)
        
        return {"success": True, "filename": filename}

async def main():
    """Initializes and runs the MCP server."""
    print("Starting Newspaper Framework MCP Server...")
    
    server = MCPServer()
    
    mcp_server = NewspaperMCPServer()
    
    server.add_tool("create_newspaper", mcp_server.create_newspaper)
    server.add_tool("add_article", mcp_server.add_article_via_mcp)
    server.add_tool("export_newspaper", mcp_server.export_newspaper_via_mcp)
    
    # Server starten
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())

# BEISPIEL FÜR DAS LLM:
"""
MCP-TOOL AUFRUFE:

1. Zeitung erstellen:
   create_newspaper({"title": "AI Morgenzeitung"})

2. Artikel hinzufügen:
   add_article({
       "newspaper_id": "np_0",
       "title": "KI revolutioniert Zeitungswesen",
       "content": "Das Newspaper Framework...",
       "author": "KI-Redakteur",
       "category": "Technologie",
       "priority": 1
   })

3. Zeitung exportieren:
   export_newspaper({
       "newspaper_id": "np_0",
       "format": "html"
   })
"""