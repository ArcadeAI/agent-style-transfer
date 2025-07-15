#!/usr/bin/env python3
"""Unit tests for evaluators using VCR for API call recording."""

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
from tests.conftest import load_fixture

@pytest.mark.vcr
def test_style_fidelity_evaluation():
    request = load_fixture("tweet-request", model=StyleTransferRequest)
    response = load_fixture("tweet-response", model=StyleTransferResponse)
    response.output_schema = request.target_schemas[0]
    result = evaluate_style_fidelity(
        request, response, "anthropic", "claude-3-haiku-20240307"
    )
    assert isinstance(result, dict)
    assert result["key"] == "style_fidelity"
    assert isinstance(result["score"], int | float)
    assert 1 <= result["score"] <= 5
    assert isinstance(result["comment"], str)
    assert len(result["comment"]) > 0

@pytest.mark.vcr
def test_content_preservation_evaluation():
    request = load_fixture("tweet-request", model=StyleTransferRequest)
    response = load_fixture("tweet-response", model=StyleTransferResponse)
    response.output_schema = request.target_schemas[0]
    result = evaluate_content_preservation(request, response)
    assert isinstance(result, dict)
    assert result["key"] == "content_preservation"
    assert isinstance(result["score"], int | float)
    assert 0 <= result["score"] <= 5
    assert isinstance(result["comment"], str)

@pytest.mark.vcr
def test_quality_evaluation():
    request = load_fixture("tweet-request", model=StyleTransferRequest)
    response = load_fixture("tweet-response", model=StyleTransferResponse)
    response.output_schema = request.target_schemas[0]
    result = evaluate_quality(request, response, "anthropic", "claude-3-haiku-20240307")
    assert isinstance(result, dict)
    assert result["key"] == "content_quality"
    assert isinstance(result["score"], int | float)
    assert 1 <= result["score"] <= 5
    assert isinstance(result["comment"], str)
    assert len(result["comment"]) > 0

@pytest.mark.vcr
def test_platform_appropriateness_evaluation():
    request = load_fixture("tweet-request", model=StyleTransferRequest)
    response = load_fixture("tweet-response", model=StyleTransferResponse)
    response.output_schema = request.target_schemas[0]
    result = evaluate_platform_appropriateness(
        request, response, "anthropic", "claude-3-haiku-20240307"
    )
    assert isinstance(result, dict)
    assert result["key"] == "platform_appropriateness"
    assert isinstance(result["score"], int | float)
    assert 1 <= result["score"] <= 5
    assert isinstance(result["comment"], str)
    assert len(result["comment"]) > 0

@pytest.mark.vcr
def test_evaluate_all():
    request = load_fixture("tweet-request", model=StyleTransferRequest)
    response = load_fixture("tweet-response", model=StyleTransferResponse)
    response.output_schema = request.target_schemas[0]
    results = evaluate_all(request, response, "anthropic", "claude-3-haiku-20240307")
    assert isinstance(results, list)
    assert len(results) == 4
    evaluation_keys = {result["key"] for result in results}
    expected_keys = {
        "style_fidelity",
        "content_preservation",
        "content_quality",
        "platform_appropriateness",
    }
    assert evaluation_keys == expected_keys
    for result in results:
        assert isinstance(result, dict)
        assert "key" in result
        assert "score" in result
        assert "comment" in result
        assert isinstance(result["score"], int | float)
        assert isinstance(result["comment"], str)

@pytest.mark.vcr
def test_evaluate_batch():
    request = load_fixture("tweet-request", model=StyleTransferRequest)
    response1 = load_fixture("tweet-response", model=StyleTransferResponse)
    response1.output_schema = request.target_schemas[0]
    response2 = load_fixture("tweet-2-response", model=StyleTransferResponse)
    response2.output_schema = request.target_schemas[0]
    responses = [response1, response2]
    batch_results = evaluate_batch(
        request, responses, "anthropic", "claude-3-haiku-20240307"
    )
    assert isinstance(batch_results, list)
    assert len(batch_results) == 2
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
    request = load_fixture("linkedin-request", model=StyleTransferRequest)
    response = load_fixture("linkedin-response", model=StyleTransferResponse)
    response.output_schema = request.target_schemas[0]
    results = evaluate_all(request, response, "anthropic", "claude-3-haiku-20240307")
    assert len(results) == 4
    for result in results:
        assert isinstance(result["score"], int | float)
        assert result["score"] >= 0

@pytest.mark.vcr
def test_multi_platform_evaluation():
    request = load_fixture("tweet-and-blog-request", model=StyleTransferRequest)
    response = load_fixture("tweet-and-blog-response", model=StyleTransferResponse)
    response.output_schema = request.target_schemas[0]
    results = evaluate_all(request, response, "anthropic", "claude-3-haiku-20240307")
    assert len(results) == 4
    for result in results:
        assert isinstance(result["score"], int | float)
        assert result["score"] >= 0

@pytest.mark.vcr
def test_evaluation_without_api_calls():
    request = load_fixture("tweet-request", model=StyleTransferRequest)
    response = load_fixture("tweet-response", model=StyleTransferResponse)
    response.output_schema = request.target_schemas[0]
    result = evaluate_content_preservation(request, response)
    assert isinstance(result, dict)
    assert result["key"] == "content_preservation"
    assert isinstance(result["score"], int | float)
    assert 0 <= result["score"] <= 5
    assert isinstance(result["comment"], str)
