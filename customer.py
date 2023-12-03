from dataclasses import dataclass


@dataclass
class Customer:
    balance: float = 0.0

    def withdraw_balance(self, amount: float) -> bool:
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False
