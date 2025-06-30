"""Functions to run all evaluations."""

from typing import Any, Dict, List

from agent_style_transfer.evals.content_preservation import (
    evaluate_content_preservation,
)
from agent_style_transfer.evals.platform_appropriateness import (
    evaluate_platform_appropriateness,
)
from agent_style_transfer.evals.quality import evaluate_quality
from agent_style_transfer.evals.style_fidelity import evaluate_style_fidelity
from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse


def evaluate_all(
    request: StyleTransferRequest,
    response: StyleTransferResponse,
    model: str = "openai:o3-mini",
) -> List[Dict[str, Any]]:
    """Run all evaluations on a style transfer response."""
    results = [
        evaluate_style_fidelity(request, response, model),
        evaluate_content_preservation(request, response),
        evaluate_quality(request, response, model),
        evaluate_platform_appropriateness(request, response, model),
    ]
    return results


def evaluate_batch(
    request: StyleTransferRequest,
    responses: List[StyleTransferResponse],
    model: str = "openai:o3-mini",
) -> List[List[Dict[str, Any]]]:
    """Evaluate multiple style transfer responses."""
    return [evaluate_all(request, response, model) for response in responses]
