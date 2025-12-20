"""Base class for exporters."""

from abc import ABC, abstractmethod
from typing import Dict

class Exporter(ABC):
    """Abstract base class for exporters."""

    @abstractmethod
    def export(self, data: Dict, filename: str) -> str:
        """Exports data to a file."""
        pass
