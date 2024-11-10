import pytest

from src.classifiers.llama2_classifier import extract_document_type_from_prompt_response
from src.enums.document_types import DocumentType


def test_classifier_can_extract_text():
    prompt_returned = {
        "file_class": "doc_type: drivers_license"
    }

    doc_type = extract_document_type_from_prompt_response(prompt_returned)

    assert doc_type == DocumentType.DRIVERS_LICENSE
