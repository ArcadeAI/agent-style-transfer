"""Content quality evaluation."""

from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse
from agent_style_transfer.utils.evaluation import (
    create_llm_evaluator,
    format_result,
    get_text_content,
)

QUALITY_PROMPT = """
Rate the overall quality of this content (1-5 scale):

Generated Content: {outputs}
Platform: {platform}
Intent: {intent}

Consider writing quality, engagement potential, and value.
Score 1-5 where 1=poor, 5=excellent.
"""


def evaluate_quality(
    request: StyleTransferRequest,
    response: StyleTransferResponse,
    provider: str = "anthropic",
    model: str = "gpt-4",
):
    """Evaluate overall content quality."""
    generated_text, _ = get_text_content(request, response)
    platform = (
        response.output_schema.output_type.value
        if response.output_schema
        else "unknown"
    )

    evaluator = create_llm_evaluator(QUALITY_PROMPT, "content_quality", provider, model)
    result = evaluator(
        outputs=generated_text,
        platform=platform,
        intent=request.intent or "Not specified",
    )

    return format_result(
        "content_quality", result.get("score", 0), result.get("comment")
    )
