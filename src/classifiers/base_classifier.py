from abc import ABC

from werkzeug.datastructures import FileStorage

from src.enums.document_types import DocumentType


class DocumentClassifier(ABC):

    def classify(self, file: FileStorage) -> DocumentType:
        raise NotImplementedError
