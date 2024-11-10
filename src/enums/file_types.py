from enum import Enum

class GenericDocumentTypes(Enum):
    UNKNOWN_DOCUMENT_TYPE='unknown_document_type'

class SupportedFileTypes(Enum):
    PDF = 'application/pdf'
    JPG = 'image/jpeg'
    PNG = "image/png"

