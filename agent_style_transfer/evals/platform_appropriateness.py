"""Platform appropriateness evaluation."""

from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse
from agent_style_transfer.utils.evaluation import (
    create_llm_evaluator,
    format_result,
    get_text_content,
)

PLATFORM_APPROPRIATENESS_PROMPT = """
Rate how appropriate this content is for the target platform (1-5 scale):

Content: {outputs}
Platform: {platform}

Consider platform-specific requirements and conventions.
Score 1-5 where 1=inappropriate, 5=perfect for platform.
"""


def evaluate_platform_appropriateness(
    request: StyleTransferRequest,
    response: StyleTransferResponse,
    provider: str = "openai",
    model: str = "gpt-4",
):
    """Evaluate platform appropriateness."""
    generated_text, _ = get_text_content(request, response)
    platform = (
        response.output_schema.output_type.value
        if response.output_schema
        else "unknown"
    )

    evaluator = create_llm_evaluator(
        PLATFORM_APPROPRIATENESS_PROMPT, "platform_appropriateness", provider, model
    )
    result = evaluator(outputs=generated_text, platform=platform)

    return format_result(
        "platform_appropriateness", result.get("score", 0), result.get("comment")
    )
