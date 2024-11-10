# import os
# from typing import Type
#
# from llama_cpp import Llama
# from werkzeug.datastructures import FileStorage
#
# from src.classifiers.base_classifier import DocumentClassifier
# from src.classifiers.utils import extract_text_from_file
# from src.enums.document_types import DocumentType
#
#
# def extract_document_type_from_prompt_response(response: str) -> Type[DocumentType]:
#     return
#
#
# class Llama2DocumentClassifier(DocumentClassifier):
#
#     def __init__(self):
#         self.__llm = Llama(model_path=f'{os.getcwd()}/src/classifiers/Llama-3.2-3B-Instruct-uncensored.IQ3_M.gguf',
#                            n_ctx=512, n_threads=4)
#
#     def classify(self, file: FileStorage):
#         extracted_text = extract_text_from_file(file, file.mimetype)
#
#         print("extracted_text_is", extracted_text)
#
#         orignal_prompt = f""""
#                 You are a document classifier, your task is to classify the text I give you and return the document classification in a JSON format with a key 'document_type'
#
#                 There are only four possible document types. These are 'driving_license','bank_statement','invoice'
#
#
#                 Here is text I want you to classify
#
#                 {extracted_text}
#
#         """
#
#         response = self.__llm(f""""
#         IMPORTANT: Follow these instructions carefully
#         Question: Is the text from a drivers license, invoice or bank statement?
#         Instructions: Provide only the type of document as your answer, do not include any additional information or explanation, you can return one of the following document types, drivers_license,bank_statement,invoice
#         Answer:
#
#         Text:{extracted_text}
#
#         """, max_tokens=150)
#         # TO DO
#         # ADD LOGIC TO EXTRACT RESULT, IF RESULT DOES NOT MATCH FORMAT OR IS TOO LONG THEN RAISE ERROR
#
#         return response
