from dataclasses import dataclass, field

from customer import Customer


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
