from werkzeug.datastructures import FileStorage
from src.enums.document_types import DocumentType
from src.classifiers.base_classifier import DocumentClassifier


class BankStatementClassifier(DocumentClassifier):

    def classify(self, file: FileStorage):
        filename = file.filename.lower()
        if "bank_statement" in filename:
            return DocumentType.BANK_STATEMENT.value
