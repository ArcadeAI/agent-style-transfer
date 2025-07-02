#!/usr/bin/env python3
"""Unit tests for evaluator utility functions."""

import json

import pytest


from agent_style_transfer.schemas import (
    StyleTransferRequest,
    StyleTransferResponse,
)
from agent_style_transfer.utils.evaluation import (
    format_result,
    get_text_content,
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


@pytest.mark.parametrize(
    "request_file,response_file,expected_keywords",
    [
        (
            "fixtures/tweet-request.json",
            "fixtures/tweet-response.json",
            ["Machine Learning", "AI", "programming"],
        ),
        (
            "fixtures/linkedin-request.json",
            "fixtures/linkedin-response.json",
            ["full-stack developers", "React", "Node.js"],
        ),
        (
            "fixtures/tweet-and-blog-request.json",
            "fixtures/tweet-and-blog-response.json",
            ["API", "REST", "design"],
        ),
    ],
)
def test_get_text_content(request_file, response_file, expected_keywords):
    """Test text content extraction with various fixture data."""
    # Load request data
    with open(request_file) as f:
        request_data = json.load(f)
    request = StyleTransferRequest(**request_data)

    # Load response data
    with open(response_file) as f:
        response_data = json.load(f)

    # Test each response in the file
    for response_item in response_data["responses"]:
        # Find matching schema
        matching_schema = None
        for schema in request.target_schemas:
            if schema.name == response_item["output_schema"]:
                matching_schema = schema
                break

        if not matching_schema:
            continue

        response = StyleTransferResponse(
            processed_content=response_item["processed_content"],
            applied_style=response_item["applied_style"],
            output_schema=matching_schema,
            metadata=response_item["metadata"],
        )

        generated_text, original_text = get_text_content(request, response)

        # Assertions
        assert isinstance(generated_text, str)
        assert isinstance(original_text, str)

        # Check that generated text contains expected keywords
        for keyword in expected_keywords:
            assert (
                keyword.lower() in generated_text.lower()
            ), f"Expected '{keyword}' in generated text"

        # Original text should be empty since fixture files don't contain actual content
        assert (
            original_text == ""
        ), f"Expected empty original text, got: {original_text}"


def test_get_text_content_no_original_content():
    """Test text content extraction when original content is None."""
    # Load real example request
    with open("fixtures/tweet-request.json") as f:
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



