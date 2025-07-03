#!/usr/bin/env python3
"""Test LLM provider setup with real API keys."""

import pytest

from agent_style_transfer.llm_provider_setup import get_llm


@pytest.mark.integration
def test_get_llm_openai():
    """Test OpenAI LLM creation."""
    llm = get_llm("openai", "gpt-3.5-turbo")
    assert llm is not None
    assert hasattr(llm, "invoke")


@pytest.mark.integration
def test_get_llm_anthropic():
    """Test Anthropic LLM creation."""
    llm = get_llm("anthropic", "claude-3-haiku-20240307")
    assert llm is not None
    assert hasattr(llm, "invoke")


@pytest.mark.integration
def test_get_llm_google_genai():
    """Test Google GenAI LLM creation."""
    llm = get_llm("google_genai", "gemini-1.5-flash")
    assert llm is not None
    assert hasattr(llm, "invoke")


@pytest.mark.integration
def test_get_llm_default_models():
    """Test LLM creation with default models."""
    providers = ["openai", "anthropic", "google_genai"]

    for provider in providers:
        llm = get_llm(provider)  # No model specified, should use defaults
        assert llm is not None
        assert hasattr(llm, "invoke")


@pytest.mark.integration
def test_get_llm_with_temperature():
    """Test LLM creation with custom temperature."""
    llm = get_llm("openai", "gpt-3.5-turbo", temperature=0.1)
    assert llm is not None
    assert hasattr(llm, "invoke")
