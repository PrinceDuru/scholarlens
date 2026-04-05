from abc import ABC, abstractmethod


class BaseDocumentAdapter(ABC):
    """Abstract adapter — normalises different document input formats to plain text."""

    @abstractmethod
    def load(self, source: str) -> str:
        """Load the document from *source* and return its plain-text content."""
