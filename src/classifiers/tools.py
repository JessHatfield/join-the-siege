import structlog
from transformers import pipeline
from src.classifiers.base_classifier import ClassifierResult

logger = structlog.getLogger(__name__)


def deberta_v3_classifier(extracted_text: str, candidate_labels: [str], industry: str) -> ClassifierResult:
    model_name = "MoritzLaurer/deberta-v3-large-zeroshot-v2.0"
    classifier = pipeline(model=model_name)
    result = classifier(extracted_text, candidate_labels, multi_label=False)
    # Classifier always returns the most likely label in position 0!
    logger.debug('classification_generated', model=model_name, results=result)

    return ClassifierResult(industry=industry,
                            label=result['labels'][0],
                            confidence=result['scores'][0])
