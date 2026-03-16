import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    raise EnvironmentError("HF_TOKEN is not set. Add it to a .env file or set the environment variable.")
MODEL_ID  = "Qwen/Qwen2.5-7B-Instruct"   # routed to Qwen2.5-7B-Instruct-Turbo
API_URL   = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json",
}

# ---------------------------------------------------------------------------
# Sample research abstract used for demonstration
# ---------------------------------------------------------------------------
SAMPLE_ABSTRACT = """
Title: Attention Is All You Need

Abstract:
We propose a new simple network architecture, the Transformer, based solely on
attention mechanisms, dispensing with recurrence and convolutions entirely.
Experiments on two machine translation tasks show these models to be superior
in quality while being more parallelizable and requiring significantly less time
to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German
translation task, improving over the existing best results, including ensembles,
by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model
establishes a new single-model state-of-the-art BLEU score of 41.8 after
training for 3.5 days on eight GPUs, a small fraction of the training costs of
the best models from the literature. We show that the Transformer generalizes
well to other tasks by applying it successfully to English constituency parsing
with both large and limited training data.

Datasets: WMT 2014 English-German, WMT 2014 English-French, Penn Treebank (WSJ)
Methods: Transformer, Multi-Head Attention, Positional Encoding,
         Scaled Dot-Product Attention, Feed-Forward Networks

References:
[1] Bahdanau et al., 2014 – Neural Machine Translation by Jointly Learning
    to Align and Translate
[2] Hochreiter & Schmidhuber, 1997 – Long Short-Term Memory
[3] LeCun et al., 1998 – Gradient-Based Learning Applied to Document Recognition
[4] Vinyals & Kaiser et al., 2015 – Grammar as a Foreign Language
"""

# ---------------------------------------------------------------------------
# Prompt builder  (OpenAI-compatible chat messages format)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are a research assistant specializing in academic papers. "
    "Be concise and structured in your responses."
)

USER_PROMPTS = {
    "summarize": (
        "Summarize the following research paper in 2-3 concise sentences, "
        "capturing the core contribution and main result:\n\n{text}"
    ),
    "contributions": (
        "List the key contributions of the following research paper as concise "
        "bullet points (use '- ' prefix for each bullet):\n\n{text}"
    ),
    "datasets_methods": (
        "Extract all dataset names and method/model names mentioned in the "
        "following research paper text. Return the result in exactly this format:\n"
        "Datasets: <comma-separated list>\n"
        "Methods:  <comma-separated list>\n\n{text}"
    ),
    "citations": (
        "Extract every citation and reference entry from the following research "
        "paper text. List each one on its own line with a leading number or "
        "bullet:\n\n{text}"
    ),
}


def build_messages(task: str, text: str) -> list:
    """Return the chat messages list for a given ScholarLens task."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": USER_PROMPTS[task].format(text=text.strip())},
    ]


def call_llm(task: str, text: str, max_tokens: int = 400) -> str:
    """
    POST a chat-completion request to the HuggingFace Inference Router.
    Returns the assistant reply string, or raises on HTTP error.
    """
    payload = {
        "model": MODEL_ID,
        "messages": build_messages(task, text),
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=120)
    response.raise_for_status()

    result = response.json()
    
    try:
        return result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# ScholarLens pipeline
# ---------------------------------------------------------------------------
TASKS = [
    ("summarize",         "SUMMARY"),
    ("contributions",     "KEY CONTRIBUTIONS"),
    ("datasets_methods",  "DATASETS & METHODS"),
    ("citations",         "CITATIONS"),
]


def run_scholarlens_pipeline(text: str) -> None:
    """Run all four ScholarLens extraction tasks and print structured output."""
    print("=" * 62)
    print("           SCHOLARLENS - PAPER ANALYSIS")
    print(f"           Model: {MODEL_ID}")
    print("=" * 62)

    for task_key, label in TASKS:
        print("\n" + "-" * 62)
        print(f"  {label}")
        print("-" * 62)
        output = call_llm(task_key, text)
        print(output)

    print("\n" + "=" * 62)


if __name__ == "__main__":
    run_scholarlens_pipeline(SAMPLE_ABSTRACT)

