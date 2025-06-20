#!/usr/bin/env python3
"""Comprehensive test for the new style transfer API."""

from agent_style_transfer import (
    ContentType,
    Document,
    DocumentCategory,
    OutputSchema,
    ReferenceStyle,
    StyleTransferRequest,
    transfer_style,
)


def test_comprehensive_style_transfer() -> None:
    """Test the comprehensive style transfer function."""
    # Create reference documents (persona's writing style)
    reference_docs = [
        Document(
            url="https://example.com/persona-blog-1",
            type=ContentType.BLOG,
            category=DocumentCategory.TECHNICAL,
        ),
        Document(
            url="https://example.com/persona-linkedin-1",
            type=ContentType.LINKEDIN,
            category=DocumentCategory.PROFESSIONAL,
        ),
    ]
    # Create target documents (content to be processed)
    target_docs = [
        Document(
            url="https://example.com/target-article",
            type=ContentType.BLOG,
            category=DocumentCategory.MARKETING,
        ),
    ]
    # Create output schema for LinkedIn post
    output_schema = OutputSchema(
        name="linkedin_post",
        output_type="linkedin_post",
        max_length=300,
        min_length=50,
        format="markdown",
    )
    # Create the request
    request = StyleTransferRequest(
        reference_style=[
            ReferenceStyle(name="comprehensive_style", documents=reference_docs),
        ],
        intent="Make it more engaging and conversational while maintaining professionalism",
        focus="Extract key insights and present them in an actionable format",
        target_content=target_docs,
        target_schemas=[output_schema],
    )
    # Process the request
    response = transfer_style(request)
    # Assert expected results
    assert response.applied_style == "placeholder"
    assert response.output_schema.output_type == "linkedin_post"
    substantial_word_count = 50
    assert (
        len(response.processed_content.split()) > substantial_word_count
    )  # Should have substantial content
    assert "Extract key insights" in response.processed_content


def test_default_blog_mode() -> None:
    """Test with default blog mode (no output schemas specified)."""
    # Simple request without output schemas
    request = StyleTransferRequest(
        reference_style=[
            ReferenceStyle(
                name="default_style",
                documents=[
                    Document(
                        url="https://example.com/reference",
                        type=ContentType.BLOG,
                        category=DocumentCategory.TECHNICAL,
                    ),
                ],
            ),
        ],
        focus="Summarize the main points",
        target_content=[
            Document(
                url="https://example.com/target",
                type=ContentType.BLOG,
                category=DocumentCategory.TECHNICAL,
            ),
        ],
    )
    response = transfer_style(request)
    # Assert expected results
    assert response.applied_style == "placeholder"
    assert response.output_schema.output_type == "blog_post"
    assert "Summarize the main points" in response.processed_content
