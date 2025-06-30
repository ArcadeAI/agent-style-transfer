"""Content extraction utilities for style transfer schemas."""

import json

from agent_style_transfer.schemas import OutputSchema
from agent_style_transfer.utils.pydantic_utils import get_text_fields


def extract_content(content_json: str, output_schema: OutputSchema) -> str:
    """Extract content from JSON output based on the output schema.

    Args:
        content_json: JSON string containing the schema output
        output_schema: The output schema object that defines the structure

    Returns:
        Extracted text content as a string

    Raises:
        json.JSONDecodeError: If content_json is not valid JSON
    """
    try:
        content_data = json.loads(content_json)

        # Use the schema's output_type to determine extraction strategy
        output_type = output_schema.output_type

        # Get the schema class for this output type
        schema_class = output_type.get_schema()

        # Get the schema field names that contain text content
        text_fields = get_text_fields(schema_class)

        # Extract text from the identified fields
        extracted_parts = []
        for field_name in text_fields:
            if field_name in content_data:
                value = content_data[field_name]
                if isinstance(value, str) and value.strip():
                    extracted_parts.append(value.strip())
                elif isinstance(value, list):
                    # Handle list fields (like tweets in a thread)
                    list_texts = []
                    for item in value:
                        if isinstance(item, dict) and "text" in item:
                            list_texts.append(item["text"])
                    if list_texts:
                        extracted_parts.append("\n\n".join(list_texts))

        if extracted_parts:
            return "\n\n".join(extracted_parts)
        else:
            # Fallback for unknown types or empty content
            return str(content_data)

    except (json.JSONDecodeError, KeyError):
        return content_json
