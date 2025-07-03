"""General-purpose utilities for working with Pydantic models."""

from typing import Union, get_args, get_origin

from pydantic import BaseModel


def get_text_fields(schema_class: type[BaseModel]) -> list[str]:
    """Get all string fields from a Pydantic schema class."""
    return [
        field_name
        for field_name, field_info in schema_class.model_fields.items()
        if is_text_field(field_info.annotation)
    ]


def is_text_field(annotation) -> bool:
    """Check if a type annotation represents a text field."""
    if annotation is str:
        return True

    origin = get_origin(annotation)
    args = get_args(annotation)

    # Optional[str] or Union[str, None]
    if origin is Union and str in args:
        return True

    # List[str] or similar
    return bool(origin is list and args and args[0] is str)
