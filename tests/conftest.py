"""Pytest configuration for evaluator tests."""

from pathlib import Path
from typing import Any, Dict

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def vcr_config() -> Dict[str, Any]:
    """Configure VCR for recording HTTP interactions."""
    return {
        "cassette_library_dir": "tests/cassettes",
        "record_mode": "once",
        "filter_headers": ["authorization", "x-api-key", "x-goog-api-key"],
        "filter_query_parameters": ["key", "api_key"],
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
    }


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment variables from .env file if it exists."""
    env_file = Path(__file__).parent.parent / ".env"
    load_dotenv(env_file)


@pytest.fixture(scope="session")
def vcr_cassette_dir() -> str:
    """Directory for VCR cassettes."""
    return "tests/cassettes"
