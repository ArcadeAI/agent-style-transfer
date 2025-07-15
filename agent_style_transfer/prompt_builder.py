"""Prompt building utilities for style transfer."""

from agent_style_transfer.schemas import (
    Document,
    OutputSchema,
    ReferenceStyle,
)


def build_generation_prompt(
    output_schema: OutputSchema,
    reference_docs: list[ReferenceStyle],
    intent: str | None,
    focus: str,
    target_docs: list[Document],
) -> str:
    """Build a comprehensive prompt for content generation."""

    # NEW: Ensure all reference styles have complete style definitions
    enhanced_reference_docs = ensure_complete_style_definitions(reference_docs)

    style_info = extract_style_information(enhanced_reference_docs)

    target_info = extract_target_information(target_docs)

    writing_guidance = get_writing_guidance(output_schema.output_type)

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

## Writing Style Guidance:
{writing_guidance}

## Instructions:
1. Analyze the reference style characteristics carefully
2. Extract key information from the target content
3. Create content that matches the reference style while conveying the target
   content's message
4. Follow the writing style guidance above
5. Return the content in the exact format specified by the output schema
6. Maintain the original intent and focus while adapting to the new style

Please generate the content now:
"""

    return prompt


def get_writing_guidance(output_type: str) -> str:
    """Get writing style guidance for different output types."""
    guidance = {
        "tweet_single": (
            "Create engaging, concise content suitable for Twitter. "
            "Use hashtags appropriately and make it shareable."
        ),
        "tweet_thread": (
            "Create a connected series of tweets that tell a story. "
            "Number them and make each tweet engaging."
        ),
        "linkedin_post": (
            "Write professional but engaging content. Use bullet points "
            "for readability and end with a call-to-action."
        ),
        "linkedin_comment": (
            "Be professional and constructive. Add value to the "
            "conversation and keep it concise."
        ),
        "blog_post": (
            "Create comprehensive content with proper structure. "
            "Use markdown formatting and include relevant details."
        ),
    }

    return guidance.get(
        output_type,
        "Create well-structured, engaging content appropriate for the platform.",
    )


def extract_style_information(reference_docs: list[ReferenceStyle]) -> str:
    """Extract and format style information from reference documents."""
    style_info = []

    for i, ref_style in enumerate(reference_docs, 1):
        style_info.append(f"### Reference Style {i}: {ref_style.name}")

        if ref_style.description:
            style_info.append(f"Description: {ref_style.description}")

        if ref_style.style_definition:
            style_def = ref_style.style_definition
            style_info.append(f"Tone: {style_def.tone}")
            style_info.append(
                f"Formality Level: {style_def.formality_level:.1f} (0.0-1.0 scale)"
            )
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

            # NEW: Include style rules
            if style_def.style_rules:
                style_info.append("Style Rules:")
                for rule in style_def.style_rules:
                    style_info.append(f"  - {rule}")

            # NEW: Include few-shot examples
            if style_def.few_shot_examples:
                style_info.append("Examples:")
                for j, example in enumerate(style_def.few_shot_examples, 1):
                    style_info.append(f"  Example {j}:")
                    style_info.append(f"    Input: {example.input}")
                    style_info.append(f"    Output: {example.output}")
                    style_info.append("")

        if ref_style.documents:
            style_info.append(
                f"Reference Documents: {len(ref_style.documents)} documents"
            )
            for doc in ref_style.documents:
                style_info.append(f"  - {doc.title or 'Untitled'} ({doc.type.value})")

        style_info.append("")

    return "\n".join(style_info)


def extract_target_information(target_docs: list[Document]) -> str:
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

        if doc.content:
            target_info.append("Content:")
            target_info.append(doc.content)

        target_info.append("")

    return "\n".join(target_info)


def get_max_tokens(output_schema: OutputSchema) -> int:
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


def ensure_complete_style_definitions(
    reference_docs: list[ReferenceStyle],
) -> list[ReferenceStyle]:
    """
    Ensure all reference styles have complete style definitions.

    This agent's responsibility: if style_rules or few_shot_examples are missing,
    infer them from the provided documents.

    Args:
        reference_docs: List of reference styles to enhance

    Returns:
        List of enhanced reference styles with complete style definitions
    """
    enhanced_docs = []

    for ref_style in reference_docs:
        # Create a copy to avoid modifying the original
        enhanced_style = ref_style.model_copy()

        # Only enhance if we have documents to analyze
        if enhanced_style.documents:
            # If style_definition exists but is missing rules/examples, enhance it
            if enhanced_style.style_definition:
                style_def = enhanced_style.style_definition

                if not style_def.style_rules or not style_def.few_shot_examples:
                    print(
                        f"🔧 Inferring missing style components for '{enhanced_style.name}'..."
                    )

                    # Infer missing components from documents
                    from agent_style_transfer.writing_style_inferrer import (
                        infer_few_shot_examples,
                        infer_style_rules,
                    )

                    if not style_def.style_rules:
                        style_def.style_rules = infer_style_rules(
                            enhanced_style.documents
                        )

                    if not style_def.few_shot_examples:
                        style_def.few_shot_examples = infer_few_shot_examples(
                            enhanced_style.documents
                        )

            # If no style_definition exists, create one from documents
            elif not enhanced_style.style_definition:
                print(
                    f"🔧 Creating style definition for '{enhanced_style.name}' from documents..."
                )
                # Create a basic style definition
                from agent_style_transfer.schemas import WritingStyle
                from agent_style_transfer.writing_style_inferrer import (
                    infer_few_shot_examples,
                    infer_style_rules,
                )

                enhanced_style.style_definition = WritingStyle(
                    tone="neutral",
                    formality_level=0.5,
                    sentence_structure="varied",
                    vocabulary_level="moderate",
                    personality_traits=[],
                    writing_patterns={},
                    style_rules=infer_style_rules(enhanced_style.documents),
                    few_shot_examples=infer_few_shot_examples(enhanced_style.documents),
                )

        enhanced_docs.append(enhanced_style)

    return enhanced_docs
