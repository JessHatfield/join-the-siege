import dataclasses

from werkzeug.datastructures import FileStorage

from src.classifiers.base_classifier import ClassifierResult
from src.classifiers.finance_industry_document_classifier import FinancialDocumentClassifier
from src.enums.file_types import GenericDocumentTypes


@dataclasses.dataclass
class ClassificationResults:
    results: [ClassifierResult]

    def get_document_label(self):

        highest_score = 0
        label = GenericDocumentTypes.UNKNOWN_DOCUMENT_TYPE

        for result in self.results:
            if result.score > highest_score:
                highest_score = result.score
                label = result.label

        return label


def classify_file(file: FileStorage):
    classifiers = [FinancialDocumentClassifier()]
    results = ClassificationResults()

    for classifier in classifiers:
        results.append(classifier.classify(file=file))

    return results.get_document_label()
