from enum import Enum
from typing import Set
from pydantic import BaseModel, HttpUrl


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
