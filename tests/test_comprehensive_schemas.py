#!/usr/bin/env python3
"""Test script to demonstrate the comprehensive schemas for style transfer."""

from agent_style_transfer.agent import transfer_style
from agent_style_transfer.schemas import (
    BlogPost,
    ContentType,
    Document,
    DocumentCategory,
    DocumentType,
    LinkedInPost,
    OutputSchema,
    ReferenceStyle,
    StyleTransferRequest,
    TweetSingle,
    TweetThread,
)


def test_twitter_single_tweet() -> None:
    """Test creating a single tweet output."""
    # Create reference documents
    reference_docs = [
        Document(
            url="https://example.com/reference1.txt",
            type=ContentType.TWITTER,
            category=DocumentCategory.CASUAL,
            file_type=DocumentType.TXT,
            title="Casual Twitter Reference",
        ),
    ]

    # Create target documents
    target_docs = [
        Document(
            url="https://example.com/target1.md",
            type=ContentType.BLOG,
            category=DocumentCategory.FORMAL,
            file_type=DocumentType.MARKDOWN,
            title="Formal Blog Post",
        ),
    ]

    # Create output schema for single tweet
    output_schema = OutputSchema(
        name="casual_tweet",
        output_type="tweet_single",
        max_length=280,
        min_length=50,
        format="text",
        tweet_single=TweetSingle(text="", url_allowed=True),
    )

    # Create request
    request = StyleTransferRequest(
        reference_style=[ReferenceStyle(name="casual_style", documents=reference_docs)],
        intent="Make it engaging and casual",
        focus="Key insights from the blog post",
        target_content=target_docs,
        target_schemas=[output_schema],
    )

    # Process
    response = transfer_style(request)
    assert response.output_schema.output_type == "tweet_single"
    assert "placeholder tweet" in response.processed_content
    assert "Key insights from the blog post" in response.processed_content


def test_twitter_thread() -> None:
    """Test creating a Twitter thread output."""
    # Create reference documents
    reference_docs = [
        Document(
            url="https://example.com/reference2.txt",
            type=ContentType.TWITTER,
            category=DocumentCategory.PROFESSIONAL,
            file_type=DocumentType.TXT,
            title="Professional Twitter Reference",
        ),
    ]

    # Create target documents
    target_docs = [
        Document(
            url="https://example.com/target2.pdf",
            type=ContentType.BLOG,
            category=DocumentCategory.TECHNICAL,
            file_type=DocumentType.PDF,
            title="Technical Report",
        ),
    ]

    # Create output schema for Twitter thread
    output_schema = OutputSchema(
        name="professional_thread",
        output_type="tweet_thread",
        max_length=1000,
        min_length=200,
        format="text",
        tweet_thread=TweetThread(tweets=[], max_tweets=5),
    )

    # Create request
    request = StyleTransferRequest(
        reference_style=[
            ReferenceStyle(name="professional_style", documents=reference_docs),
        ],
        intent="Break down complex concepts",
        focus="Main findings and implications",
        target_content=target_docs,
        target_schemas=[output_schema],
    )

    # Process
    response = transfer_style(request)
    assert response.output_schema.output_type == "tweet_thread"
    assert "Thread" in response.processed_content
    assert "Break down complex concepts" in response.processed_content


def test_linkedin_post() -> None:
    """Test creating a LinkedIn post output."""
    # Create reference documents
    reference_docs = [
        Document(
            url="https://example.com/reference3.txt",
            type=ContentType.LINKEDIN,
            category=DocumentCategory.PROFESSIONAL,
            file_type=DocumentType.TXT,
            title="Professional LinkedIn Reference",
        ),
    ]

    # Create target documents
    target_docs = [
        Document(
            url="https://example.com/target3.docx",
            type=ContentType.BLOG,
            category=DocumentCategory.MARKETING,
            file_type=DocumentType.DOCX,
            title="Marketing Strategy",
        ),
    ]

    # Create output schema for LinkedIn post
    output_schema = OutputSchema(
        name="professional_linkedin_post",
        output_type="linkedin_post",
        max_length=2000,
        min_length=100,
        format="text",
        linkedin_post=LinkedInPost(text="", multimedia_url=None),
    )

    # Create request
    request = StyleTransferRequest(
        reference_style=[
            ReferenceStyle(
                name="professional_linkedin_style",
                documents=reference_docs,
            ),
        ],
        intent="Share insights professionally",
        focus="Key takeaways and business value",
        target_content=target_docs,
        target_schemas=[output_schema],
    )

    # Process
    response = transfer_style(request)
    assert response.output_schema.output_type == "linkedin_post"
    assert "LinkedIn post" in response.processed_content
    assert "Key takeaways and business value" in response.processed_content


def test_blog_post() -> None:
    """Test creating a blog post output."""
    # Create reference documents
    reference_docs = [
        Document(
            url="https://example.com/reference4.md",
            type=ContentType.BLOG,
            category=DocumentCategory.TECHNICAL,
            file_type=DocumentType.MARKDOWN,
            title="Technical Blog Reference",
        ),
    ]

    # Create target documents
    target_docs = [
        Document(
            url="https://example.com/target4.txt",
            type=ContentType.TWITTER,
            category=DocumentCategory.CASUAL,
            file_type=DocumentType.TXT,
            title="Casual Twitter Content",
        ),
    ]

    # Create output schema for blog post
    output_schema = OutputSchema(
        name="technical_blog_post",
        output_type="blog_post",
        max_length=5000,
        min_length=500,
        format="markdown",
        blog_post=BlogPost(
            title="",
            subtitle="",
            author="AI Style Transfer",
            markdown="",
            tags=[],
            categories=[],
        ),
    )

    # Create request
    request = StyleTransferRequest(
        reference_style=[
            ReferenceStyle(name="technical_blog_style", documents=reference_docs),
        ],
        intent="Expand and formalize the content",
        focus="Comprehensive analysis and insights",
        target_content=target_docs,
        target_schemas=[output_schema],
    )

    # Process
    response = transfer_style(request)
    assert response.output_schema.output_type == "blog_post"
    assert "blog post" in response.processed_content
    assert "Comprehensive analysis and insights" in response.processed_content
