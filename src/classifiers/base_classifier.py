import dataclasses
from abc import ABC

from werkzeug.datastructures import FileStorage

from src.enums import SupportedIndustries


@dataclasses.dataclass
class ClassifierResult:
    industry: SupportedIndustries
    label: str
    confidence: float


class DocumentClassifier(ABC):

    def classify(self, file: FileStorage) -> ClassifierResult:
        raise NotImplementedError
