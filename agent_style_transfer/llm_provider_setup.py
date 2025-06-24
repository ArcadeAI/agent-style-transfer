"""LLM provider setup and configuration using LangChain model factories."""

from typing import Optional

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables from .env file
load_dotenv()


def get_llm(provider: str, model: Optional[str] = None, temperature: float = 0.7):
    """Get the appropriate LLM instance using LangChain's model factory.

    Args:
        provider: Model provider (openai, anthropic, google_genai)
        model: Model name. If None, will use provider defaults.
        temperature: Model temperature (0.0 to 1.0). Defaults to 0.7.

    Returns:
        ChatModel instance
    """

    # Set default models for each provider if not specified
    if model is None:
        default_models = {
            "openai": "gpt-3.5-turbo",
            "anthropic": "claude-3-haiku-20240307",
            "google_genai": "gemini-1.5-flash",
        }
        model = default_models.get(provider)

    # Use LangChain's model factory with automatic provider inference
    # The factory will handle API key loading automatically from environment variables
    return init_chat_model(
        model=model, model_provider=provider, temperature=temperature
    )
