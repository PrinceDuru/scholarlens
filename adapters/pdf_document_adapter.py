import os
from .base_document_adapter import BaseDocumentAdapter


class PDFDocumentAdapter(BaseDocumentAdapter):
    """Adapter for PDF file input — extracts plain text using PyPDF2."""

    def load(self, source: str) -> str:
        try:
            import PyPDF2
        except ImportError:
            raise ImportError(
                "PyPDF2 is required for PDF support. "
                "Install it with: pip install PyPDF2"
            )

        if not os.path.isfile(source):
            raise FileNotFoundError(f"PDF file not found: {source}")

        text_parts = []
        with open(source, "rb") as fh:
            reader = PyPDF2.PdfReader(fh)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        full_text = "\n".join(text_parts).strip()
        if not full_text:
            raise ValueError(f"No extractable text found in PDF: {source}")
        return full_text
