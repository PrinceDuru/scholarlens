from adapters.base_document_adapter import BaseDocumentAdapter
from adapters.text_document_adapter import TextDocumentAdapter
from adapters.pdf_document_adapter import PDFDocumentAdapter


class DocumentProviderFactory:
    """Factory Method — instantiates the correct document adapter at runtime."""

    @staticmethod
    def create(source_type: str) -> BaseDocumentAdapter:
        """Return the appropriate document adapter for *source_type*.

        Args:
            source_type: One of ``"text"`` or ``"pdf"``.

        Returns:
            A concrete :class:`BaseDocumentAdapter` instance.

        Raises:
            ValueError: If *source_type* is not supported.
        """
        normalised = source_type.lower().strip()
        if normalised == "text":
            return TextDocumentAdapter()
        if normalised == "pdf":
            return PDFDocumentAdapter()
        raise ValueError(
            f"Unsupported document source type '{source_type}'. "
            "Supported types: 'text', 'pdf'."
        )
