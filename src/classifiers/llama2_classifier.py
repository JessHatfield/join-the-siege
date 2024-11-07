import magic
from werkzeug.datastructures import FileStorage

from langchain_ollama import OllamaLLM
from src.classifiers.base_classifier import DocumentClassifier
from src.classifiers.utils import extract_text_from_image



class Llama2DocumentClassifier(DocumentClassifier):

    def classify(self, file: FileStorage):
        # Usage

        type = magic.from_buffer(open(file, "rb").read(2048))

        image_path = 'driving_licenses/drivers_license_1.jpg'
        extracted_text = extract_text_from_image(image_path)
        print(extracted_text)

        llm = OllamaLLM(model="llama3.2:1b")
        response = llm.invoke(f""""
                You are a document classifier, your task is to read text I give you and tell me if you think this text is from 
                a drivers license, 
                a bank statement 
                an invoice. 
                Please return your answer in this format  'doc_type':value . Where document_type is either
                drivers_license,bank_statement or invoice

                Here is text I want you to classify

                {extracted_text}

        """)

        return response
