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


@pytest.fixture
def single_tech_tweet_request() -> StyleTransferRequest:
    """Load the single tech tweet example request."""
    with open("fixtures/tweet-request.json") as f:
        request_data = json.load(f)
    return StyleTransferRequest(**request_data)


@pytest.fixture
def single_tech_tweet_response(single_tech_tweet_request) -> StyleTransferResponse:
    """Create a realistic response for the single tech tweet example."""
    response = StyleTransferResponse(
        processed_content=json.dumps(
            {
                "text": "Dive into #MachineLearning basics with this beginner-friendly guide for devs! 🧠 Learn the essentials of AI and programming in just 2500 words. 👨‍💻 #TechTips #DevLife",
                "url_allowed": True,
            }
        ),
        applied_style="Tech Influencer Style",
        output_schema=single_tech_tweet_request.target_schemas[0],
        metadata={
            "schema_name": "Twitter Single Post",
            "reference_styles_count": 1,
            "target_documents_count": 1,
        },
    )
    return response


@pytest.fixture
def linkedin_request() -> StyleTransferRequest:
    """Load the LinkedIn fullstack skills example request."""
    with open("fixtures/linkedin-request.json") as f:
        request_data = json.load(f)
    return StyleTransferRequest(**request_data)


@pytest.fixture
def linkedin_response(linkedin_request) -> StyleTransferResponse:
    """Create a realistic response for the LinkedIn example."""
    response = StyleTransferResponse(
        processed_content=json.dumps(
            {
                "text": "I'm excited to share insights from our analysis of 50,000+ job postings. The demand for full-stack developers continues to grow, with React, Node.js, and cloud skills leading the way. Here's what employers are actually looking for in 2024."
            }
        ),
        applied_style="LinkedIn Tech Thought Leader",
        output_schema=linkedin_request.target_schemas[0],
        metadata={
            "schema_name": "LinkedIn Professional Post",
            "reference_styles_count": 1,
            "target_documents_count": 1,
        },
    )
    return response


@pytest.fixture
def multi_platform_request() -> StyleTransferRequest:
    """Load the multi-platform content example request."""
    with open("fixtures/tweet-and-blog-request.json") as f:
        request_data = json.load(f)
    return StyleTransferRequest(**request_data)


@pytest.fixture
def multi_platform_response(multi_platform_request) -> StyleTransferResponse:
    """Create a realistic response for the multi-platform example."""
    response = StyleTransferResponse(
        processed_content=json.dumps(
            {
                "text": "🚀 REST API design tips that will save you hours! #APIDesign #BestPractices #DevTips",
                "url_allowed": True,
            }
        ),
        applied_style="Social Media Tech Influencer",
        output_schema=multi_platform_request.target_schemas[0],
        metadata={
            "schema_name": "Engaging Tweet",
            "reference_styles_count": 2,
            "target_documents_count": 2,
        },
    )
    return response


@pytest.mark.vcr
def test_style_fidelity_evaluation(
    single_tech_tweet_request, single_tech_tweet_response
):
    """Test style fidelity evaluation with VCR recording."""
    result = evaluate_style_fidelity(
        single_tech_tweet_request, single_tech_tweet_response, "claude-3-haiku-20240307"
    )

    assert isinstance(result, dict)
    assert result["key"] == "style_fidelity"
    assert isinstance(result["score"], (int, float))

    assert 1 <= result["score"] <= 5
    assert isinstance(result["comment"], str)
    assert len(result["comment"]) > 0


@pytest.mark.vcr
def test_content_preservation_evaluation(
    single_tech_tweet_request, single_tech_tweet_response
):
    """Test content preservation evaluation with VCR recording."""
    result = evaluate_content_preservation(
        single_tech_tweet_request, single_tech_tweet_response
    )

    assert isinstance(result, dict)
    assert result["key"] == "content_preservation"
    assert isinstance(result["score"], (int, float))
    assert 0 <= result["score"] <= 1  # Embedding similarity is typically 0-1
    assert isinstance(result["comment"], str)


@pytest.mark.vcr
def test_quality_evaluation(single_tech_tweet_request, single_tech_tweet_response):
    """Test content quality evaluation with VCR recording."""
    result = evaluate_quality(
        single_tech_tweet_request, single_tech_tweet_response, "claude-3-haiku-20240307"
    )

    assert isinstance(result, dict)
    assert result["key"] == "content_quality"
    assert isinstance(result["score"], (int, float))
    assert 1 <= result["score"] <= 5
    assert isinstance(result["comment"], str)
    assert len(result["comment"]) > 0


@pytest.mark.vcr
def test_platform_appropriateness_evaluation(
    single_tech_tweet_request, single_tech_tweet_response
):
    """Test platform appropriateness evaluation with VCR recording."""
    result = evaluate_platform_appropriateness(
        single_tech_tweet_request, single_tech_tweet_response, "claude-3-haiku-20240307"
    )

    assert isinstance(result, dict)
    assert result["key"] == "platform_appropriateness"
    assert isinstance(result["score"], (int, float))
    assert 1 <= result["score"] <= 5
    assert isinstance(result["comment"], str)
    assert len(result["comment"]) > 0


@pytest.mark.vcr
def test_evaluate_all(single_tech_tweet_request, single_tech_tweet_response):
    """Test running all evaluations together with VCR recording."""
    results = evaluate_all(
        single_tech_tweet_request, single_tech_tweet_response, "claude-3-haiku-20240307"
    )

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
def test_evaluate_batch(single_tech_tweet_request, single_tech_tweet_response):
    """Test batch evaluation with multiple responses."""
    # Create a second response with different content
    second_response = StyleTransferResponse(
        processed_content=json.dumps(
            {
                "text": "Another tech achievement! Deployed new microservices with 50% faster response times. The architecture is solid! 💪 #Microservices #Performance",
                "url_allowed": True,
            }
        ),
        applied_style="Tech Influencer Style",
        output_schema=single_tech_tweet_response.output_schema,
        metadata=single_tech_tweet_response.metadata,
    )

    responses = [single_tech_tweet_response, second_response]
    batch_results = evaluate_batch(
        single_tech_tweet_request, responses, "claude-3-haiku-20240307"
    )

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
def test_linkedin_post_evaluation(linkedin_request, linkedin_response):
    """Test evaluation with LinkedIn post content."""
    results = evaluate_all(
        linkedin_request, linkedin_response, "claude-3-haiku-20240307"
    )

    assert len(results) == 4
    for result in results:
        assert isinstance(result["score"], (int, float))
        assert result["score"] >= 0


@pytest.mark.vcr
def test_multi_platform_evaluation(multi_platform_request, multi_platform_response):
    """Test evaluation with multi-platform content."""
    results = evaluate_all(
        multi_platform_request, multi_platform_response, "claude-3-haiku-20240307"
    )

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
    with open("fixtures/tweet-request.json") as f:
        request_data = json.load(f)
    request = StyleTransferRequest(**request_data)

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


def test_evaluation_without_api_calls(
    single_tech_tweet_request, single_tech_tweet_response
):
    """Test evaluation functions that don't require API calls."""
    # Content preservation uses embedding similarity which may not require API calls
    # depending on the implementation
    result = evaluate_content_preservation(
        single_tech_tweet_request, single_tech_tweet_response
    )

    assert isinstance(result, dict)
    assert result["key"] == "content_preservation"
    assert isinstance(result["score"], (int, float))
    assert isinstance(result["comment"], str)
