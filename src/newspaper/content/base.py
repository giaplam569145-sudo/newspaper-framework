"""Base class for content generators."""

from abc import ABC, abstractmethod
from typing import Any, Dict

class ContentGenerator(ABC):
    """Abstract base class for content generators."""

    @abstractmethod
    def generate(self) -> Any:
        """Generates the content."""
        pass

    def to_dict(self) -> Dict:
        """Returns dictionary representation of the content for JSON export."""
        return {}
