from adapters.base_llm_adapter import BaseLLMAdapter
from adapters.huggingface_llm_adapter import HuggingFaceLLMAdapter


class LLMProviderFactory:
    """Factory Method — instantiates the correct LLM adapter at runtime."""

    @staticmethod
    def create(provider: str = "huggingface") -> BaseLLMAdapter:
        """Return the appropriate LLM adapter for *provider*.

        Args:
            provider: The LLM provider identifier. Currently supported:
                ``"huggingface"``.

        Returns:
            A concrete :class:`BaseLLMAdapter` instance.

        Raises:
            ValueError: If *provider* is not supported.
        """
        normalised = provider.lower().strip()
        if normalised == "huggingface":
            return HuggingFaceLLMAdapter()
        raise ValueError(
            f"Unsupported LLM provider '{provider}'. "
            "Supported providers: 'huggingface'."
        )
