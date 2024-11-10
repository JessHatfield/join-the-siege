from enum import Enum


class FinancialDocumentType(Enum):
    DRIVERS_LICENSE = 'drivers_licence'
    BANK_STATEMENT = 'bank_statement'
    INVOICE = 'invoice'


class SupportedFileTypes(Enum):
    PDF = 'application/pdf'
    JPG = 'image/jpeg'
    PNG = "image/png"

