"""Style Transfer Agent.

A standalone Python agent that implements textual style transfer
from pre-processed documents using LangChain.
"""

from agent_style_transfer.agent import transfer_style
from agent_style_transfer.schemas import (
    ContentType,
    Document,
    DocumentCategory,
    OutputSchema,
    ReferenceStyle,
    StyleTransferRequest,
    StyleTransferResponse,
    WritingStyle,
)

__version__ = "0.1.0"
__all__ = [
    "ContentType",
    "Document",
    "DocumentCategory",
    "OutputSchema",
    "ReferenceStyle",
    "StyleTransferRequest",
    "StyleTransferResponse",
    "WritingStyle",
    "transfer_style",
]
