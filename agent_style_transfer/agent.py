"""Style transfer agent with comprehensive parameters."""

from __future__ import annotations

import asyncio
from langchain.schema import HumanMessage, SystemMessage

from agent_style_transfer.llm_provider_setup import get_llm
from agent_style_transfer.prompt_builder import build_generation_prompt
from agent_style_transfer.schemas import (
    StyleTransferRequest,
    StyleTransferResponse,
)


async def transfer_style(request: StyleTransferRequest) -> list[StyleTransferResponse]:
    """Main interface for style transfer functionality with parallel processing."""
    
    # Get LLM provider once for all schemas
    llm = get_llm(request.llm_provider)
    
    # Create tasks for parallel processing
    tasks = []
    for output_schema in request.target_schemas:
        task = process_target_schema(
            llm, output_schema, request.reference_style, 
            request.intent, request.focus, request.target_content
        )
        tasks.append(task)
    
    # Execute all tasks concurrently
    responses = await asyncio.gather(*tasks)
    
    return responses


async def process_target_schema(
    llm, 
    output_schema, 
    reference_style, 
    intent, 
    focus, 
    target_content
) -> StyleTransferResponse:
    """Process a single schema asynchronously."""
    
    # Get the appropriate schema class
    schema_class = output_schema.output_type.get_schema()

    # Wrap LLM for structured output
    structured_llm = llm.with_structured_output(schema_class)

    # Build prompt and generate
    prompt = build_generation_prompt(
        output_schema, reference_style, intent, focus, target_content
    )

    system_message = (
        "You are an expert content creator specializing in style transfer. "
        "Return the content in the exact format specified by the output schema."
    )

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=prompt)
    ]

    # Use async invoke if available, otherwise fall back to sync
    try:
        processed_content = await structured_llm.ainvoke(messages)
    except AttributeError:
        # Fall back to synchronous invoke if async is not available
        processed_content = structured_llm.invoke(messages)

    # Convert to JSON string
    processed_content = processed_content.model_dump_json(indent=2)

    applied_style = (
        reference_style[0].name if reference_style else "Unknown"
    )

    return StyleTransferResponse(
        processed_content=processed_content,
        applied_style=applied_style,
        output_schema=output_schema,
        metadata={
            "reference_styles_count": len(reference_style),
            "target_documents_count": len(target_content),
            "focus": focus,
            "intent": intent,
            "schema_name": output_schema.name,
        },
    )
