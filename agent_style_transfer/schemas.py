"""Comprehensive schemas for textual style transfer with social media support.

This module defines Pydantic models for style transfer requests and responses,
including support for various document types, writing styles, and output formats
such as Twitter, LinkedIn, and blog posts.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl, field_validator


class ContentType(str, Enum):
    """Defines the allowed content types for a ContentItem."""

    TWITTER = "Twitter"
    BLOG = "Blog"
    LINKEDIN = "LinkedIn"
    REDDIT = "Reddit"
    FACEBOOK = "Facebook"
    INSTAGRAM = "Instagram"
    TIKTOK = "TikTok"


class DocumentCategory(str, Enum):
    """Categories for document classification."""

    CASUAL = "Casual"
    FORMAL = "Formal"
    VERY_FORMAL = "Very Formal"
    FUNNY = "Funny"
    PROFESSIONAL = "Professional"
    TECHNICAL = "Technical"
    CREATIVE = "Creative"
    ACADEMIC = "Academic"
    JOURNALISTIC = "Journalistic"
    MARKETING = "Marketing"


class DocumentType(str, Enum):
    """Supported file types for documents."""

    TXT = "txt"
    MARKDOWN = "markdown"
    URL = "url"
    PDF = "pdf"
    DOCX = "docx"


class Document(BaseModel):
    """Comprehensive document schema for input documents."""

    url: HttpUrl = Field(description="URL to the document")
    type: ContentType = Field(
        description="Type of content (e.g., Twitter, LinkedIn, Blog, etc.)",
    )
    category: DocumentCategory = Field(
        description="Category (e.g., Casual, Formal, Very Formal, Funny, etc.)",
    )
    file_type: DocumentType | None = Field(
        default=None,
        description="File type if applicable",
    )
    title: str | None = Field(default=None, description="Document title if available")
    author: str | None = Field(default=None, description="Document author if available")
    date_published: datetime | None = Field(
        default=None,
        description="Publication date if available",
    )
    content: str | None = Field(
        default=None,
        description="The actual text content of the document",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )


class WritingStyle(BaseModel):
    """Defines writing style characteristics."""

    tone: str = Field(
        description="Overall tone: formal, casual, professional, friendly, etc.",
    )
    formality_level: int = Field(
        ge=1,
        le=10,
        description="Formality scale from 1 (very casual) to 10 (very formal)",
    )
    sentence_structure: str = Field(
        description="Sentence structure preference: short, long, varied, etc.",
    )
    vocabulary_level: str = Field(
        description="Vocabulary complexity: simple, moderate, advanced, technical",
    )
    personality_traits: list[str] = Field(
        default_factory=list,
        description="Personality traits: confident, humble, authoritative, etc.",
    )
    writing_patterns: dict[str, Any] = Field(
        default_factory=dict,
        description="Specific writing patterns and preferences",
    )


class ReferenceStyle(BaseModel):
    """Reference style that can be either documents or a defined style schema."""

    name: str = Field(description="Name/identifier for this reference style")
    description: str | None = Field(
        default=None,
        description="Description of the style",
    )

    documents: list[Document] | None = Field(
        default=None,
        description="Reference documents from persona",
    )
    style_definition: WritingStyle | None = Field(
        default=None,
        description="Explicit style definition",
    )

    categories: set[str] = Field(
        default_factory=set,
        description="Categories this style applies to",
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        default=1.0,
        description="Confidence in this style definition",
    )

    def __init__(self, **data: Any) -> None:
        """Initialize the ReferenceStyle with validation.

        Args:
            **data: Keyword arguments to initialize the model fields.

        Raises:
            ValueError: If neither documents nor style_definition is provided.

        """
        super().__init__(**data)
        if not self.documents and not self.style_definition:
            error_msg = "Either documents or style_definition must be provided"
            raise ValueError(error_msg)


class TweetSingle(BaseModel):
    """Single tweet schema."""

    text: str = Field(description="Tweet text content")
    url_allowed: bool = Field(
        default=True,
        description="Whether URLs are allowed in this tweet",
    )


class TweetThread(BaseModel):
    """Twitter thread schema."""

    tweets: list[TweetSingle] = Field(description="List of tweets in the thread")
    max_tweets: int = Field(
        default=25,
        description="Maximum number of tweets in thread",
    )


class LinkedInPost(BaseModel):
    """LinkedIn post schema."""

    text: str = Field(description="Post text content")
    multimedia_url: HttpUrl | None = Field(
        default=None,
        description="URL to multimedia content (image/video)",
    )


class LinkedInComment(BaseModel):
    """LinkedIn comment schema."""

    text: str = Field(description="Comment text content")


class BlogPost(BaseModel):
    """Blog post schema."""

    title: str = Field(description="Blog post title")
    subtitle: str | None = Field(default=None, description="Blog post subtitle")
    markdown: str = Field(description="Blog post content in markdown format")
    tags: list[str] = Field(default_factory=list, description="Tags for the blog post")
    categories: list[str] = Field(
        default_factory=list,
        description="Categories for the blog post",
    )
    date: datetime | None = Field(default=None, description="Publication date")


class StyleTransferRequest(BaseModel):
    """Complete request for style transfer."""

    reference_style: list[ReferenceStyle] = Field(
        description="Reference styles (documents or defined styles)",
    )
    intent: str | None = Field(
        default=None,
        description="Soft override for voice expectations",
    )
    focus: str = Field(description="How to process target content")
    target_content: list[Document] = Field(description="Documents to be processed")
    target_schemas: list[OutputSchema] = Field(
        description="Output schemas for different platforms",
    )

    @field_validator("reference_style")
    @classmethod
    def validate_reference_style(cls, v):
        if not v:
            raise ValueError("At least one reference style must be provided")
        return v

    @field_validator("target_content")
    @classmethod
    def validate_target_content(cls, v):
        if not v:
            raise ValueError("At least one target content must be provided")
        return v

    @field_validator("target_schemas")
    @classmethod
    def validate_target_schemas(cls, v):
        if not v:
            raise ValueError("At least one target schema must be provided")
        return v


class OutputSchema(BaseModel):
    """Comprehensive schema for structured output formats."""

    name: str = Field(description="Schema name/identifier")

    output_type: OutputType = Field(
        description="Type of output",
    )

    max_length: int | None = Field(default=None, description="Maximum length in words")
    min_length: int | None = Field(default=None, description="Minimum length in words")
    format: str = Field(default="markdown", description="Output format")

    tweet_single: TweetSingle | None = Field(
        default=None,
        description="Single tweet configuration",
    )
    tweet_thread: TweetThread | None = Field(
        default=None,
        description="Twitter thread configuration",
    )
    linkedin_post: LinkedInPost | None = Field(
        default=None,
        description="LinkedIn post configuration",
    )
    linkedin_comment: LinkedInComment | None = Field(
        default=None,
        description="LinkedIn comment configuration",
    )
    blog_post: BlogPost | None = Field(
        default=None,
        description="Blog post configuration",
    )

    description: str | None = Field(
        default=None,
        description="Description of this output schema",
    )
    platform: str | None = Field(
        default=None,
        description="Target platform for this schema",
    )


class StyleTransferResponse(BaseModel):
    """Response from style transfer."""

    processed_content: str = Field(description="The processed content")
    applied_style: str = Field(description="Name of the applied style")
    output_schema: OutputSchema | None = Field(
        default=None,
        description="Output schema used",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the processing",
    )


class OutputType(str, Enum):
    """Enum for output types with their corresponding schema classes."""

    TWEET_SINGLE = "tweet_single"
    TWEET_THREAD = "tweet_thread"
    LINKEDIN_POST = "linkedin_post"
    LINKEDIN_COMMENT = "linkedin_comment"
    BLOG_POST = "blog_post"

    def get_schema(self) -> type[BaseModel]:
        """Get the corresponding Pydantic schema class."""
        from agent_style_transfer.schemas import (
            BlogPost,
            LinkedInComment,
            LinkedInPost,
            TweetSingle,
            TweetThread,
        )

        schema_map = {
            OutputType.TWEET_SINGLE: TweetSingle,
            OutputType.TWEET_THREAD: TweetThread,
            OutputType.LINKEDIN_POST: LinkedInPost,
            OutputType.LINKEDIN_COMMENT: LinkedInComment,
            OutputType.BLOG_POST: BlogPost,
        }

        return schema_map[self]
