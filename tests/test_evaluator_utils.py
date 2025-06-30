#!/usr/bin/env python3
"""Unit tests for evaluator utility functions."""

import json
from unittest.mock import Mock, patch

from agent_style_transfer.evals import (
    evaluate_content_preservation,
    evaluate_style_fidelity,
)
from agent_style_transfer.schemas import (
    StyleTransferRequest,
    StyleTransferResponse,
)
from agent_style_transfer.utils.evaluation import (
    format_result,
    get_text_content,
    safe_evaluation,
)


def test_format_result():
    """Test the format_result utility function."""
    result = format_result("test_key", 4.5, "Great result!")

    assert result["key"] == "test_key"
    assert result["score"] == 4.5
    assert result["comment"] == "Great result!"


def test_format_result_empty_comment():
    """Test format_result with empty comment."""
    result = format_result("test_key", 3.0, "")

    assert result["key"] == "test_key"
    assert result["score"] == 3.0
    assert result["comment"] == "No comment provided"


def test_get_text_content_with_real_example():
    """Test text content extraction using real example data."""
    # Load real example request
    with open("examples/single-tech-tweet.json") as f:
        request_data = json.load(f)
    request = StyleTransferRequest(**request_data)

    # Create realistic response based on actual agent output
    response = StyleTransferResponse(
        processed_content=json.dumps(
            {
                "text": "Dive into #MachineLearning basics with this beginner-friendly guide for devs! 🧠 Learn the essentials of AI and programming in just 2500 words. 👨‍💻 #TechTips #DevLife",
                "url_allowed": True,
            }
        ),
        applied_style="Tech Influencer Style",
        output_schema=request.target_schemas[0],
        metadata={
            "schema_name": "Twitter Single Post",
            "reference_styles_count": 1,
            "target_documents_count": 1,
        },
    )

    generated_text, original_text = get_text_content(request, response)

    assert (
        generated_text
        == "Dive into #MachineLearning basics with this beginner-friendly guide for devs! 🧠 Learn the essentials of AI and programming in just 2500 words. 👨‍💻 #TechTips #DevLife"
    )
    # The original content would be the blog post content, but it's not in the example
    assert original_text == ""


def test_get_text_content_no_original_content():
    """Test text content extraction when original content is None."""
    # Load real example request
    with open("examples/single-tech-tweet.json") as f:
        request_data = json.load(f)

    # Modify to have no content
    request_data["target_content"][0]["content"] = None
    request = StyleTransferRequest(**request_data)

    response = StyleTransferResponse(
        processed_content=json.dumps(
            {"text": "Generated content here", "url_allowed": True}
        ),
        applied_style="Tech Influencer Style",
        output_schema=request.target_schemas[0],
        metadata={},
    )

    generated_text, original_text = get_text_content(request, response)

    assert generated_text == "Generated content here"
    assert original_text == ""


def test_safe_evaluation_decorator():
    """Test the safe_evaluation decorator."""

    @safe_evaluation("test_eval")
    def failing_function():
        raise ValueError("Test error")

    result = failing_function()

    assert result["key"] == "test_eval"
    assert result["score"] == 0
    assert "Evaluation failed" in result["comment"]
    assert "Test error" in result["comment"]


def test_safe_evaluation_decorator_success():
    """Test the safe_evaluation decorator with successful execution."""

    @safe_evaluation("test_eval")
    def successful_function():
        return {"key": "test_eval", "score": 5.0, "comment": "Success!"}

    result = successful_function()

    assert result["key"] == "test_eval"
    assert result["score"] == 5.0
    assert result["comment"] == "Success!"


@patch(
    "agent_style_transfer.evals.content_preservation.create_embedding_similarity_evaluator"
)
def test_content_preservation_evaluation_mock(mock_evaluator):
    """Test content preservation evaluation with mocked dependencies."""
    # Mock the evaluator
    mock_eval = Mock()
    mock_eval.return_value = {"score": 0.85, "comment": "Good similarity"}
    mock_evaluator.return_value = mock_eval

    # Load real example request
    with open("examples/single-tech-tweet.json") as f:
        request_data = json.load(f)
    request = StyleTransferRequest(**request_data)

    response = StyleTransferResponse(
        processed_content=json.dumps(
            {
                "text": "Dive into #MachineLearning basics with this beginner-friendly guide for devs! 🧠 Learn the essentials of AI and programming in just 2500 words. 👨‍💻 #TechTips #DevLife",
                "url_allowed": True,
            }
        ),
        applied_style="Tech Influencer Style",
        output_schema=request.target_schemas[0],
        metadata={},
    )

    result = evaluate_content_preservation(request, response)

    assert result["key"] == "content_preservation"
    assert result["score"] == 0.85
    assert result["comment"] == "Good similarity"

    # Verify the evaluator was called correctly
    mock_eval.assert_called_once()


@patch("agent_style_transfer.evals.style_fidelity.create_llm_evaluator")
def test_style_fidelity_evaluation_mock(mock_evaluator):
    """Test style fidelity evaluation with mocked dependencies."""
    # Mock the evaluator
    mock_eval = Mock()
    mock_eval.return_value = {"score": 4.0, "comment": "Good style match"}
    mock_evaluator.return_value = mock_eval

    # Load real example request
    with open("examples/single-tech-tweet.json") as f:
        request_data = json.load(f)
    request = StyleTransferRequest(**request_data)

    response = StyleTransferResponse(
        processed_content=json.dumps(
            {
                "text": "Dive into #MachineLearning basics with this beginner-friendly guide for devs! 🧠 Learn the essentials of AI and programming in just 2500 words. 👨‍💻 #TechTips #DevLife",
                "url_allowed": True,
            }
        ),
        applied_style="Tech Influencer Style",
        output_schema=request.target_schemas[0],
        metadata={},
    )

    result = evaluate_style_fidelity(request, response, "openai:o3-mini")

    assert result["key"] == "style_fidelity"
    assert result["score"] == 4.0
    assert result["comment"] == "Good style match"

    # Verify the evaluator was called correctly
    mock_eval.assert_called_once()


def test_evaluation_with_invalid_json():
    """Test evaluation with invalid JSON in processed content."""
    # Load real example request
    with open("examples/single-tech-tweet.json") as f:
        request_data = json.load(f)
    request = StyleTransferRequest(**request_data)

    response = StyleTransferResponse(
        processed_content="invalid json content",  # Invalid JSON
        applied_style="Tech Influencer Style",
        output_schema=request.target_schemas[0],
        metadata={},
    )

    # This should handle the JSON parsing error gracefully
    result = evaluate_content_preservation(request, response)

    assert result["key"] == "content_preservation"
    assert result["score"] == 0
    assert "Evaluation failed" in result["comment"]


def test_evaluation_with_empty_content():
    """Test evaluation with empty content."""
    # Load real example request
    with open("examples/single-tech-tweet.json") as f:
        request_data = json.load(f)
    request = StyleTransferRequest(**request_data)

    response = StyleTransferResponse(
        processed_content=json.dumps(
            {"text": "", "url_allowed": True}  # Empty generated content
        ),
        applied_style="Tech Influencer Style",
        output_schema=request.target_schemas[0],
        metadata={},
    )

    # This should handle empty content gracefully
    result = evaluate_content_preservation(request, response)

    assert result["key"] == "content_preservation"
    assert isinstance(result["score"], (int, float))
    assert isinstance(result["comment"], str)


def test_linkedin_example():
    """Test with LinkedIn example data."""
    # Load LinkedIn example request
    with open("examples/linkedin-fullstack-skills.json") as f:
        request_data = json.load(f)
    request = StyleTransferRequest(**request_data)

    response = StyleTransferResponse(
        processed_content=json.dumps(
            {
                "text": "I'm excited to share insights from our analysis of 50,000+ job postings. The demand for full-stack developers continues to grow, with React, Node.js, and cloud skills leading the way. Here's what employers are actually looking for in 2024."
            }
        ),
        applied_style="LinkedIn Tech Thought Leader",
        output_schema=request.target_schemas[0],
        metadata={
            "schema_name": "LinkedIn Professional Post",
            "reference_styles_count": 1,
            "target_documents_count": 1,
        },
    )

    generated_text, original_text = get_text_content(request, response)

    assert "full-stack developers" in generated_text.lower()
    assert original_text == ""  # No content in the example


def test_multi_platform_example():
    """Test with multi-platform example data."""
    # Load multi-platform example request
    with open("examples/multi-platform-content.json") as f:
        request_data = json.load(f)
    request = StyleTransferRequest(**request_data)

    # Test with first schema (Twitter)
    response = StyleTransferResponse(
        processed_content=json.dumps(
            {
                "text": "🚀 REST API design tips that will save you hours! #APIDesign #BestPractices #DevTips",
                "url_allowed": True,
            }
        ),
        applied_style="Social Media Tech Influencer",
        output_schema=request.target_schemas[0],
        metadata={
            "schema_name": "Engaging Tweet",
            "reference_styles_count": 2,
            "target_documents_count": 2,
        },
    )

    generated_text, original_text = get_text_content(request, response)

    assert "API" in generated_text
    assert original_text == ""
