from werkzeug.datastructures import FileStorage
from src.enums.document_types import DocumentType
from src.classifiers.base_classifier import DocumentClassifier


class InvoiceClassifier(DocumentClassifier):

    def classify(self, file: FileStorage):
        filename = file.filename.lower()
        if "invoice" in filename:
            return DocumentType.INVOICE.value
