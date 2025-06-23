"""LLM provider setup and configuration."""

import os

from langchain_anthropic import ChatAnthropic
from langchain_community.llms import HuggingFaceHub
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


def get_api_key(provider: str) -> str:
    """Get the appropriate API key for the given provider."""
    api_keys = {
        "huggingface": "HUGGINGFACE_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY",
    }

    env_var = api_keys.get(provider, "HUGGINGFACE_API_KEY")
    api_key = os.environ.get(env_var)

    if not api_key:
        raise ValueError(
            f"{env_var} environment variable is required for {provider} provider"
        )

    return api_key

# TODO: Use langgraph to get the llm and possible set the model and temperature
def get_llm(provider: str):
    """Get the appropriate LLM instance for the given provider."""
    api_key = get_api_key(provider)

    if provider == "huggingface":
        return HuggingFaceHub(
            repo_id="meta-llama/Meta-Llama-3-8B",
            huggingfacehub_api_token=api_key,
            temperature=0.7,
        )

    elif provider == "openai":
        return ChatOpenAI(
            api_key=api_key,
            model="gpt-3.5-turbo",
            temperature=0.7,
        )

    elif provider == "anthropic":
        return ChatAnthropic(
            api_key=api_key,
            model="claude-3-sonnet-20240229",
            temperature=0.7,
        )

    elif provider == "google":
        return ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model="gemini-pro",
            temperature=0.7,
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}")
