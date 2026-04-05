from abc import ABC, abstractmethod


class BaseLLMAdapter(ABC):
    """Abstract adapter — normalises calls to different external LLM providers."""

    @abstractmethod
    def call(self, task: str, text: str) -> str:
        """Send a task-specific prompt with *text* to the LLM and return the response."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the identifier string of the underlying model."""
