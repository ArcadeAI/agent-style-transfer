#!/usr/bin/env python3
"""
Comprehensive test for the new style transfer API.
"""

from agent_style_transfer import (
    transfer_style,
    StyleTransferRequest,
    Document,
    ContentType,
    OutputSchema
)


def test_comprehensive_style_transfer():
    """Test the comprehensive style transfer function."""
    print("Testing comprehensive style transfer...")
    
    # Create reference documents (persona's writing style)
    reference_docs = [
        Document(
            url="https://example.com/persona-blog-1",
            content_type=ContentType.BLOG,
            categories={"technology", "ai", "professional"}
        ),
        Document(
            url="https://example.com/persona-linkedin-1", 
            content_type=ContentType.LINKEDIN,
            categories={"business", "leadership"}
        )
    ]
    
    # Create target documents (content to be processed)
    target_docs = [
        Document(
            url="https://example.com/target-article",
            content_type=ContentType.BLOG,
            categories={"marketing", "strategy"}
        )
    ]
    
    # Create output schema for LinkedIn post
    output_schema = OutputSchema(
        name="linkedin_post",
        max_length=300,
        min_length=50,
        format="markdown"
    )
    
    # Create the request
    request = StyleTransferRequest(
        reference_style=reference_docs,
        intent="Make it more engaging and conversational while maintaining professionalism",
        focus="Extract key insights and present them in an actionable format",
        target_content=target_docs,
        target_schemas=[output_schema]
    )
    
    # Process the request
    response = transfer_style(request)
    
    # Display results
    print(f"Request processed successfully!")
    print(f"Applied style: {response.applied_style}")
    print(f"Output schema: {response.output_schema.name}")
    print(f"Content length: {len(response.processed_content.split())} words")
    print(f"\nProcessed content:\n{response.processed_content}")
    print()


def test_default_blog_mode():
    """Test with default blog mode (no output schemas specified)."""
    print("Testing default blog mode...")
    
    # Simple request without output schemas
    request = StyleTransferRequest(
        reference_style=[
            Document(
                url="https://example.com/reference",
                content_type=ContentType.BLOG,
                categories={"tech"}
            )
        ],
        focus="Summarize the main points",
        target_content=[
            Document(
                url="https://example.com/target",
                content_type=ContentType.BLOG,
                categories={"ai"}
            )
        ]
    )
    
    response = transfer_style(request)
    
    print(f"Default mode applied: {response.applied_style}")
    print(f"Default schema: {response.output_schema.name}")
    print(f"Content:\n{response.processed_content}")
    print()


if __name__ == "__main__":
    print("=== Comprehensive Style Transfer Tests ===\n")
    
    test_comprehensive_style_transfer()
    test_default_blog_mode()
    
    print("All comprehensive tests completed!") 