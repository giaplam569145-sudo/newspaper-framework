"""JSON exporter implementation."""

import json
import logging
from .base import Exporter
from typing import Dict

logger = logging.getLogger(__name__)

class JsonExporter(Exporter):
    """Exports newspaper data to JSON."""

    def export(self, data: Dict, filename: str) -> str:
        """Exports the newspaper data as a JSON file.

        Args:
            data (Dict): The newspaper data to export.
            filename (str): The name of the output JSON file.

        Returns:
            str: The generated JSON content as a string.
        """
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json_str)

        logger.info("JSON exported: %s", filename)
        return json_str
