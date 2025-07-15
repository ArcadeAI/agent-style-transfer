#!/usr/bin/env python3
"""Unit tests for style inference evaluation functions."""

import pytest

from agent_style_transfer.evals import (
    evaluate_style_inference_accuracy,
    evaluate_style_rule_usefulness,
)
from agent_style_transfer.schemas import (
    StyleTransferRequest,
    StyleTransferResponse,
)
from tests.conftest import load_fixture


@pytest.mark.vcr
def test_evaluate_style_inference_accuracy():
    """Test style inference accuracy evaluation."""
    request = load_fixture("document-based-request", model=StyleTransferRequest)
    response = load_fixture("tweet-response", model=StyleTransferResponse)
    response.output_schema = request.target_schemas[0]

    result = evaluate_style_inference_accuracy(request, response, provider="anthropic")

    assert isinstance(result, dict)
    assert "key" in result
    assert "score" in result
    assert "comment" in result
    assert result["key"] == "style_inference_accuracy"
    assert isinstance(result["score"], (int, float))
    assert 0 <= result["score"] <= 5
    assert isinstance(result["comment"], str)


@pytest.mark.vcr
def test_evaluate_style_rule_usefulness():
    """Test style rule usefulness evaluation."""
    request = load_fixture("document-based-request", model=StyleTransferRequest)
    response = load_fixture("tweet-response", model=StyleTransferResponse)
    response.output_schema = request.target_schemas[0]

    result = evaluate_style_rule_usefulness(request, response, provider="anthropic")

    assert isinstance(result, dict)
    assert "key" in result
    assert "score" in result
    assert "comment" in result
    assert result["key"] == "style_rule_usefulness"
    assert isinstance(result["score"], (int, float))
    assert 0 <= result["score"] <= 5
    assert isinstance(result["comment"], str)


def test_evaluate_style_inference_accuracy_no_reference_docs():
    """Test style inference accuracy evaluation with no reference documents."""
    # Use tweet-request fixture which has style definitions but no documents
    request = load_fixture("tweet-request", model=StyleTransferRequest)

    response = StyleTransferResponse(
        processed_content='{"text": "Test response"}',
        applied_style="Tech Influencer Style",
        output_schema=request.target_schemas[0],
        metadata={},
    )

    result = evaluate_style_inference_accuracy(request, response)

    assert isinstance(result, dict)
    assert result["key"] == "style_inference_accuracy"
    assert result["score"] == 0
    assert "No reference documents available" in result["comment"]


def test_evaluate_style_rule_usefulness_no_reference_docs():
    """Test style rule usefulness evaluation with no reference documents."""
    # Use tweet-request fixture which has style definitions but no documents
    request = load_fixture("tweet-request", model=StyleTransferRequest)

    response = StyleTransferResponse(
        processed_content='{"text": "Test response"}',
        applied_style="Tech Influencer Style",
        output_schema=request.target_schemas[0],
        metadata={},
    )

    result = evaluate_style_rule_usefulness(request, response)

    assert isinstance(result, dict)
    assert result["key"] == "style_rule_usefulness"
    assert result["score"] == 0
    assert "No reference documents available" in result["comment"]


@pytest.mark.vcr
def test_evaluate_style_inference_accuracy_with_linkedin_documents():
    """Test style inference accuracy evaluation with LinkedIn-style documents."""
    request = load_fixture("linkedin-request", model=StyleTransferRequest)
    response = load_fixture("linkedin-response", model=StyleTransferResponse)
    response.output_schema = request.target_schemas[0]

    result = evaluate_style_inference_accuracy(request, response, provider="anthropic")

    assert isinstance(result, dict)
    assert result["key"] == "style_inference_accuracy"
    assert isinstance(result["score"], (int, float))
    assert 0 <= result["score"] <= 5


@pytest.mark.vcr
def test_evaluate_style_rule_usefulness_with_linkedin_documents():
    """Test style rule usefulness evaluation with LinkedIn-style documents."""
    request = load_fixture("linkedin-request", model=StyleTransferRequest)
    response = load_fixture("linkedin-response", model=StyleTransferResponse)
    response.output_schema = request.target_schemas[0]

    result = evaluate_style_rule_usefulness(request, response, provider="anthropic")

    assert isinstance(result, dict)
    assert result["key"] == "style_rule_usefulness"
    assert isinstance(result["score"], (int, float))
    assert 0 <= result["score"] <= 5


def test_evaluate_style_inference_accuracy_empty_documents():
    """Test style inference accuracy evaluation with empty document content."""
    # Use document-based-request fixture but modify it to have empty content
    request = load_fixture("document-based-request", model=StyleTransferRequest)

    # Clear the content from all documents to test empty content handling
    if request.reference_style[0].documents:
        for doc in request.reference_style[0].documents:
            doc.content = None

    response = StyleTransferResponse(
        processed_content='{"text": "Test response"}',
        applied_style="Tech Influencer Style",
        output_schema=request.target_schemas[0],
        metadata={},
    )

    result = evaluate_style_inference_accuracy(request, response)

    assert isinstance(result, dict)
    assert result["key"] == "style_inference_accuracy"
    assert result["score"] == 0
    assert "No reference documents available" in result["comment"]
