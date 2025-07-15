"""Style rule usefulness evaluation."""

from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse
from agent_style_transfer.utils.evaluation import (
    create_llm_evaluator,
    format_result,
    get_text_content,
)
from agent_style_transfer.writing_style_inferrer import (
    infer_style_rules,
)

STYLE_RULE_USEFULNESS_PROMPT = """
Rate how useful the inferred style rules are for style transfer (1-5 scale):

Reference Documents: {reference_documents}
Inferred Style Rules: {inferred_rules}
Generated Content: {generated_content}
Original Content: {original_content}

Consider:
1. How actionable and specific the rules are
2. Whether following these rules would improve the output
3. If the rules capture the most important style characteristics
4. How well the rules would guide a writer to match the style

Score 1-5 where 1=not useful at all, 5=highly useful for style transfer.
"""


def evaluate_style_rule_usefulness(
    request: StyleTransferRequest,
    response: StyleTransferResponse,
    provider: str = "anthropic",
    model: str = "claude-3-haiku-20240307",
):
    """Evaluate how useful the inferred style rules are for style transfer."""
    # Extract reference documents
    reference_documents = []
    for ref_style in request.reference_style:
        if ref_style.documents:
            reference_documents.extend(ref_style.documents)

    if not reference_documents:
        return format_result(
            "style_rule_usefulness", 0, "No reference documents available"
        )

    # Get generated and original content
    generated_text, original_text = get_text_content(request, response)

    # Run style inference
    try:
        inferred_rules = infer_style_rules(reference_documents, provider, model)
    except Exception as e:
        return format_result(
            "style_rule_usefulness", 0, f"Style inference failed: {str(e)}"
        )

    # Check if style inference produced any results
    if not inferred_rules:
        return format_result(
            "style_rule_usefulness", 0, "No reference documents available"
        )

    # Format documents for evaluation
    doc_texts = []
    for doc in reference_documents:
        if doc.title and doc.content:
            doc_texts.append(f"Title: {doc.title}\nContent: {doc.content[:200]}...")

    reference_docs_text = "\n\n".join(doc_texts)
    rules_text = "\n".join([f"- {rule}" for rule in inferred_rules])

    evaluator = create_llm_evaluator(
        STYLE_RULE_USEFULNESS_PROMPT, "style_rule_usefulness", provider, model
    )
    result = evaluator(
        f"Reference Documents: {reference_docs_text}\nInferred Rules: {rules_text}\nGenerated Content: {generated_text}\nOriginal Content: {original_text}"
    )

    return format_result(
        "style_rule_usefulness", result.get("score", 0), result.get("comment")
    )
