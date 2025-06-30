"""Platform appropriateness evaluation."""

from . import (
    StyleTransferRequest,
    StyleTransferResponse,
    create_llm_evaluator,
    format_result,
    get_text_content,
    safe_evaluation,
)

PLATFORM_APPROPRIATENESS_PROMPT = """
Rate how appropriate this content is for the target platform (1-5 scale):

Content: {outputs}
Platform: {platform}

Consider platform-specific requirements and conventions.
Score 1-5 where 1=inappropriate, 5=perfect for platform.
"""


@safe_evaluation("platform_appropriateness")
def evaluate_platform_appropriateness(
    request: StyleTransferRequest,
    response: StyleTransferResponse,
    model: str = "openai:o3-mini",
):
    """Evaluate platform appropriateness."""
    generated_text, _ = get_text_content(request, response)
    platform = (
        response.output_schema.output_type.value
        if response.output_schema
        else "unknown"
    )

    evaluator = create_llm_evaluator(
        PLATFORM_APPROPRIATENESS_PROMPT, "platform_appropriateness", model
    )
    result = evaluator(outputs=generated_text, platform=platform)

    return format_result(
        "platform_appropriateness", result.get("score", 0), result.get("comment")
    )
