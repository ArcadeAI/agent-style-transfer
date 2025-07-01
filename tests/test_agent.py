#!/usr/bin/env python3
"""Unit tests for the style transfer agent using VCR for API call recording."""

import json

import pytest

from agent_style_transfer.agent import transfer_style
from agent_style_transfer.schemas import StyleTransferRequest


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_single_tech_tweet():
    """Test style transfer for single tech tweet example."""
    with open("fixtures/tweet-request.json") as f:
        request_data = json.load(f)

    request = StyleTransferRequest(**request_data)

    responses = await transfer_style(request, "anthropic")

    assert len(responses) == 1
    response = responses[0]

    assert response.applied_style == "Tech Influencer Style"
    assert response.output_schema.name == "Twitter Single Post"
    assert response.processed_content is not None

    content_data = json.loads(response.processed_content)
    assert "text" in content_data
    assert "url_allowed" in content_data

    assert response.metadata["schema_name"] == "Twitter Single Post"
    assert response.metadata["reference_styles_count"] == 1
    assert response.metadata["target_documents_count"] == 1


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_multi_platform_content():
    """Test style transfer for multi-platform content example."""
    with open("fixtures/tweet-and-blog-request.json") as f:
        request_data = json.load(f)

    request = StyleTransferRequest(**request_data)

    responses = await transfer_style(request, "anthropic")

    assert len(responses) > 1

    for response in responses:
        assert response.applied_style in [
            "Tech Educator Style",
            "Social Media Tech Influencer",
        ]
        assert response.processed_content is not None

        content_data = json.loads(response.processed_content)
        assert isinstance(content_data, dict)

        assert "schema_name" in response.metadata
        assert response.metadata["reference_styles_count"] == 2
        assert response.metadata["target_documents_count"] == 2


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_linkedin_fullstack_skills():
    """Test style transfer for LinkedIn fullstack skills example."""
    with open("fixtures/linkedin-request.json") as f:
        request_data = json.load(f)

    request = StyleTransferRequest(**request_data)

    responses = await transfer_style(request, "anthropic")

    assert len(responses) >= 1

    for response in responses:
        assert response.applied_style == "LinkedIn Tech Thought Leader"
        assert response.processed_content is not None

        content_data = json.loads(response.processed_content)
        assert isinstance(content_data, dict)

        assert "schema_name" in response.metadata
        assert response.metadata["reference_styles_count"] == 1
        assert response.metadata["target_documents_count"] == 1
