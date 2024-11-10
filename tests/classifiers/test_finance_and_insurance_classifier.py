import pytest
from werkzeug.datastructures import FileStorage

from src.classifiers.base_classifier import ClassifierResult
from src.classifiers.industries.finance_and_insurance_classifier import FinancialDocumentClassifier


def test_finance_and_insurance_classifier_returns_result(mocker):
    expected_result = ClassifierResult(industry='finance',
                                       label='test_label',
                                       confidence=0.98)

    mocker.patch('src.classifiers.industries.finance_and_insurance_classifier.deberta_v3_classifier',
                 return_value=expected_result)

    mocker.patch('src.classifiers.industries.finance_and_insurance_classifier.extract_text_from_file', return_value="")

    assert FinancialDocumentClassifier().classify(file=FileStorage()) == expected_result
