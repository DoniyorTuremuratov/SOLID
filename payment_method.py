from abc import ABC, abstractmethod
from dataclasses import dataclass

from authorizer import Authorizer
from exceptions import InsufficientBalanceError
from order import Order
from payment import PricingService
from payment_type import PaymentType


def verify_security_code(security_code: int):
    print(f'Verifying security code: {"*" * len(str(security_code))}')


def verify_email_address(email_address: str):
    username, domain = email_address.split('@')
    masked_username = f"{'*' * (len(username) - 3)}{username[-3:]}@{domain}"
    print(f'Verifying email address: {masked_username}')


class PaymentMethod(ABC):
    def __init__(self, authorizer: Authorizer):
        self.authorizer = authorizer

    @abstractmethod
    def pay(self, order: Order):
        pass

    def _process_payment(payment_type: PaymentType, order: Order):
        if order.customer.withdraw_balance(PricingService.calculate_total_price(order)):
            print(f'Processing payment type: {payment_type.name}')
            order.status = 'paid'
            print("Payment successful! \n"
                  f"Remaining balance: ${order.customer.balance}")
        else:
            raise InsufficientBalanceError(
                f"Payment failed due to insufficient balance \nYour balance: ${order.customer.balance}"
            )

    def _verify_and_process_payment(self, payment_type: PaymentType, order: Order, verification_function):
        self.authorizer.authorize()
        verification_function()
        try:
            PaymentMethod._process_payment(payment_type, order)
        except InsufficientBalanceError as e:
            print(f"Insufficient Balance Error: {e}")


@dataclass
class DebitCardPaymentMethod(PaymentMethod):
    security_code: int
    authorizer: Authorizer

    def pay(self, order):
        verification_function: () = lambda: verify_security_code(self.security_code)
        self._verify_and_process_payment(PaymentType.DEBIT, order, verification_function)


@dataclass
class CreditCardPaymentMethod(PaymentMethod):
    security_code: int
    authorizer: Authorizer

    def pay(self, order):
        verification_function: () = lambda: verify_security_code(self.security_code)
        self._verify_and_process_payment(PaymentType.DEBIT, order, verification_function)


@dataclass
class PayPalPaymentMethod(PaymentMethod):
    email_address: str
    authorizer: Authorizer

    def pay(self, order):
        verification_function: () = lambda: verify_email_address(self.email_address)
        self._verify_and_process_payment(PaymentType.DEBIT, order, verification_function)
