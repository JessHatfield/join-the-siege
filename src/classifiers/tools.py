from transformers import pipeline

from src.classifiers.base_classifier import DocumentClassifier, ClassifierResult


class DebertaV3Classifier(DocumentClassifier):

    def __init__(self):
        self.classifier = pipeline(model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")

    def classify(self, extracted_text: str, candidate_labels: [str],industry:str) -> ClassifierResult:
        result = self.classifier(extracted_text, candidate_labels, multi_label=False)
        # Classifier always returns the most likely label in position 0!
        return ClassifierResult(industry=industry,
                         label=result['labels'[0]],
                         confidence=result['scores'][0])
