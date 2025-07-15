"""Writing style inference utilities for extracting style rules and examples from documents."""

from agent_style_transfer.llm_provider_setup import get_llm
from agent_style_transfer.schemas import Document, FewShotExample


def infer_style_rules(
    documents: list[Document], provider: str = "google_genai", model: str = None
) -> list[str]:
    """
    Infer style rules from a list of documents using LLM analysis.

    Args:
        documents: List of reference documents to analyze
        provider: LLM provider (openai, anthropic, google_genai)
        model: Model name (optional, uses provider default)

    Returns:
        List of style rules inferred from the documents
    """
    if not documents:
        return []

    # Get LLM instance
    llm = get_llm(provider, model, temperature=0.3)

    # Combine document content for analysis
    combined_content = "\n\n".join(
        [
            f"Title: {doc.title}\nContent: {doc.content[:300]}..."
            for doc in documents
            if doc.title and doc.content
        ]
    )

    if not combined_content:
        return []

    # Create a prompt to analyze writing style patterns
    prompt = (
        """
    Analyze these documents and extract 3-5 specific writing style rules.

    Documents:
    """
        + f"{combined_content}\n\n"
        + """
    Identify the key writing style characteristics and create clear, actionable rules.
    Focus on tone, structure, vocabulary, and writing patterns.

    Format your response as a simple list, one rule per line:
    - [Rule 1]
    - [Rule 2]
    - [Rule 3]
    """
    )

    try:
        response = llm.invoke(prompt)
        content = response.content

        # Parse the response to extract rules
        rules = []
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("-") or line.startswith("•"):
                rule = line[1:].strip()
                if rule:
                    rules.append(rule)

        return rules

    except Exception:
        # Return empty list if LLM fails
        return []


def infer_few_shot_examples(
    documents: list[Document], provider: str = "google_genai", model: str = None
) -> list[FewShotExample]:
    """
    Infer few-shot examples from a list of documents using LLM analysis.

    Args:
        documents: List of reference documents to analyze
        provider: LLM provider (openai, anthropic, google_genai)
        model: Model name (optional, uses provider default)

    Returns:
        List of few-shot examples inferred from the documents
    """
    if not documents:
        return []

    # Get LLM instance
    llm = get_llm(provider, model, temperature=0.3)

    examples = []

    # Analyze each document to create meaningful examples
    for doc in documents:
        if doc.title and doc.content:
            # Create a prompt to analyze the writing style
            prompt = (
                """
            Analyze this document and create a few-shot example that demonstrates its writing style.

            Document Title: """
                + f"{doc.title}\n"
                + "Document Content: "
                + f"{doc.content[:500]}...\n\n"
                + """
            Create a simple input-output pair that shows how to write in this style.
            The input should be a generic topic, and the output should demonstrate the same writing style.

            Format your response as:
            Input: [generic topic]
            Output: [content in the same style]

            Keep the output concise (100-200 words) and focus on capturing the writing style.
            """
            )

            try:
                response = llm.invoke(prompt)
                content = response.content

                # Parse the response to extract input and output
                lines = content.split("\n")
                input_text = ""
                output_text = ""

                for line in lines:
                    if line.strip().startswith("Input:"):
                        input_text = line.replace("Input:", "").strip()
                    elif line.strip().startswith("Output:"):
                        output_text = line.replace("Output:", "").strip()

                if input_text and output_text:
                    examples.append(
                        FewShotExample(input=input_text, output=output_text)
                    )

            except Exception:
                # Fallback to simple example if LLM fails
                input_text = f"Content about {doc.title.lower()}"
                output_text = (
                    doc.content[:200] + "..." if len(doc.content) > 200 else doc.content
                )

                examples.append(FewShotExample(input=input_text, output=output_text))

    return examples
