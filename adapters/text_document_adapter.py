from .base_document_adapter import BaseDocumentAdapter


class TextDocumentAdapter(BaseDocumentAdapter):
    """Adapter for raw text input passed directly from the CLI."""

    def load(self, source: str) -> str:
        return source.strip()
