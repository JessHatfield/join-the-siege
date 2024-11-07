from abc import ABC


class DocumentClassifier(ABC):

    def classify(self):
        raise NotImplementedError
