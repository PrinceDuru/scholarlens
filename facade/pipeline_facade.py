import datetime
from typing import List, Tuple

from adapters.base_document_adapter import BaseDocumentAdapter
from adapters.base_llm_adapter import BaseLLMAdapter
from factory.document_provider_factory import DocumentProviderFactory
from factory.llm_provider_factory import LLMProviderFactory
from models.paper import Paper
from models.summary import Summary
from models.extraction_result import ExtractionResult
from repository.firestore_repository import FirestoreRepository


# ---------------------------------------------------------------------------
# LLM output parsers
# ---------------------------------------------------------------------------

def _parse_contributions(raw: str) -> List[str]:
    """Extract bullet-point lines from the contributions LLM response."""
    results = []
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("• "):
            results.append(stripped.lstrip("-•").strip())
    return results if results else [raw.strip()]


def _parse_datasets_methods(raw: str) -> Tuple[List[str], List[str]]:
    """Parse 'Datasets: ...' and 'Methods: ...' lines from the LLM response."""
    datasets: List[str] = []
    methods: List[str] = []
    for line in raw.splitlines():
        lower = line.lower()
        if lower.startswith("datasets:"):
            value = line.split(":", 1)[1].strip()
            datasets = [d.strip() for d in value.split(",") if d.strip()]
        elif lower.startswith("methods:"):
            value = line.split(":", 1)[1].strip()
            methods = [m.strip() for m in value.split(",") if m.strip()]
    return datasets, methods


def _parse_citations(raw: str) -> List[str]:
    """Split LLM citation output into individual citation strings."""
    return [line.strip() for line in raw.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------

class PipelineFacade:
    """Facade — single entry point that coordinates document parsing,
    LLM inference, and persistence for the ScholarLens pipeline.

    Design patterns in play:
        - **Facade** (this class): hides the multi-step pipeline behind
          a single ``process()`` call.
        - **Factory Method**: delegates adapter creation to
          :class:`DocumentProviderFactory` and :class:`LLMProviderFactory`.
        - **Adapter**: the concrete adapters returned by the factories
          normalise input formats and LLM providers.
    """

    def __init__(self, llm_provider: str = "huggingface"):
        self._llm_provider = llm_provider
        self._repo = FirestoreRepository()

    def process(
        self,
        source_type: str,
        source: str,
        title: str = "",
    ) -> Tuple[Paper, Summary, ExtractionResult]:
        """Run the full ScholarLens pipeline.

        Steps:
            1. Load document text via the appropriate adapter (Factory → Adapter).
            2. Build a :class:`Paper` domain object and persist it.
            3. Call the LLM adapter for all four extraction tasks.
            4. Parse LLM responses into :class:`Summary` and
               :class:`ExtractionResult`; persist both.
            5. Write a run-log entry.
            6. Return all three domain objects to the caller.

        Args:
            source_type: ``"text"`` or ``"pdf"``.
            source:      The raw text string or path to a PDF file.
            title:       Optional human-readable title for storage/display.

        Returns:
            A tuple ``(Paper, Summary, ExtractionResult)``.
        """
        # Step 1 – load document text
        doc_adapter: BaseDocumentAdapter = DocumentProviderFactory.create(
            source_type
        )
        raw_text = doc_adapter.load(source)

        # Step 2 – build and persist Paper
        paper = Paper(raw_text=raw_text, source_type=source_type, title=title)
        self._repo.save_paper(paper)

        # Step 3 – LLM calls
        llm_adapter: BaseLLMAdapter = LLMProviderFactory.create(
            self._llm_provider
        )
        summary_raw = llm_adapter.call("summarize", raw_text)
        contributions_raw = llm_adapter.call("contributions", raw_text)
        datasets_methods_raw = llm_adapter.call("datasets_methods", raw_text)
        citations_raw = llm_adapter.call("citations", raw_text)

        # Step 4a – build and persist Summary
        contributions = _parse_contributions(contributions_raw)
        summary = Summary(
            paper_id=paper.paper_id,
            summary_text=summary_raw,
            contributions=contributions,
            model_name=llm_adapter.model_name,
        )
        self._repo.save_summary(summary)

        # Step 4b – build and persist ExtractionResult
        datasets, methods = _parse_datasets_methods(datasets_methods_raw)
        citations = _parse_citations(citations_raw)
        extraction = ExtractionResult(
            paper_id=paper.paper_id,
            datasets=datasets,
            methods=methods,
            citations=citations,
            model_name=llm_adapter.model_name,
        )
        self._repo.save_extraction(extraction)

        # Step 5 – run log
        self._repo.save_run_log({
            "paper_id": paper.paper_id,
            "model_name": llm_adapter.model_name,
            "source_type": source_type,
            "tasks": ["summarize", "contributions", "datasets_methods", "citations"],
            "status": "success",
            "timestamp": datetime.datetime.utcnow().isoformat(),
        })

        return paper, summary, extraction
