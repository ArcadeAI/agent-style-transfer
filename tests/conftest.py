"""Pytest configuration for evaluator tests."""

import json
import os
from pathlib import Path
from typing import Any

import pytest
from dotenv import load_dotenv

from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, Any]:
    """Configure VCR for recording HTTP interactions."""
    return {
        "cassette_library_dir": "tests/cassettes",
        "record_mode": "new_episodes",
        "filter_headers": [
            "authorization",
            "x-api-key",
            "api-key",
            "x-openai-api-key",
            "x-anthropic-api-key",
            "x-google-api-key",
            "openai-api-key",
            "anthropic-api-key",
            "google-api-key",
            "x-goog-api-key",
        ],
        "filter_query_parameters": [
            "key",
            "api_key",
            "token",
            "access_token",
        ],
        "filter_post_data_parameters": [
            "api_key",
            "key",
            "token",
        ],
        "match_on": ["method", "scheme", "host", "port", "path"],
    }


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment variables from .env file if it exists."""
    # Load .env.test for integration tests - required for tests
    test_env_file = Path(__file__).parent.parent / ".env.test"
    if not test_env_file.exists():
        raise FileNotFoundError(
            f".env.test file not found at {test_env_file}. "
            "Create this file with your test API keys to run integration tests."
        )

    load_dotenv(test_env_file)
    print("Loaded .env.test for integration tests")

    # Set testing environment variable
    os.environ["TESTING"] = "1"


@pytest.fixture(scope="session")
def vcr_cassette_dir() -> str:
    """Directory for VCR cassettes."""
    return "tests/cassettes"


def load_fixture(fixture_name: str, model: type = None) -> dict | StyleTransferRequest | StyleTransferResponse:
    """Load a fixture, returning raw JSON by default or model instance if specified."""
    with open(f"fixtures/{fixture_name}.json") as f:
        data = json.load(f)

    if model is None:
        return data

    # Always extract the first response if present
    if "responses" in data and isinstance(data["responses"], list):
        data = data["responses"][0]

    # Convert string output_schema to None for StyleTransferResponse
    if model == StyleTransferResponse and "output_schema" in data and isinstance(data["output_schema"], str):
        data["output_schema"] = None

    return model(**data)
