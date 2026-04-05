import os
import json
import requests
from dotenv import load_dotenv

from .base_llm_adapter import BaseLLMAdapter

load_dotenv()

_MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
_API_URL = "https://router.huggingface.co/v1/chat/completions"

_SYSTEM_PROMPT = (
    "You are a research assistant specializing in academic papers. "
    "Be concise and structured in your responses."
)

_USER_PROMPTS = {
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


class HuggingFaceLLMAdapter(BaseLLMAdapter):
    """Adapter that routes LLM calls through the HuggingFace Inference Router."""

    def __init__(self, model_id: str = _MODEL_ID):
        self._model_id = model_id
        token = os.environ.get("HF_TOKEN")
        if not token:
            raise EnvironmentError(
                "HF_TOKEN is not set. "
                "Add it to your .env file or set the environment variable."
            )
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    @property
    def model_name(self) -> str:
        return self._model_id

    def call(self, task: str, text: str, max_tokens: int = 400) -> str:
        if task not in _USER_PROMPTS:
            raise ValueError(
                f"Unknown task '{task}'. Valid tasks: {list(_USER_PROMPTS)}"
            )

        messages = [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": _USER_PROMPTS[task].format(text=text.strip())},
        ]
        payload = {
            "model": self._model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }

        response = requests.post(
            _API_URL, headers=self._headers, json=payload, timeout=120
        )
        response.raise_for_status()

        result = response.json()
        try:
            return result["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError):
            return json.dumps(result, indent=2)
