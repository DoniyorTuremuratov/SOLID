from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class AuthorizationError(Exception):
    pass


class InsufficientBalanceError(Exception):
    pass


@dataclass
class Customer:
    balance: float = 0.0

    def withdraw_balance(self, amount: float) -> bool:
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False


@dataclass
class OrderItem:
    name: str
    quantity: int
    price: float

    def calculate_price(self) -> float:
        return self.quantity * self.price


@dataclass
class Order:
    customer: Customer
    items: list[OrderItem] = field(default_factory=list)
    status: str = "open"

    def add_item(self, item: OrderItem):
        self.items.append(item)


class PricingService:
    @staticmethod
    def calculate_total_price(order: Order) -> float:
        return sum(item.calculate_price() for item in order.items)


class PaymentType(Enum):
    DEBIT = "debit"
    CREDIT = "credit"
    PAYPAL = "paypal"


def verify_security_code(security_code: int):
    print(f'Verifying security code: {"*" * len(str(security_code))}')


def verify_email_address(email_address: str):
    username, domain = email_address.split('@')
    masked_username = f"{'*' * (len(username) - 3)}{username[-3:]}@{domain}"
    print(f'Verifying email address: {masked_username}')


class Authorizer(ABC):

    @abstractmethod
    def is_authorized(self) -> bool:
        pass

    def authorize(self):
        if not self.is_authorized():
            raise AuthorizationError("Not authorized")


class SMSAuthorizer(Authorizer):
    def __init__(self):
        self.authorized = False

    def verify_mfa_code(self, code: int) -> None:
        print(f'Verifying SMS code: {code}')
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class GoogleAuthorizer(Authorizer):
    def __init__(self):
        self.authorized = False

    def verify_mfa_code(self, code: int) -> None:
        print(f'Verifying Google auth code: {code}')
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class RobotAuthorizer(Authorizer):
    def __init__(self):
        self.authorized = False

    def not_a_robot(self):
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class PaymentMethod(ABC):
    authorizer: Authorizer

    @abstractmethod
    def pay(self, order: Order):
        pass

    @staticmethod
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

    @staticmethod
    def _verify_and_process_payment(payment_type: PaymentType, order: Order, verification_function):
        authorizer.authorize()
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


item_1 = OrderItem(name="Laptop", quantity=5, price=1500)
item_2 = OrderItem(name="Speaker", quantity=3, price=1000)
item_3 = OrderItem(name="Keyboard", quantity=2, price=800)

customer = Customer(balance=20000)
order = Order(customer=customer)
order.add_item(item_1)
order.add_item(item_2)
order.add_item(item_3)
# print(f'Total price: ${PricingService.calculate_total_price(order)}')

authorizer = GoogleAuthorizer()
authorizer.verify_mfa_code(13216)
payment_method = PayPalPaymentMethod("doniyor_turemuratov@gmail.com", authorizer)
payment_method.pay(order)
