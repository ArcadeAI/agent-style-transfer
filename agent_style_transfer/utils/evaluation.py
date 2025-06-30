"""Evaluation utility functions."""

from functools import wraps
from typing import Any, Callable, Dict

from openevals.llm import create_llm_as_judge

from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse
from agent_style_transfer.utils.content_extractor import extract_content


def safe_evaluation(evaluation_name: str):
    """Decorator to handle errors in evaluation functions."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Dict[str, Any]:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return {
                    "key": evaluation_name,
                    "score": 0,
                    "comment": f"Evaluation failed: {e!s}",
                }

        return wrapper

    return decorator


def format_result(key: str, score: float, comment: str) -> Dict[str, Any]:
    """Format evaluation result consistently."""
    return {"key": key, "score": score, "comment": comment or "No comment provided"}


def get_text_content(
    request: StyleTransferRequest, response: StyleTransferResponse
) -> tuple[str, str]:
    """Extract generated and original text content."""
    generated_text = extract_content(response.processed_content, response.output_schema)
    original_text = request.target_content[0].content or ""
    return generated_text, original_text


def create_llm_evaluator(prompt: str, feedback_key: str, model: str = "openai:o3-mini"):
    """Create an LLM evaluator with the given prompt."""
    return create_llm_as_judge(prompt=prompt, model=model, feedback_key=feedback_key)
