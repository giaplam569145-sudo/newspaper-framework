"""HTML exporter implementation using Jinja2."""

from typing import Dict
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import os
from .base import Exporter

class HtmlExporter(Exporter):
    """Exports newspaper data to HTML."""

    def __init__(self):
        # We can use PackageLoader if installed as package, or FileSystemLoader for local dev.
        # Trying PackageLoader first.
        try:
             self.env = Environment(
                loader=PackageLoader("newspaper.export", "templates"),
                autoescape=select_autoescape()
            )
        except ImportError:
             # Fallback for when running locally without package install
             template_dir = os.path.join(os.path.dirname(__file__), "templates")
             self.env = Environment(
                loader=FileSystemLoader(template_dir),
                autoescape=select_autoescape()
            )

    def export(self, data: Dict, filename: str) -> str:
        """Exports the newspaper data as an HTML file.

        Args:
            data (Dict): The newspaper data to export.
            filename (str): The name of the output HTML file.

        Returns:
            str: The generated HTML content as a string.
        """
        template = self.env.get_template("base.html")

        # Prepare content HTMLs (pre-rendered by generators or rendered here?)
        # Ideally, we pass data to Jinja and let Jinja render.
        # But our generators have 'to_html'. To respect DRY and the current architecture,
        # we can pass the raw objects or pre-rendered HTML strings.
        # The 'data' dict currently contains dicts of objects (asdict).
        # We also have 'quizzes_html', 'sudokus_html' etc if we want to use the generators' logic.
        # But 'data' passed here is usually the output of 'generate()', which is all dicts.

        # Re-implementing rendering in Jinja is cleaner than mixing python-string-gen and Jinja.
        # However, Sudoku and Crossword generation logic is complex to port to Jinja.
        # I'll rely on the existing 'to_html' methods or similar logic if possible,
        # or rewrite them in Jinja if simple.

        # Current strategy: Use the data dict. For complex components (sudoku, crossword),
        # we might need to pass the HTML string or robustly handle it in Jinja.
        # The 'newspaper.generate()' returns dicts.
        # I will update 'newspaper.generate()' to optionally include HTMLs or handle it here.

        # Actually, let's look at what data contains.
        # 'quizzes': [quiz.generate_quiz()] -> dict
        # 'sudokus': [{'difficulty':..., 'grid':...}]

        # I'll implement Jinja macros or includes for these.

        html_content = template.render(data=data)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"HTML exported: {filename}")
        return html_content
