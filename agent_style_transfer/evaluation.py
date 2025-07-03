from typing import Any

from agent_style_transfer.evals import (
    evaluate_content_preservation,
    evaluate_platform_appropriateness,
    evaluate_quality,
    evaluate_style_fidelity,
)
from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse

# Type aliases for cleaner annotations
EvaluationResult = dict[str, Any]
EvaluationResults = list[EvaluationResult]
BatchEvaluationResults = list[EvaluationResults]


def evaluate(
    request: StyleTransferRequest,
    responses: StyleTransferResponse | list[StyleTransferResponse],
    provider: str = "openai",
    model: str = "gpt-4",
) -> EvaluationResults | BatchEvaluationResults:
    """Evaluate style transfer response(s).
    Args:
        request: The original style transfer request
        responses: Single response or list of responses to evaluate
        provider: Model provider (openai, anthropic, google_genai)
        model: Model name to use for LLM evaluations
    Returns:
        List of evaluation results for single response, or list of lists for
        multiple responses
    """
    if isinstance(responses, list):
        return [
            _evaluate_single(request, response, provider, model)
            for response in responses
        ]
    else:
        return _evaluate_single(request, responses, provider, model)


def _evaluate_single(
    request: StyleTransferRequest,
    response: StyleTransferResponse,
    provider: str = "openai",
    model: str = "gpt-4",
) -> EvaluationResults:
    """Run all evaluations on a single style transfer response."""
    return [
        evaluate_style_fidelity(request, response, provider, model),
        evaluate_content_preservation(request, response),
        evaluate_quality(request, response, provider, model),
        evaluate_platform_appropriateness(request, response, provider, model),
    ]
