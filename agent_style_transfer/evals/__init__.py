"""Evaluation functions for style transfer."""

from agent_style_transfer.evals.content_preservation import (
    evaluate_content_preservation,
)
from agent_style_transfer.evals.platform_appropriateness import (
    evaluate_platform_appropriateness,
)
from agent_style_transfer.evals.quality import evaluate_quality
from agent_style_transfer.evals.style_fidelity import evaluate_style_fidelity
from agent_style_transfer.evals.style_inference_accuracy import (
    evaluate_style_inference_accuracy,
)
from agent_style_transfer.evals.style_rule_usefulness import (
    evaluate_style_rule_usefulness,
)

__all__ = [
    "evaluate_all",
    "evaluate_batch",
    "evaluate_content_preservation",
    "evaluate_platform_appropriateness",
    "evaluate_quality",
    "evaluate_style_fidelity",
    "evaluate_style_inference_accuracy",
    "evaluate_style_rule_usefulness",
]


def evaluate_all(request, response, provider: str = "openai", model: str = "gpt-4"):
    """Run all evaluation functions on a single response."""
    from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse

    if not isinstance(request, StyleTransferRequest):
        raise ValueError("request must be a StyleTransferRequest")
    if not isinstance(response, StyleTransferResponse):
        raise ValueError("response must be a StyleTransferResponse")

    results = []

    # Run all evaluation functions
    results.append(evaluate_style_fidelity(request, response, provider, model))
    results.append(evaluate_content_preservation(request, response))
    results.append(evaluate_quality(request, response, provider, model))
    results.append(
        evaluate_platform_appropriateness(request, response, provider, model)
    )

    # Add style inference evaluations (only if reference documents exist)
    has_reference_docs = any(
        ref_style.documents for ref_style in request.reference_style
    )
    if has_reference_docs:
        results.append(
            evaluate_style_inference_accuracy(request, response, provider, model)
        )
        results.append(
            evaluate_style_rule_usefulness(request, response, provider, model)
        )

    return results


def evaluate_batch(request, responses, provider: str = "openai", model: str = "gpt-4"):
    """Run all evaluation functions on multiple responses."""
    from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse

    if not isinstance(request, StyleTransferRequest):
        raise ValueError("request must be a StyleTransferRequest")
    if not isinstance(responses, list):
        raise ValueError("responses must be a list")
    if not all(isinstance(r, StyleTransferResponse) for r in responses):
        raise ValueError("all responses must be StyleTransferResponse objects")

    batch_results = []

    for response in responses:
        response_results = evaluate_all(request, response, provider, model)
        batch_results.append(response_results)

    return batch_results
