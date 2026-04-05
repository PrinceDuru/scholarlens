from typing import List

from models.paper import Paper
from models.summary import Summary
from models.extraction_result import ExtractionResult

_WIDE = "=" * 66
_THIN = "-" * 66


class CLIView:
    """View — formats and prints ScholarLens results to stdout.

    Responsible solely for presentation; contains no business logic.
    """

    # ------------------------------------------------------------------
    # Header / footer
    # ------------------------------------------------------------------

    def display_header(self, title: str = "") -> None:
        print(_WIDE)
        print("         SCHOLARLENS — PAPER ANALYSIS")
        if title:
            print(f"         {title}")
        print(_WIDE)

    def display_footer(self, model_name: str) -> None:
        print("\n" + _WIDE)
        print(f"  Model            : {model_name}")
        print("  Results saved to : Firestore (papers / summaries / extractions / run_logs)")
        print(_WIDE + "\n")

    # ------------------------------------------------------------------
    # Domain object renderers
    # ------------------------------------------------------------------

    def display_paper_info(self, paper: Paper) -> None:
        print(f"\n  Paper ID  : {paper.paper_id}")
        print(f"  Source    : {paper.source_type.upper()}")
        if paper.title:
            print(f"  Title     : {paper.title}")
        print(f"  SHA-256   : {paper.text_hash[:20]}...")
        print(f"  Timestamp : {paper.timestamp}")

    def display_summary(self, summary: Summary) -> None:
        print("\n" + _THIN)
        print("  SUMMARY")
        print(_THIN)
        print(summary.summary_text)

        print("\n" + _THIN)
        print("  KEY CONTRIBUTIONS")
        print(_THIN)
        for i, contrib in enumerate(summary.contributions, 1):
            print(f"  {i}. {contrib}")

    def display_extraction(self, extraction: ExtractionResult) -> None:
        print("\n" + _THIN)
        print("  DATASETS & METHODS")
        print(_THIN)

        if extraction.datasets:
            print("  Datasets :")
            for d in extraction.datasets:
                print(f"    · {d}")
        else:
            print("  Datasets : (none identified)")

        if extraction.methods:
            print("  Methods  :")
            for m in extraction.methods:
                print(f"    · {m}")
        else:
            print("  Methods  : (none identified)")

        print("\n" + _THIN)
        print("  CITATIONS")
        print(_THIN)
        if extraction.citations:
            for cite in extraction.citations:
                print(f"  {cite}")
        else:
            print("  (none identified)")

    # ------------------------------------------------------------------
    # List / search renderers
    # ------------------------------------------------------------------

    def display_papers_list(self, papers: List[dict]) -> None:
        if not papers:
            print("\n  No papers found in the database.\n")
            return
        print(_WIDE)
        print("  PREVIOUSLY PROCESSED PAPERS")
        print(_WIDE)
        for i, p in enumerate(papers, 1):
            title = p.get("title") or "(no title)"
            pid = p.get("paper_id", "?")[:8]
            src = p.get("source_type", "?").upper()
            ts = p.get("timestamp", "?")
            print(f"  {i:>3}. [{pid}...]  {title}")
            print(f"        Source: {src}  |  {ts}")
        print(_WIDE + "\n")

    # ------------------------------------------------------------------
    # Error display
    # ------------------------------------------------------------------

    def display_error(self, message: str) -> None:
        print(f"\n[ERROR] {message}\n")
