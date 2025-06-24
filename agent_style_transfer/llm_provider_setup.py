"""LLM provider setup and configuration."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


def get_api_key(provider: str) -> str:
    """Get the appropriate API key for the given provider."""
    api_keys = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY",
    }

    env_var = api_keys.get(provider, "OPENAI_API_KEY")
    api_key = os.environ.get(env_var)

    if not api_key:
        raise ValueError(
            f"{env_var} environment variable is required for {provider} provider"
        )

    return api_key


# TODO: Use langgraph to get the llm and possible set the model and temperature
def get_llm(provider: str, model: str = None):
    """Get the appropriate LLM instance for the given provider."""
    api_key = get_api_key(provider)

    if provider == "openai":
        # Use specified model or default to cost-effective option
        if model is None:
            model = "gpt-3.5-turbo"  # More cost-effective than gpt-4o-mini
        
        return ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=0.7,
        )

    elif provider == "anthropic":
        # Use specified model or default to cost-effective option
        if model is None:
            model = "claude-3-haiku-20240307"  # More cost-effective than sonnet
        
        return ChatAnthropic(
            api_key=api_key,
            model=model,
            temperature=0.7,
        )

    elif provider == "google":
        # Use specified model or default to cost-effective option
        if model is None:
            model = "gemini-1.5-flash"  # More cost-effective than pro
        
        return ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model,
            temperature=0.7,
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}. Supported providers: openai, anthropic, google")
