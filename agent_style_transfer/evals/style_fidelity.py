"""Style fidelity evaluation."""

from . import (
    StyleTransferRequest,
    StyleTransferResponse,
    create_llm_evaluator,
    format_result,
    get_text_content,
    safe_evaluation,
)

STYLE_FIDELITY_PROMPT = """
Rate the style fidelity of this content (1-5 scale):

Reference Style: {reference_style}
Original Content: {original_content}
Generated Content: {outputs}

Consider tone, formality, vocabulary, and writing patterns.
Score 1-5 where 1=completely different, 5=excellent match.
"""


@safe_evaluation("style_fidelity")
def evaluate_style_fidelity(
    request: StyleTransferRequest,
    response: StyleTransferResponse,
    model: str = "openai:o3-mini",
):
    """Evaluate how well the output matches the reference style."""
    generated_text, original_text = get_text_content(request, response)

    evaluator = create_llm_evaluator(STYLE_FIDELITY_PROMPT, "style_fidelity", model)
    result = evaluator(
        reference_style=str(request.reference_style[0]),
        original_content=original_text,
        outputs=generated_text,
    )

    return format_result(
        "style_fidelity", result.get("score", 0), result.get("comment")
    )
