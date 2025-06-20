from enum import Enum
from typing import Set, List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl, Field


class ContentType(str, Enum):
    """
    Defines the allowed content types for a ContentItem.
    """
    TWITTER = "Twitter"
    BLOG = "Blog"
    LINKEDIN = "LinkedIn"
    YOUTUBE = "YouTube"
    REDDIT = "Reddit"
    FACEBOOK = "Facebook"
    INSTAGRAM = "Instagram"
    TIKTOK = "TikTok"


class Document(BaseModel):
    url: HttpUrl
    content_type: ContentType
    categories: Set[str]


class WritingStyle(BaseModel):
    """Defines writing style characteristics."""
    tone: str = Field(description="Overall tone: formal, casual, professional, friendly, etc.")
    formality_level: int = Field(ge=1, le=10, description="Formality scale from 1 (very casual) to 10 (very formal)")
    sentence_structure: str = Field(description="Sentence structure preference: short, long, varied, etc.")
    vocabulary_level: str = Field(description="Vocabulary complexity: simple, moderate, advanced, technical")
    personality_traits: List[str] = Field(default_factory=list, description="Personality traits: confident, humble, authoritative, etc.")
    writing_patterns: Dict[str, Any] = Field(default_factory=dict, description="Specific writing patterns and preferences")


class ReferenceStyle(BaseModel):
    """Reference style that can be either documents or a defined style schema."""
    name: str = Field(description="Name/identifier for this reference style")
    description: Optional[str] = Field(default=None, description="Description of the style")
    
    # Can be either documents OR a defined style
    documents: Optional[List[Document]] = Field(default=None, description="Reference documents from persona")
    style_definition: Optional[WritingStyle] = Field(default=None, description="Explicit style definition")
    
    # Metadata
    categories: Set[str] = Field(default_factory=set, description="Categories this style applies to")
    confidence: float = Field(ge=0.0, le=1.0, default=1.0, description="Confidence in this style definition")
    
    def __init__(self, **data):
        super().__init__(**data)
        # Ensure at least one of documents or style_definition is provided
        if not self.documents and not self.style_definition:
            raise ValueError("Either documents or style_definition must be provided")


class OutputSchema(BaseModel):
    """Schema for structured output formats."""
    name: str  # e.g., "linkedin_post", "twitter_thread", "blog_post"
    max_length: Optional[int] = None  # in words
    min_length: Optional[int] = None  # in words
    format: str = "markdown"  # default to markdown


class StyleTransferRequest(BaseModel):
    """Complete request for style transfer."""
    reference_style: List[ReferenceStyle]  # Can be documents or defined styles
    intent: Optional[str] = None  # Soft override for voice expectations
    focus: str  # How to process target content
    target_content: List[Document]  # Documents to be processed
    target_schemas: Optional[List[OutputSchema]] = None  # Output format schemas


class StyleTransferResponse(BaseModel):
    """Response from style transfer."""
    processed_content: str
    applied_style: str
    output_schema: Optional[OutputSchema] = None
