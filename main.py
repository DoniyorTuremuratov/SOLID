from authorizer import GoogleAuthorizer
from customer import Customer
from order import OrderItem, Order
from payment_method import PayPalPaymentMethod

if __name__ == "__main__":
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
