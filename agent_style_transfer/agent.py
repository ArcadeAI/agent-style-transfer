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


async def transfer_style(
    request: StyleTransferRequest,
    llm_provider: str = "google_genai",
    model: str | None = None,
    temperature: float = 0.7,
) -> list[StyleTransferResponse]:
    """Main interface for style transfer functionality with parallel processing.

    Args:
        request: Style transfer request with reference styles and target content
        llm_provider: Model provider (openai, anthropic, google_genai).
            Defaults to "google_genai".
        model: Model name. If None, will use provider defaults.
        temperature: Model temperature (0.0 to 1.0). Defaults to 0.7.

    Returns:
        List of style transfer responses
    """

    llm = get_llm(llm_provider, model=model, temperature=temperature)

    tasks = []
    for output_schema in request.target_schemas:
        task = process_target_schema(
            llm,
            output_schema,
            request.reference_style,
            request.intent,
            request.focus,
            request.target_content,
            llm_provider,
        )
        tasks.append(task)

    responses = await asyncio.gather(*tasks)

    return responses


async def process_target_schema(
    llm, output_schema, reference_style, intent, focus, target_content, llm_provider
) -> StyleTransferResponse:
    """Process a single schema asynchronously."""

    schema_class = output_schema.output_type.get_schema()

    structured_llm = llm.with_structured_output(schema_class, method="function_calling")

    prompt = build_generation_prompt(
        output_schema, reference_style, intent, focus, target_content, llm_provider
    )

    system_message = (
        "You are an expert content creator specializing in style transfer. "
        "Return the content in the exact format specified by the output schema."
    )

    messages = [SystemMessage(content=system_message), HumanMessage(content=prompt)]

    try:
        processed_content = await structured_llm.ainvoke(messages)
    except AttributeError:
        processed_content = structured_llm.invoke(messages)

    processed_content = processed_content.model_dump_json(indent=2)

    applied_style = reference_style[0].name if reference_style else "Unknown"

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
