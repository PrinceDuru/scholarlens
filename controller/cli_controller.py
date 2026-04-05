import argparse
import sys

from facade.pipeline_facade import PipelineFacade
from repository.firestore_repository import FirestoreRepository
from view.cli_view import CLIView


class CLIController:
    """Controller — parses CLI arguments and routes commands.

    Implements the C of MVC: receives user input, delegates work to the
    PipelineFacade or Repository, then hands results to CLIView for display.
    """

    def __init__(self):
        self._view = CLIView()
        self._facade: PipelineFacade = None   # lazy init — avoids token check at import
        self._repo: FirestoreRepository = None  # lazy init

    # ------------------------------------------------------------------
    # Lazy accessors
    # ------------------------------------------------------------------

    def _get_facade(self) -> PipelineFacade:
        if self._facade is None:
            self._facade = PipelineFacade()
        return self._facade

    def _get_repo(self) -> FirestoreRepository:
        if self._repo is None:
            self._repo = FirestoreRepository()
        return self._repo

    # ------------------------------------------------------------------
    # Command handlers
    # ------------------------------------------------------------------

    def _cmd_process(self, args: argparse.Namespace) -> None:
        """Handle the ``process`` command."""
        if args.pdf:
            source_type = "pdf"
            source = args.pdf
        elif args.text:
            source_type = "text"
            source = args.text
        elif not sys.stdin.isatty():
            # Support piped input:  echo "abstract..." | python main.py process
            source_type = "text"
            source = sys.stdin.read()
        else:
            self._view.display_error(
                "Provide input via --text 'paper text...' or --pdf path/to/file.pdf"
            )
            sys.exit(1)

        title = args.title or ""
        self._view.display_header(title)

        try:
            facade = self._get_facade()
            paper, summary, extraction = facade.process(source_type, source, title)
            self._view.display_paper_info(paper)
            self._view.display_summary(summary)
            self._view.display_extraction(extraction)
            self._view.display_footer(summary.model_name)
        except Exception as exc:
            self._view.display_error(str(exc))
            sys.exit(1)

    def _cmd_list(self, args: argparse.Namespace) -> None:
        """Handle the ``list`` command — shows previously processed papers."""
        try:
            papers = self._get_repo().list_papers(limit=args.limit)
            self._view.display_papers_list(papers)
        except Exception as exc:
            self._view.display_error(str(exc))
            sys.exit(1)

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def run(self) -> None:
        parser = argparse.ArgumentParser(
            prog="scholarlens",
            description="ScholarLens — Research Paper Analysis Tool",
        )
        subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
        subparsers.required = True

        # --- process ---
        process_p = subparsers.add_parser(
            "process",
            help="Summarize and extract structured data from a research paper.",
        )
        input_group = process_p.add_mutually_exclusive_group()
        input_group.add_argument(
            "--text", "-t",
            metavar="TEXT",
            help="Raw paper text (wrap in quotes).",
        )
        input_group.add_argument(
            "--pdf", "-p",
            metavar="FILE",
            help="Path to a PDF file.",
        )
        process_p.add_argument(
            "--title",
            metavar="TITLE",
            default="",
            help="Optional paper title for display and storage.",
        )

        # --- list ---
        list_p = subparsers.add_parser(
            "list",
            help="List previously processed papers stored in the database.",
        )
        list_p.add_argument(
            "--limit", "-n",
            type=int,
            default=20,
            metavar="N",
            help="Maximum number of papers to display (default: 20).",
        )

        args = parser.parse_args()

        if args.command == "process":
            self._cmd_process(args)
        elif args.command == "list":
            self._cmd_list(args)
