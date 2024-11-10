import dataclasses

from werkzeug.datastructures import FileStorage

from src.classifiers.base_classifier import ClassifierResult
from src.classifiers.industries.finance_and_insurance_classifier import FinancialDocumentClassifier
from src.enums import GenericDocumentTypes

# In prod this would be replaced by a settings value stored in a DB or settings file
CONFIDENCE_THRESHOLD = 0.75


@dataclasses.dataclass
class ClassificationResults:
    results: [ClassifierResult] = list

    def get_document_label(self):
        highest_confidence_score = 0
        label = GenericDocumentTypes.UNKNOWN_DOCUMENT_TYPE.value
        for result in self.results:
            if result.confidence > highest_confidence_score and result.confidence>=CONFIDENCE_THRESHOLD:
                highest_confidence_score = result.confidence
                label = result.label

        return label


def classify_file(file: FileStorage) -> ClassificationResults:
    classifiers = [FinancialDocumentClassifier()]
    results = []

    for classifier in classifiers:
        results.append(classifier.classify(file=file))

    return ClassificationResults(results=results)
