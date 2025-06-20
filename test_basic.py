#!/usr/bin/env python3
"""
Basic test script for the style transfer agent.
"""

from agent_style_transfer import transfer_style, Document, ContentType, StyleTransferRequest


def test_basic_style_transfer():
    """Test the basic style transfer function."""
    print("Testing basic style transfer...")
    
    # Create a simple request
    request = StyleTransferRequest(
        reference_style=[
            Document(
                url="https://example.com/reference",
                content_type=ContentType.BLOG,
                categories={"technology"}
            )
        ],
        focus="Convert to formal style",
        target_content=[
            Document(
                url="https://example.com/target",
                content_type=ContentType.BLOG,
                categories={"ai"}
            )
        ]
    )
    
    response = transfer_style(request)
    
    print(f"Applied style: {response.applied_style}")
    print(f"Output schema: {response.output_schema.name}")
    print(f"Content:\n{response.processed_content}")
    print()


if __name__ == "__main__":
    print("=== Style Transfer Agent Basic Tests ===\n")
    
    test_basic_style_transfer()
    
    print("All tests completed!") 