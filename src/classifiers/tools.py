from transformers import pipeline

from src.classifiers.base_classifier import ClassifierResult


def deberta_v3_classifier(extracted_text: str, candidate_labels: [str], industry:str) -> ClassifierResult:
    classifier = pipeline(model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")
    result = classifier(extracted_text, candidate_labels, multi_label=False)
    # Classifier always returns the most likely label in position 0!
    return ClassifierResult(industry=industry,
                     label=result['labels'[0]],
                     confidence=result['scores'][0])


