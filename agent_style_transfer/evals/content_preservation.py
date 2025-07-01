"""Content preservation evaluation."""

from openevals.string.embedding_similarity import create_embedding_similarity_evaluator

from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse
from agent_style_transfer.utils.evaluation import (
    format_result,
    get_text_content,
)


def evaluate_content_preservation(
    request: StyleTransferRequest, response: StyleTransferResponse
):
    """Evaluate how well the original message is preserved."""
    generated_text, original_text = get_text_content(request, response)

    evaluator = create_embedding_similarity_evaluator()
    result = evaluator(outputs=generated_text, reference_outputs=original_text)

    return format_result(
        "content_preservation", result.get("score", 0), result.get("comment")
    )
