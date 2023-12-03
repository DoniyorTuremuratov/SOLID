from enum import Enum, auto


class PaymentType(Enum):
    DEBIT = auto()
    CREDIT = auto()
    PAYPAL = auto()