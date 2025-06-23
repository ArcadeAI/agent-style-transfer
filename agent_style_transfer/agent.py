"""Style transfer agent with comprehensive parameters."""

from __future__ import annotations

from langchain.schema import HumanMessage, SystemMessage

from agent_style_transfer.llm_provider_setup import get_llm
from agent_style_transfer.prompt_builder import build_generation_prompt
from agent_style_transfer.schemas import (
    StyleTransferRequest,
    StyleTransferResponse,
)


def transfer_style(request: StyleTransferRequest) -> StyleTransferResponse:
    """Main interface for style transfer functionality."""
    output_schema = request.target_schemas[0]

    # Get the appropriate schema class
    schema_class = output_schema.output_type.get_schema()

    # Get LLM provider and wrap for structured output
    llm = get_llm(request.llm_provider)
    structured_llm = llm.with_structured_output(schema_class, method="json_mode")

    # Build prompt and generate
    prompt = build_generation_prompt(
        output_schema, request.reference_style, request.intent,
        request.focus, request.target_content
    )

    system_message = (
        "You are an expert content creator specializing in style transfer. "
        "Return the content in the exact format specified by the output schema."
    )

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=prompt)
    ]

    processed_content = structured_llm.invoke(messages)

    # Convert to JSON string
    processed_content = processed_content.model_dump_json(indent=2)

    applied_style = (
        request.reference_style[0].name if request.reference_style else "Unknown"
    )

    return StyleTransferResponse(
        processed_content=processed_content,
        applied_style=applied_style,
        output_schema=output_schema,
        metadata={
            "reference_styles_count": len(request.reference_style),
            "target_documents_count": len(request.target_content),
            "focus": request.focus,
            "intent": request.intent,
        },
    )
