"""Decorator Pattern: compose optional order features without boolean flags."""
from abc import ABC, abstractmethod


class OrderComponent(ABC):
    """Common interface for a base order and all order decorators."""

    @abstractmethod
    def get_cost(self) -> float:
        """Return the total cost."""

    @abstractmethod
    def get_description(self) -> str:
        """Return a human-readable description."""


class BaseOrder(OrderComponent):
    def __init__(self, base_price: float):
        if base_price < 0:
            raise ValueError("Base price cannot be negative")
        self._base_price = float(base_price)

    def get_cost(self) -> float:
        return self._base_price

    def get_description(self) -> str:
        return f"Base order: €{self._base_price:.2f}"


class OrderDecorator(OrderComponent):
    """Base decorator that delegates to the wrapped order component."""

    def __init__(self, order: OrderComponent):
        self._order = order

    def get_cost(self) -> float:
        return self._order.get_cost()

    def get_description(self) -> str:
        return self._order.get_description()


class ExpressShippingDecorator(OrderDecorator):
    SHIPPING_COST = 15.00

    def get_cost(self) -> float:
        return self._order.get_cost() + self.SHIPPING_COST

    def get_description(self) -> str:
        return f"{self._order.get_description()}\nExpress shipping: +€{self.SHIPPING_COST:.2f}"


class InsuranceDecorator(OrderDecorator):
    INSURANCE_RATE = 0.05

    def get_cost(self) -> float:
        return self._order.get_cost() * (1 + self.INSURANCE_RATE)

    def get_description(self) -> str:
        insurance = self._order.get_cost() * self.INSURANCE_RATE
        return f"{self._order.get_description()}\nInsurance (5%): +€{insurance:.2f}"


class GiftWrapDecorator(OrderDecorator):
    WRAP_COST = 5.00

    def get_cost(self) -> float:
        return self._order.get_cost() + self.WRAP_COST

    def get_description(self) -> str:
        return f"{self._order.get_description()}\nGift wrap: +€{self.WRAP_COST:.2f}"


class DiscountDecorator(OrderDecorator):
    def __init__(self, order: OrderComponent, discount_percent: float):
        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount must be between 0 and 100 percent")
        super().__init__(order)
        self._discount_percent = discount_percent

    def get_cost(self) -> float:
        return self._order.get_cost() * (1 - self._discount_percent / 100)

    def get_description(self) -> str:
        discount = self._order.get_cost() * self._discount_percent / 100
        return (f"{self._order.get_description()}\n"
                f"Discount ({self._discount_percent:g}%): -€{discount:.2f}")


class PremiumMemberDecorator(OrderDecorator):
    DISCOUNT_RATE = 0.10

    def get_cost(self) -> float:
        return self._order.get_cost() * (1 - self.DISCOUNT_RATE)

    def get_description(self) -> str:
        discount = self._order.get_cost() * self.DISCOUNT_RATE
        return f"{self._order.get_description()}\nPremium member (10%): -€{discount:.2f}"


if __name__ == "__main__":
    order = PremiumMemberDecorator(
        DiscountDecorator(
            GiftWrapDecorator(
                InsuranceDecorator(ExpressShippingDecorator(BaseOrder(100.00)))
            ),
            15,
        )
    )
    print(order.get_description())
    print(f"TOTAL: €{order.get_cost():.2f}")
