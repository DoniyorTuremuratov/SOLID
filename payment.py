from order import Order


class PricingService:
    @staticmethod
    def calculate_total_price(order: Order) -> float:
        return sum(item.calculate_price() for item in order.items)
