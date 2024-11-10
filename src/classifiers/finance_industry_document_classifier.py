from werkzeug.datastructures import FileStorage

from src.classifiers.base_classifier import DocumentClassifier, ClassifierResult
from src.classifiers.tools import DebertaV3Classifier
from src.classifiers.utils import extract_text_from_file
from src.enums.document_types import FinancialDocumentType


class FinancialDocumentClassifier(DocumentClassifier):

    def __init__(self):
        self.__classifier = DebertaV3Classifier()
        self.__candidate_labels = [doc_type.value for doc_type in FinancialDocumentType]

    def classify(self, file: FileStorage) -> ClassifierResult:
        extracted_text = extract_text_from_file(file, file.mimetype)

        return self.__classifier.classify(extracted_text=extracted_text, candidate_labels=self.__candidate_labels)
