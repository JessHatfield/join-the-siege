from werkzeug.datastructures import FileStorage

from src.classifiers.finance_industry_document_classifier import FinancialDocumentClassifier
from src.enums.document_types import DocumentType


def classify_file(file: FileStorage):
    classifiers = [FinancialDocumentClassifier()]

    # build a list of industry classifiers
    # store results
    # return result with highest confidence rating?

    for classifier in classifiers:
        document_type = classifier.classify(file=file)

    if document_type:
        return document_type

    # If we can't retrieve any classifications return hardcoded value
    return DocumentType.UNKNOWN_FILE.value
