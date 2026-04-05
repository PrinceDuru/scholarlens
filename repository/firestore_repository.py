import os
from typing import List, Optional

from google.cloud import firestore

from models.paper import Paper
from models.summary import Summary
from models.extraction_result import ExtractionResult

_SERVICE_ACCOUNT_PATH = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS", "serviceAccount.json"
)


class FirestoreRepository:
    """Repository — abstracts all Firestore read/write operations.

    Collections used:
        papers       – paper metadata (id, title, hash, source type, timestamp)
        summaries    – LLM-generated summaries and contributions
        extractions  – structured elements: datasets, methods, citations
        run_logs     – per-run metadata, model info, status
    """

    def __init__(self):
        self._db = firestore.Client.from_service_account_json(
            _SERVICE_ACCOUNT_PATH
        )

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def save_paper(self, paper: Paper) -> str:
        """Persist paper metadata. Raw text is intentionally excluded."""
        self._db.collection("papers").document(paper.paper_id).set(
            paper.to_dict()
        )
        return paper.paper_id

    def save_summary(self, summary: Summary) -> str:
        """Persist a Summary document."""
        self._db.collection("summaries").document(summary.summary_id).set(
            summary.to_dict()
        )
        return summary.summary_id

    def save_extraction(self, extraction: ExtractionResult) -> str:
        """Persist an ExtractionResult document."""
        self._db.collection("extractions").document(
            extraction.extraction_id
        ).set(extraction.to_dict())
        return extraction.extraction_id

    def save_run_log(self, log: dict) -> str:
        """Append a run-log entry and return the auto-generated document id."""
        doc_ref = self._db.collection("run_logs").document()
        doc_ref.set(log)
        return doc_ref.id

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def list_papers(self, limit: int = 20) -> List[dict]:
        """Return up to *limit* paper metadata documents."""
        docs = self._db.collection("papers").limit(limit).stream()
        return [doc.to_dict() for doc in docs]

    def get_summary(self, paper_id: str) -> Optional[dict]:
        """Return the most recent summary for *paper_id*, or None."""
        docs = (
            self._db.collection("summaries")
            .where("paper_id", "==", paper_id)
            .limit(1)
            .stream()
        )
        for doc in docs:
            return doc.to_dict()
        return None

    def get_extraction(self, paper_id: str) -> Optional[dict]:
        """Return the most recent extraction for *paper_id*, or None."""
        docs = (
            self._db.collection("extractions")
            .where("paper_id", "==", paper_id)
            .limit(1)
            .stream()
        )
        for doc in docs:
            return doc.to_dict()
        return None
