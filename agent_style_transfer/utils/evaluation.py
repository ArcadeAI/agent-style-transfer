"""Evaluation utility functions."""

from typing import Any

from agent_style_transfer.llm_provider_setup import get_llm
from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse
from agent_style_transfer.utils.content_extractor import extract_content


def format_result(key: str, score: float, comment: str) -> dict[str, Any]:
    """Format evaluation result consistently."""
    return {"key": key, "score": score, "comment": comment or "No comment provided"}


def get_text_content(
    request: StyleTransferRequest, response: StyleTransferResponse
) -> tuple[str, str]:
    """Extract generated and original text content."""
    generated_text = extract_content(response.processed_content, response.output_schema)

    # Get original content, return empty string if content is not available
    original_content = request.target_content[0]
    original_text = original_content.content or ""

    return generated_text, original_text


def create_llm_evaluator(
    prompt: str, feedback_key: str, provider: str = "openai", model: str = "gpt-4"
):
    """Create an LLM evaluator with the given prompt.

    Uses our get_llm() method instead of OpenEval, but maintains the same interface
    and return format that OpenEval expects.

    Args:
        prompt: The evaluation prompt
        feedback_key: Key for the feedback (used in return format)
        provider: Model provider (openai, anthropic, google_genai)
        model: Model name (e.g., "gpt-4", "claude-3-haiku-20240307")
    """

    def evaluator(outputs, reference_outputs=None, **kwargs):
        """Evaluator function that mimics OpenEval's interface."""
        try:
            # Get LLM instance using unified format
            llm = get_llm(provider, model, temperature=0.1)

            # Create the full prompt with the outputs
            full_prompt = f"{prompt}\n\nOutput: {outputs}"
            if reference_outputs:
                full_prompt += f"\nReference: {reference_outputs}"

            # Get evaluation response
            response = llm.invoke(full_prompt)
            evaluation_text = response.content

            # Extract score from response (look for number 0-5)
            import re

            score_match = re.search(r"(\d+(?:\.\d+)?)", evaluation_text)
            score = float(score_match.group(1)) if score_match else 2.5

            # Ensure score is within 0-5 range
            normalized_score = min(max(score, 0.0), 5.0)

            # Return in OpenEval format
            return {"score": normalized_score, "comment": evaluation_text.strip()}

        except Exception as e:
            return {"score": 0.0, "comment": f"Evaluation failed: {e!s}"}

    return evaluator
