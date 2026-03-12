# ScholarLens

A lightweight command-line tool that ingests research abstracts or full-text papers and produces structured, skimmable outputs — including concise summaries, key contributions, dataset and method mentions, and extracted citation lists.

The focus is on a clean, demonstrable software architecture: the app orchestrates a document-parsing pipeline, calls an LLM for summarization and information extraction, and persists inputs, outputs, and metadata in a cloud database for full traceability.

---

## Target Audience

- Students and researchers who need quick overviews of papers
- Educators compiling course notes from multiple sources
- Analysts who need structured, skimmable insights from technical documents

---

## Features

### Core (Initial Scope)

| # | Feature | Input | Output |
|---|---------|-------|--------|
| 1 | **Summarize Paper Content** | Raw text (pasted), PDF path, or URL *(stretch)* | Short summary + bullet list of key contributions — printed to CLI and stored in cloud DB |
| 2 | **Extract Structured Elements** | Paper text | Dataset mentions, method/model names, and reference list (citations) — persisted in cloud DB for retrieval and audit |

### Optional (Time-Permitting)

- Compare two papers (differences in contributions)
- Export a plain-text "report" artifact
- Simple search over previously processed papers

> All outputs are minimal text tables / bullet points in the CLI to keep scope tight.

---

## Architecture & Design Patterns

ScholarLens follows the **MVC** architectural pattern combined with the following GoF design patterns:

| Pattern | Category | Role in ScholarLens |
|---------|----------|----------------------|
| **Facade** | Structural | Pipeline Orchestrator — single entry point that coordinates parsing, LLM calls, and persistence |
| **Adapter** | Structural | Document & Model Providers — normalises different input formats and LLM providers behind a uniform interface |
| **Factory Method** | Creational | Provider Selection — instantiates the correct document parser or LLM adapter at runtime |

### MVC Breakdown

| Layer | Component |
|-------|-----------|
| **Model** | Domain objects: `Paper`, `Summary`, `Citation`, `ExtractionResult` |
| **View** | CLI (formatted text output to stdout) |
| **Controller** | Routes CLI commands to the Facade / Command objects |

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11 |
| Cloud Database | Google Cloud Firestore |
| LLM API | OpenAI API or Hugging Face Inference API |
| Interface | Command-line (Python) |

---

## Getting Started

### Prerequisites

- Python 3.11+
- A Google Cloud project with Firestore enabled
- A `serviceAccount.json` key file placed in the project root
- An OpenAI or Hugging Face API key

### Installation

```bash
# Clone the repository
git clone https://github.com/PrinceDuru/scholarlens.git
cd scholarlens

# Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirement.txt
```

### Configuration

Place your Firestore service account key file at the project root:

```
scholarlens/
└── serviceAccount.json   ← your Firebase/GCP service account key
```

Set your LLM API key as an environment variable:

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# or Hugging Face
export HF_API_TOKEN="hf_..."
```

### Usage

```bash
# Summarize a paper by pasting raw text
python main.py summarize --text "Paste your abstract or full text here..."

# Summarize from a local PDF
python main.py summarize --pdf path/to/paper.pdf

# Extract structured elements (datasets, methods, citations)
python main.py extract --pdf path/to/paper.pdf
```

---

## Project Structure

```
scholarlens/
├── serviceAccount.json       # GCP service account key (not committed)
├── requirement.txt           # Python dependencies
├── test_firestore_db.py      # Firestore connectivity smoke test
└── README.md
```

> Additional modules (pipeline, adapters, CLI controller, domain models) will be added in upcoming milestones.

---

## Milestones

| Milestone | Status | Description |
|-----------|--------|-------------|
| Milestone 1 | ✅ Complete | Project Proposal — architecture design, technology selection, pattern identification |
| Milestone 2 | 🔄 In Progress | Core implementation |

---


## License

This project is for academic/educational purposes.
