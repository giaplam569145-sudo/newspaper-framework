"""Base class for exporters."""

from abc import ABC, abstractmethod
from typing import Any, Dict

class Exporter(ABC):

    @abstractmethod
    def export(self, data: Dict[str, Any], filename: str) -> str:
        """Exports data to a file."""
        pass
