#!/usr/bin/env python3
"""Basic test script for the style transfer agent."""

from agent_style_transfer import transfer_style
from agent_style_transfer.schemas import (
    ContentType,
    Document,
    DocumentCategory,
    ReferenceStyle,
    StyleTransferRequest,
)


def test_basic_style_transfer() -> None:
    """Test the basic style transfer function."""
    # Create a simple request
    request = StyleTransferRequest(
        reference_style=[
            ReferenceStyle(
                name="basic_reference",
                documents=[
                    Document(
                        url="https://example.com/reference",
                        type=ContentType.BLOG,
                        category=DocumentCategory.TECHNICAL,
                    ),
                ],
            ),
        ],
        focus="Convert to formal style",
        target_content=[
            Document(
                url="https://example.com/target",
                type=ContentType.BLOG,
                category=DocumentCategory.FORMAL,
            ),
        ],
    )
    response = transfer_style(request)
    assert response.applied_style == "placeholder"
    assert response.output_schema.name == "blog_post"
    assert "Style Transfer Result" in response.processed_content
    assert "Convert to formal style" in response.processed_content
