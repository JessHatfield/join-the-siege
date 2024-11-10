from enum import Enum


class DocumentType(Enum):
    DRIVERS_LICENSE = 'drivers_licence'
    BANK_STATEMENT = 'bank_statement'
    INVOICE = 'invoice'
    UNKNOWN_FILE = 'unknown file'


class SupportedFileTypes(Enum):
    PDF = 'application/pdf'
    JPG = 'image/jpeg'
    PNG = "image/png"

