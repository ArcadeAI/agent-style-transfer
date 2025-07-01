#!/usr/bin/env python3
"""Unit tests for evaluators using VCR for API call recording."""

import json

import pytest
from pydantic import ValidationError

from agent_style_transfer.evals import (
    evaluate_all,
    evaluate_batch,
    evaluate_content_preservation,
    evaluate_platform_appropriateness,
    evaluate_quality,
    evaluate_style_fidelity,
)
from agent_style_transfer.schemas import (
    StyleTransferRequest,
    StyleTransferResponse,
)


@pytest.fixture(scope="session")
def vcr_config() -> dict:
    """Configure VCR for recording HTTP interactions."""
    return {
        "cassette_library_dir": "tests/cassettes",
        "record_mode": "once",
        "filter_headers": ["authorization", "x-api-key"],
    }


def load_request(fixture_name: str) -> StyleTransferRequest:
    """Load a StyleTransferRequest from a JSON fixture file."""
    with open(f"fixtures/{fixture_name}-request.json") as f:
        request_data = json.load(f)
    return StyleTransferRequest(**request_data)


def load_response(fixture_name: str, request: StyleTransferRequest = None) -> StyleTransferResponse:
    """Load a StyleTransferResponse from a JSON fixture file."""
    with open(f"fixtures/{fixture_name}-response.json") as f:
        response_data = json.load(f)
    # Use the first response from the responses array
    response_obj = response_data["responses"][0]
    
    # Handle output_schema field - it might be a string that needs to be matched with the request
    if "output_schema" in response_obj and isinstance(response_obj["output_schema"], str):
        schema_name = response_obj["output_schema"]
        output_schema = None
        if request:
            # Try to find matching output schema from original request
            for schema in request.target_schemas:
                if schema.name == schema_name:
                    output_schema = schema
                    break
        # If no match found or no request provided, set to None
        response_obj["output_schema"] = output_schema
    
    return StyleTransferResponse(**response_obj)


@pytest.mark.vcr
def test_style_fidelity_evaluation():
    """Test style fidelity evaluation with VCR recording."""
    request = load_request("tweet")
    response = load_response("tweet", request)
    
    result = evaluate_style_fidelity(request, response, "claude-3-haiku-20240307")

    assert isinstance(result, dict)
    assert result["key"] == "style_fidelity"
    assert isinstance(result["score"], (int, float))
    assert 1 <= result["score"] <= 5
    assert isinstance(result["comment"], str)
    assert len(result["comment"]) > 0


@pytest.mark.vcr
def test_content_preservation_evaluation():
    """Test content preservation evaluation with VCR recording."""
    request = load_request("tweet")
    response = load_response("tweet", request)
    
    result = evaluate_content_preservation(request, response)

    assert isinstance(result, dict)
    assert result["key"] == "content_preservation"
    assert isinstance(result["score"], (int, float))
    assert 0 <= result["score"] <= 1  # Embedding similarity is typically 0-1
    assert isinstance(result["comment"], str)


@pytest.mark.vcr
def test_quality_evaluation():
    """Test content quality evaluation with VCR recording."""
    request = load_request("tweet")
    response = load_response("tweet", request)
    
    result = evaluate_quality(request, response, "claude-3-haiku-20240307")

    assert isinstance(result, dict)
    assert result["key"] == "content_quality"
    assert isinstance(result["score"], (int, float))
    assert 1 <= result["score"] <= 5
    assert isinstance(result["comment"], str)
    assert len(result["comment"]) > 0


@pytest.mark.vcr
def test_platform_appropriateness_evaluation():
    """Test platform appropriateness evaluation with VCR recording."""
    request = load_request("tweet")
    response = load_response("tweet", request)
    
    result = evaluate_platform_appropriateness(request, response, "claude-3-haiku-20240307")

    assert isinstance(result, dict)
    assert result["key"] == "platform_appropriateness"
    assert isinstance(result["score"], (int, float))
    assert 1 <= result["score"] <= 5
    assert isinstance(result["comment"], str)
    assert len(result["comment"]) > 0


@pytest.mark.vcr
def test_evaluate_all():
    """Test running all evaluations together with VCR recording."""
    request = load_request("tweet")
    response = load_response("tweet", request)
    
    results = evaluate_all(request, response, "claude-3-haiku-20240307")

    assert isinstance(results, list)
    assert len(results) == 4

    # Check that all expected evaluation types are present
    evaluation_keys = {result["key"] for result in results}
    expected_keys = {
        "style_fidelity",
        "content_preservation",
        "content_quality",
        "platform_appropriateness",
    }
    assert evaluation_keys == expected_keys

    # Check each result has proper structure
    for result in results:
        assert isinstance(result, dict)
        assert "key" in result
        assert "score" in result
        assert "comment" in result
        assert isinstance(result["score"], (int, float))
        assert isinstance(result["comment"], str)


@pytest.mark.vcr
def test_evaluate_batch():
    """Test batch evaluation with multiple responses."""
    request = load_request("tweet")
    response1 = load_response("tweet", request)
    response2 = load_response("tweet-2", request)
    
    responses = [response1, response2]
    batch_results = evaluate_batch(request, responses, "claude-3-haiku-20240307")

    assert isinstance(batch_results, list)
    assert len(batch_results) == 2

    # Check each response has all evaluations
    for response_results in batch_results:
        assert isinstance(response_results, list)
        assert len(response_results) == 4

        evaluation_keys = {result["key"] for result in response_results}
        expected_keys = {
            "style_fidelity",
            "content_preservation",
            "content_quality",
            "platform_appropriateness",
        }
        assert evaluation_keys == expected_keys


@pytest.mark.vcr
def test_linkedin_post_evaluation():
    """Test evaluation with LinkedIn post content."""
    request = load_request("linkedin")
    response = load_response("linkedin", request)
    
    results = evaluate_all(request, response, "claude-3-haiku-20240307")

    assert len(results) == 4
    for result in results:
        assert isinstance(result["score"], (int, float))
        assert result["score"] >= 0


@pytest.mark.vcr
def test_multi_platform_evaluation():
    """Test evaluation with multi-platform content."""
    request = load_request("tweet-and-blog")
    response = load_response("tweet-and-blog", request)
    
    results = evaluate_all(request, response, "claude-3-haiku-20240307")

    assert len(results) == 4
    for result in results:
        assert isinstance(result["score"], (int, float))
        assert result["score"] >= 0


def test_evaluation_error_handling():
    """Test that evaluation functions handle errors gracefully."""
    # Test that creating a malformed request raises ValidationError
    with pytest.raises(ValidationError):
        StyleTransferRequest(
            reference_style=[],
            intent="Test",
            focus="Test",
            target_content=[],
            target_schemas=[],
        )

    # Test evaluation with minimal valid request but broken content
    request = load_request("tweet")

    malformed_response = StyleTransferResponse(
        processed_content="invalid json content",
        applied_style="Test Style",
        output_schema=request.target_schemas[0],
        metadata={},
    )

    # This should handle the JSON parsing error gracefully
    result = evaluate_content_preservation(request, malformed_response)
    assert result["key"] == "content_preservation"
    assert result["score"] == 0
    assert "Evaluation failed" in result["comment"]


def test_evaluation_without_api_calls():
    """Test evaluation functions that don't require API calls."""
    # Content preservation uses embedding similarity which may not require API calls
    # depending on the implementation
    request = load_request("tweet")
    response = load_response("tweet", request)
    
    result = evaluate_content_preservation(request, response)

    assert isinstance(result, dict)
    assert result["key"] == "content_preservation"
    assert isinstance(result["score"], (int, float))
    assert isinstance(result["comment"], str)
