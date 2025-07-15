"""Style inference accuracy evaluation."""

from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse
from agent_style_transfer.utils.evaluation import (
    create_llm_evaluator,
    format_result,
)
from agent_style_transfer.writing_style_inferrer import (
    infer_few_shot_examples,
    infer_style_rules,
)

STYLE_INFERENCE_ACCURACY_PROMPT = """
Rate the accuracy of the inferred style rules and examples (1-5 scale):

Reference Documents: {reference_documents}
Inferred Style Rules: {inferred_rules}
Inferred Examples: {inferred_examples}

Consider:
1. How well the rules capture the actual writing patterns
2. Whether the examples demonstrate the style effectively
3. If the inferences are specific and actionable
4. Overall accuracy of style characterization

Score 1-5 where 1=completely inaccurate, 5=highly accurate.
"""


def evaluate_style_inference_accuracy(
    request: StyleTransferRequest,
    response: StyleTransferResponse,
    provider: str = "anthropic",
    model: str = "claude-3-haiku-20240307",
):
    """Evaluate how accurately the style inference worked."""
    # Extract reference documents
    reference_documents = []
    for ref_style in request.reference_style:
        if ref_style.documents:
            reference_documents.extend(ref_style.documents)

    if not reference_documents:
        return format_result(
            "style_inference_accuracy", 0, "No reference documents available"
        )

    # Run style inference
    try:
        inferred_rules = infer_style_rules(reference_documents, provider, model)
        inferred_examples = infer_few_shot_examples(
            reference_documents, provider, model
        )
    except Exception as e:
        return format_result(
            "style_inference_accuracy", 0, f"Style inference failed: {str(e)}"
        )

    # Check if style inference produced any results
    if not inferred_rules and not inferred_examples:
        return format_result(
            "style_inference_accuracy", 0, "No reference documents available"
        )

    # Format documents for evaluation
    doc_texts = []
    for doc in reference_documents:
        if doc.title and doc.content:
            doc_texts.append(f"Title: {doc.title}\nContent: {doc.content[:200]}...")

    reference_docs_text = "\n\n".join(doc_texts)
    rules_text = "\n".join([f"- {rule}" for rule in inferred_rules])
    examples_text = "\n\n".join(
        [f"Input: {ex.input}\nOutput: {ex.output}" for ex in inferred_examples]
    )

    evaluator = create_llm_evaluator(
        STYLE_INFERENCE_ACCURACY_PROMPT, "style_inference_accuracy", provider, model
    )
    result = evaluator(
        f"Reference Documents: {reference_docs_text}\nInferred Rules: {rules_text}\nInferred Examples: {examples_text}"
    )

    return format_result(
        "style_inference_accuracy", result.get("score", 0), result.get("comment")
    )
