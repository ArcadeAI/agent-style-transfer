#!/usr/bin/env python3
"""Unit tests for the writing style inferrer functionality."""

import pytest

from agent_style_transfer.schemas import (
    FewShotExample,
    StyleTransferRequest,
)
from agent_style_transfer.writing_style_inferrer import (
    infer_few_shot_examples,
    infer_style_rules,
)
from tests.conftest import load_fixture


@pytest.mark.vcr
def test_infer_style_rules():
    """Test style rules inference using fixture documents."""
    request = load_fixture("document-based-request", model=StyleTransferRequest)
    documents = []
    for ref_style in request.reference_style:
        if ref_style.documents:
            documents.extend(ref_style.documents)

    rules = infer_style_rules(documents, provider="anthropic")

    for rule in rules:
        assert isinstance(rule, str)


@pytest.mark.vcr
def test_infer_few_shot_examples():
    """Test few-shot examples inference using fixture documents."""
    request = load_fixture("document-based-request", model=StyleTransferRequest)
    documents = []
    for ref_style in request.reference_style:
        if ref_style.documents:
            documents.extend(ref_style.documents)

    examples = infer_few_shot_examples(documents, provider="anthropic")

    for example in examples:
        assert isinstance(example, FewShotExample)


@pytest.mark.vcr
def test_infer_style_rules_with_linkedin_documents():
    """Test style rules inference with LinkedIn-style documents."""
    request = load_fixture("linkedin-request", model=StyleTransferRequest)
    documents = []
    for ref_style in request.reference_style:
        if ref_style.documents:
            documents.extend(ref_style.documents)

    rules = infer_style_rules(documents, provider="anthropic")

    for rule in rules:
        assert isinstance(rule, str)
