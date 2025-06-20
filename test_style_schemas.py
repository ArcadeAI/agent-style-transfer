#!/usr/bin/env python3
"""
Test for Pydantic schema-based reference styles.
"""

from agent_style_transfer import (
    transfer_style,
    Document,
    ContentType,
    WritingStyle,
    ReferenceStyle,
    StyleTransferRequest,
    OutputSchema
)


def test_document_based_style():
    """Test using documents as reference style."""
    print("Testing document-based reference style...")
    
    # Create reference style using documents
    reference_style = ReferenceStyle(
        name="tech_blogger_style",
        description="Style based on a tech blogger's writing",
        documents=[
            Document(
                url="https://example.com/tech-blog-1",
                content_type=ContentType.BLOG,
                categories={"technology", "ai"}
            ),
            Document(
                url="https://example.com/tech-blog-2",
                content_type=ContentType.BLOG,
                categories={"programming", "startups"}
            )
        ],
        categories={"technology", "programming"},
        confidence=0.9
    )
    
    request = StyleTransferRequest(
        reference_style=[reference_style],
        focus="Write in the same engaging tech blogger style",
        target_content=[
            Document(
                url="https://example.com/target-content",
                content_type=ContentType.BLOG,
                categories={"ai", "machine-learning"}
            )
        ]
    )
    
    response = transfer_style(request)
    print(f"Applied style: {response.applied_style}")
    print(f"Content: {response.processed_content[:100]}...")
    print()


def test_schema_based_style():
    """Test using explicit style schema as reference."""
    print("Testing schema-based reference style...")
    
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
            "prefer_active_voice": True
        }
    )
    
    # Create reference style using the schema
    reference_style = ReferenceStyle(
        name="professional_consultant",
        description="Professional consultant style with clear explanations",
        style_definition=writing_style,
        categories={"business", "consulting", "professional"},
        confidence=0.95
    )
    
    request = StyleTransferRequest(
        reference_style=[reference_style],
        intent="Make it more engaging for a business audience",
        focus="Present insights in a clear, actionable format",
        target_content=[
            Document(
                url="https://example.com/business-content",
                content_type=ContentType.LINKEDIN,
                categories={"strategy", "leadership"}
            )
        ]
    )
    
    response = transfer_style(request)
    print(f"Applied style: {response.applied_style}")
    print(f"Content: {response.processed_content[:100]}...")
    print()


def test_mixed_reference_styles():
    """Test using both document-based and schema-based styles."""
    print("Testing mixed reference styles...")
    
    # Document-based style
    doc_style = ReferenceStyle(
        name="startup_founder",
        documents=[
            Document(
                url="https://example.com/founder-post",
                content_type=ContentType.LINKEDIN,
                categories={"startups", "entrepreneurship"}
            )
        ],
        categories={"startups"}
    )
    
    # Schema-based style
    schema_style = ReferenceStyle(
        name="data_scientist",
        style_definition=WritingStyle(
            tone="analytical and precise",
            formality_level=8,
            sentence_structure="clear and structured",
            vocabulary_level="technical",
            personality_traits=["analytical", "precise", "thorough"]
        ),
        categories={"data-science", "analytics"}
    )
    
    request = StyleTransferRequest(
        reference_style=[doc_style, schema_style],
        focus="Combine startup energy with analytical precision",
        target_content=[
            Document(
                url="https://example.com/mixed-content",
                content_type=ContentType.BLOG,
                categories={"startups", "analytics"}
            )
        ]
    )
    
    response = transfer_style(request)
    print(f"Applied style: {response.applied_style}")
    print(f"Content: {response.processed_content[:100]}...")
    print()


if __name__ == "__main__":
    print("=== Pydantic Schema-Based Style Tests ===\n")
    
    test_document_based_style()
    test_schema_based_style()
    test_mixed_reference_styles()
    
    print("All schema-based tests completed!") 