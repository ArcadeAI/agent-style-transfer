"""Content preservation evaluation."""

from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse
from agent_style_transfer.utils.evaluation import (
    create_llm_evaluator,
    format_result,
    get_text_content,
)


def evaluate_content_preservation(
    request: StyleTransferRequest,
    response: StyleTransferResponse,
    provider: str = "anthropic",
    model: str = "claude-3-haiku-20240307",
):
    """Evaluate how well the original message is preserved."""
    generated_text, original_text = get_text_content(request, response)

    # Create evaluation prompt
    prompt = (
        "You are an expert evaluator assessing content preservation in style "
        "transfer.\n"
        "Your task is to evaluate how well the core meaning and key information "
        "from the original text is preserved in the style-transferred version.\n\n"
        "Please evaluate the content preservation on a scale of 0-5, where:\n"
        "- 5: Perfect preservation - all key information, facts, and meaning "
        "preserved\n"
        "- 4: Good preservation - most key information preserved, minor details "
        "may differ\n"
        "- 3: Moderate preservation - some key information preserved, but "
        "significant omissions or changes\n"
        "- 2: Poor preservation - most key information lost or significantly "
        "altered\n"
        "- 1: Very poor preservation - significant information lost\n"
        "- 0: No preservation - completely different meaning or content\n\n"
        "Provide your score (0-5) and a brief explanation of your reasoning."
    )

    # Create evaluator using our custom framework
    evaluator = create_llm_evaluator(prompt, "content_preservation", provider, model)
    result = evaluator(outputs=generated_text, reference_outputs=original_text)

    return format_result(
        "content_preservation", result.get("score", 0), result.get("comment")
    )
