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
    
    # Get original content, fallback to title and metadata if content is not available
    original_content = request.target_content[0]
    if original_content.content:
        original_text = original_content.content
    else:
        # Use title and metadata as proxy for original content
        original_text = f"Title: {original_content.title or 'Untitled'}"
        if original_content.metadata:
            original_text += f"\nMetadata: {original_content.metadata}"
    
    return generated_text, original_text


def create_llm_evaluator(prompt: str, feedback_key: str, model: str = "openai:o3-mini"):
    """Create an LLM evaluator with the given prompt.
    
    Supports both OpenEval's native format and the same model factory approach as the AI tool.
    
    Args:
        prompt: The evaluation prompt
        feedback_key: Key for the feedback
        model: Model identifier. Can be:
            - OpenEval format: "openai:o3-mini", "anthropic:claude-3-haiku-20240307", etc.
            - AI tool format: "openai:gpt-4", "anthropic:claude-3-haiku-20240307", etc.
    """
    # Map AI tool model names to OpenEval format
    model_mapping = {
        # OpenAI models
        "openai:gpt-4": "openai:gpt-4",
        "openai:gpt-3.5-turbo": "openai:gpt-3.5-turbo",
        "openai:gpt-4-turbo": "openai:gpt-4-turbo",
        # Anthropic models
        "anthropic:claude-3-haiku-20240307": "anthropic:claude-3-haiku-20240307",
        "anthropic:claude-3-sonnet-20240229": "anthropic:claude-3-sonnet-20240229",
        "anthropic:claude-3-opus-20240229": "anthropic:claude-3-opus-20240229",
        # Google models - OpenEval uses different format for Google models
        "google:gemini-1.5-flash": "gemini-1.5-flash",
        "google:gemini-1.5-pro": "gemini-1.5-pro",
        "google:gemini-pro": "gemini-pro",
    }
    
    # Use mapped model if available, otherwise use the original model string
    mapped_model = model_mapping.get(model, model)
    
    return create_llm_as_judge(prompt=prompt, model=mapped_model, feedback_key=feedback_key)
