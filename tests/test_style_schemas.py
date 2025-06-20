#!/usr/bin/env python3
"""Test for Pydantic schema-based reference styles."""

import pytest

from agent_style_transfer import (
    ContentType,
    Document,
    DocumentCategory,
    ReferenceStyle,
    StyleTransferRequest,
    WritingStyle,
    transfer_style,
)


def test_document_based_style() -> None:
    """Test using documents as reference style."""
    # Create reference style using documents
    reference_style = ReferenceStyle(
        name="tech_blogger_style",
        description="Style based on a tech blogger's writing",
        documents=[
            Document(
                url="https://example.com/tech-blog-1",
                type=ContentType.BLOG,
                category=DocumentCategory.TECHNICAL,
            ),
            Document(
                url="https://example.com/tech-blog-2",
                type=ContentType.BLOG,
                category=DocumentCategory.TECHNICAL,
            ),
        ],
        categories={"technology", "programming"},
        confidence=0.9,
    )

    request = StyleTransferRequest(
        reference_style=[reference_style],
        focus="Write in the same engaging tech blogger style",
        target_content=[
            Document(
                url="https://example.com/target-content",
                type=ContentType.BLOG,
                category=DocumentCategory.TECHNICAL,
            ),
        ],
    )

    response = transfer_style(request)
    assert response.applied_style == "placeholder"
    assert "tech blogger style" in response.processed_content


def test_schema_based_style() -> None:
    """Test using explicit style schema as reference."""
    # Create explicit writing style definition
    writing_style = WritingStyle(
        tone="professional yet approachable",
        formality_level=7,
        sentence_structure="varied",
        vocabulary_level="moderate",
        personality_traits=["confident", "knowledgeable", "helpful"],
        writing_patterns={
            "use_examples": True,
            "include_action_items": True,
            "prefer_active_voice": True,
        },
    )

    # Create reference style using the schema
    reference_style = ReferenceStyle(
        name="professional_consultant",
        description="Professional consultant style with clear explanations",
        style_definition=writing_style,
        categories={"business", "consulting", "professional"},
        confidence=0.95,
    )

    request = StyleTransferRequest(
        reference_style=[reference_style],
        intent="Make it more engaging for a business audience",
        focus="Present insights in a clear, actionable format",
        target_content=[
            Document(
                url="https://example.com/business-content",
                type=ContentType.LINKEDIN,
                category=DocumentCategory.PROFESSIONAL,
            ),
        ],
    )

    response = transfer_style(request)
    assert response.applied_style == "placeholder"
    assert "business audience" in response.processed_content


@pytest.mark.parametrize("expected_count", [2])
def test_mixed_reference_styles(expected_count: int) -> None:
    """Test using both document-based and schema-based styles."""
    # Document-based style
    doc_style = ReferenceStyle(
        name="startup_founder",
        documents=[
            Document(
                url="https://example.com/founder-post",
                type=ContentType.LINKEDIN,
                category=DocumentCategory.PROFESSIONAL,
            ),
        ],
        categories={"startups"},
    )

    # Schema-based style
    schema_style = ReferenceStyle(
        name="data_scientist",
        style_definition=WritingStyle(
            tone="analytical and precise",
            formality_level=8,
            sentence_structure="clear and structured",
            vocabulary_level="technical",
            personality_traits=["analytical", "precise", "thorough"],
        ),
        categories={"data-science", "analytics"},
    )

    request = StyleTransferRequest(
        reference_style=[doc_style, schema_style],
        focus="Combine startup energy with analytical precision",
        target_content=[
            Document(
                url="https://example.com/mixed-content",
                type=ContentType.BLOG,
                category=DocumentCategory.TECHNICAL,
            ),
        ],
    )

    response = transfer_style(request)
    assert response.applied_style == "placeholder"
    assert "startup energy" in response.processed_content
    assert (
        len(request.reference_style) == expected_count
    )  # Should have 2 reference styles
