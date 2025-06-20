"""
Style Transfer Agent

A standalone Python agent that implements textual style transfer 
from pre-processed documents using the Arcade.dev ecosystem.
"""

from agent_style_transfer.schemas import (
    ContentType, 
    Document, 
    WritingStyle,
    ReferenceStyle,
    OutputSchema, 
    StyleTransferRequest, 
    StyleTransferResponse
)
from agent_style_transfer.agent import transfer_style

__version__ = "0.1.0"
__all__ = [
    "ContentType", 
    "Document", 
    "WritingStyle",
    "ReferenceStyle",
    "OutputSchema", 
    "StyleTransferRequest", 
    "StyleTransferResponse",
    "transfer_style"
] 