"""HTML exporter implementation using Jinja2."""

import logging
import os
from typing import Any, Dict
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from .base import Exporter

logger = logging.getLogger(__name__)

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
            template_dir = os.path.join(os.path.dirname(__file__), "templates")
            self.env = Environment(
                loader=FileSystemLoader(template_dir),
                autoescape=select_autoescape()
            )

    def export(self, data: Dict[str, Any], filename: str) -> str:
        """Exports the newspaper data as an HTML file.

        Args:
            data (Dict): The newspaper data to export.
            filename (str): The name of the output HTML file.

        Returns:
            str: The generated HTML content as a string.
        """
        template = self.env.get_template("base.html")

        # Current strategy: Pass data dict to Jinja for rendering.

        html_content = template.render(data=data)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info("HTML exported: %s", filename)
        return html_content
