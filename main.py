"""
ScholarLens — entry point.

Usage examples:
    python main.py process --text "Abstract: ..." --title "My Paper"
    python main.py process --pdf path/to/paper.pdf --title "My Paper"
    python main.py list
    python main.py list --limit 5
    echo "paper text..." | python main.py process
"""
from controller.cli_controller import CLIController


def main() -> None:
    controller = CLIController()
    controller.run()


if __name__ == "__main__":
    main()
