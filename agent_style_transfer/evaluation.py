from typing import Any, Dict, List, Union

from agent_style_transfer.evals import (
    evaluate_content_preservation,
    evaluate_platform_appropriateness,
    evaluate_quality,
    evaluate_style_fidelity,
)
from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse

# Type aliases for cleaner annotations
EvaluationResult = Dict[str, Any]
EvaluationResults = List[EvaluationResult]
BatchEvaluationResults = List[EvaluationResults]


def evaluate(
    request: StyleTransferRequest,
    responses: Union[StyleTransferResponse, List[StyleTransferResponse]],
    provider: str = "openai",
    model: str = "gpt-4",
) -> Union[EvaluationResults, BatchEvaluationResults]:
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
