import pytest

from src.classifier import classify_file, ClassificationResults
from src.classifiers.base_classifier import ClassifierResult
from src.classifiers.finance_industry_document_classifier import FinancialDocumentType
from src.enums import SupportedIndustries, GenericDocumentTypes


def test_classifier_returns_classification_results(mocker):
    finance_classification_result = ClassifierResult(label='bank_statement', confidence=0.987654321,
                                                     industry=SupportedIndustries.FINANCE_AND_INSURANCE)

    mocker.patch('src.classifier.FinancialDocumentClassifier.classify',
                 return_value=finance_classification_result)

    result = classify_file(file=None)

    assert result == ClassificationResults(results=[finance_classification_result])


@pytest.mark.parametrize('confidence_score,expected_label', [(0.75, FinancialDocumentType.BANK_STATEMENT),
                                                             (0.45, GenericDocumentTypes.UNKNOWN_DOCUMENT_TYPE)])
def test_threshold_applied_when_returning_classification(mocker,confidence_score,expected_label):
    finance_classification_result = ClassifierResult(label='bank_statement', confidence=confidence_score,
                                                     industry=SupportedIndustries.FINANCE_AND_INSURANCE)

    mocker.patch('src.classifier.FinancialDocumentClassifier.classify',
                 return_value=finance_classification_result)

    result = classify_file(file=None)

    assert result.get_document_label() == expected_label.value

