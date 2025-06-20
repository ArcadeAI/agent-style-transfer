"""Style transfer agent with comprehensive parameters."""

from __future__ import annotations

import os

from arcadepy import Arcade

from agent_style_transfer.schemas import (
    Document,
    OutputSchema,
    ReferenceStyle,
    StyleTransferRequest,
    StyleTransferResponse,
)


def transfer_style(request: StyleTransferRequest) -> StyleTransferResponse:
    """Main interface for style transfer functionality.

    Args:
        request: Complete style transfer request containing reference styles,
                target content, and output schemas.

    Returns:
        StyleTransferResponse: Processed content with applied style information.

    Raises:
        ValueError: If ARCADE_API_KEY is not set or request validation fails.
    """
    # Validate request
    if not request.reference_style:
        raise ValueError("At least one reference style must be provided")

    if not request.target_content:
        raise ValueError("At least one target content document must be provided")

    # Require at least one output schema
    if not request.target_schemas:
        raise ValueError("At least one target schema must be provided")

    # Use the first output schema
    output_schema = request.target_schemas[0]

    # Generate content using the helper function
    processed_content = _generate_content(
        output_schema=output_schema,
        reference_docs=request.reference_style,
        intent=request.intent,
        focus=request.focus,
        target_docs=request.target_content,
    )

    # Determine the applied style name
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


def _generate_content(
    output_schema: OutputSchema,
    reference_docs: list[ReferenceStyle],
    intent: str | None,
    focus: str,
    target_docs: list[Document],
) -> str:
    """Generate content using Arcade client."""
    # Initialize Arcade client
    arcade_api_key = os.environ.get("ARCADE_API_KEY")

    if not arcade_api_key:
        raise ValueError("ARCADE_API_KEY environment variable is required")

    arcade = Arcade(api_key=arcade_api_key)

    # Build the prompt based on output schema type
    prompt = _build_generation_prompt(
        output_schema, reference_docs, intent, focus, target_docs
    )

    # Generate content using Arcade
    response = arcade.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert content creator specializing in style transfer. "
                    "You adapt content to match specific writing styles while "
                    "maintaining the original message and intent."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=_get_max_tokens(output_schema),
    )

    return response.choices[0].message.content.strip()


def _build_generation_prompt(
    output_schema: OutputSchema,
    reference_docs: list[ReferenceStyle],
    intent: str | None,
    focus: str,
    target_docs: list[Document],
) -> str:
    """Build a comprehensive prompt for content generation."""

    # Extract style information from reference documents
    style_info = _extract_style_information(reference_docs)

    # Extract target content information
    target_info = _extract_target_information(target_docs)

    # Build output format instructions
    format_instructions = _build_format_instructions(output_schema)

    prompt = f"""
You are tasked with creating content that transfers the style from reference
materials to target content.

## Reference Style Information:
{style_info}

## Target Content Information:
{target_info}

## Intent and Focus:
- Intent: {intent or "Not specified"}
- Focus: {focus}

## Output Requirements:
{format_instructions}

## Instructions:
1. Analyze the reference style characteristics carefully
2. Extract key information from the target content
3. Create content that matches the reference style while conveying the target
   content's message
4. Ensure the output follows the specified format and constraints
5. Maintain the original intent and focus while adapting to the new style

Please generate the content now:
"""

    return prompt


def _extract_style_information(reference_docs: list[ReferenceStyle]) -> str:
    """Extract and format style information from reference documents."""
    style_info = []

    for i, ref_style in enumerate(reference_docs, 1):
        style_info.append(f"### Reference Style {i}: {ref_style.name}")

        if ref_style.description:
            style_info.append(f"Description: {ref_style.description}")

        if ref_style.style_definition:
            style_def = ref_style.style_definition
            style_info.append(f"Tone: {style_def.tone}")
            style_info.append(f"Formality Level: {style_def.formality_level}/10")
            style_info.append(f"Sentence Structure: {style_def.sentence_structure}")
            style_info.append(f"Vocabulary Level: {style_def.vocabulary_level}")

            if style_def.personality_traits:
                style_info.append(
                    f"Personality Traits: {', '.join(style_def.personality_traits)}"
                )

            if style_def.writing_patterns:
                style_info.append("Writing Patterns:")
                for pattern, value in style_def.writing_patterns.items():
                    style_info.append(f"  - {pattern}: {value}")

        if ref_style.documents:
            style_info.append(
                f"Reference Documents: {len(ref_style.documents)} documents"
            )
            for doc in ref_style.documents:
                style_info.append(f"  - {doc.title or 'Untitled'} ({doc.type.value})")

        style_info.append("")  # Empty line for separation

    return "\n".join(style_info)


def _extract_target_information(target_docs: list[Document]) -> str:
    """Extract and format target content information."""
    target_info = []

    for i, doc in enumerate(target_docs, 1):
        target_info.append(f"### Target Document {i}")
        target_info.append(f"Title: {doc.title or 'Untitled'}")
        target_info.append(f"Type: {doc.type.value}")
        target_info.append(f"Category: {doc.category.value}")
        target_info.append(f"Author: {doc.author or 'Unknown'}")

        if doc.date_published:
            target_info.append(f"Date: {doc.date_published}")

        if doc.metadata:
            target_info.append("Metadata:")
            for key, value in doc.metadata.items():
                target_info.append(f"  - {key}: {value}")

        target_info.append("")  # Empty line for separation

    return "\n".join(target_info)


def _build_format_instructions(output_schema: OutputSchema) -> str:
    """Build format-specific instructions based on output schema."""
    output_type = output_schema.output_type

    format_instructions = {
        "tweet_single": """
- Create a single tweet (max 280 characters)
- Use engaging, concise language
- Include relevant hashtags if appropriate
- Make it shareable and engaging
- Follow Twitter best practices
""",
        "tweet_thread": """
- Create a thread of 3-5 tweets
- Number each tweet (1/3, 2/3, etc.)
- Make each tweet engaging and connected
- Include relevant hashtags
- End with a call-to-action or conclusion
""",
        "linkedin_post": """
- Create a professional LinkedIn post
- Use professional but engaging tone
- Include bullet points for readability
- Add relevant hashtags
- End with a thought-provoking question or call-to-action
""",
        "linkedin_comment": """
- Create a concise LinkedIn comment
- Be professional and constructive
- Add value to the conversation
- Keep it under 200 characters if possible
""",
        "blog_post": """
- Create a comprehensive blog post in markdown format
- Include a compelling title
- Use proper headings (H1, H2, H3)
- Include introduction, body, and conclusion
- Add relevant tags and categories
- Use markdown formatting for emphasis and structure
""",
    }

    base_instructions = format_instructions.get(
        output_type, format_instructions["blog_post"]
    )

    # Add length constraints
    if output_schema.max_length:
        base_instructions += f"\n- Maximum length: {output_schema.max_length} words"
    if output_schema.min_length:
        base_instructions += f"\n- Minimum length: {output_schema.min_length} words"

    return base_instructions


def _get_max_tokens(output_schema: OutputSchema) -> int:
    """Determine appropriate max_tokens based on output schema."""
    output_type = output_schema.output_type

    token_limits = {
        "tweet_single": 100,
        "tweet_thread": 500,
        "linkedin_post": 300,
        "linkedin_comment": 150,
        "blog_post": 2000,
    }

    return token_limits.get(output_type, 2000)
