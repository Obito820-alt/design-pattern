"""Factory Pattern example: extensible payment processing."""
from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Common interface for every payment processor."""

    @abstractmethod
    def validate(self, details: dict) -> bool:
        """Return True when the payment details are valid."""

    @abstractmethod
    def process(self, amount: float, details: dict) -> dict:
        """Validate and process a payment, returning a result dictionary."""


class CreditCardProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        card_number = str(details.get("card_number", ""))
        cvv = str(details.get("cvv", ""))
        return len(card_number) == 16 and card_number.isdigit() and len(cvv) == 3 and cvv.isdigit()

    def process(self, amount: float, details: dict) -> dict:
        if amount < 0:
            return {"success": False, "error": "Amount cannot be negative"}
        if not self.validate(details):
            return {"success": False, "error": "Invalid card number or CVV"}
        fee = amount * 0.029
        return {"success": True, "method": "credit_card", "amount": amount + fee, "fee": fee}


class BankTransferProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        iban = details.get("iban", "")
        return isinstance(iban, str) and len(iban) >= 15

    def process(self, amount: float, details: dict) -> dict:
        if amount < 0:
            return {"success": False, "error": "Amount cannot be negative"}
        if not self.validate(details):
            return {"success": False, "error": "Invalid IBAN"}
        fee = 1.50
        return {"success": True, "method": "bank_transfer", "amount": amount + fee, "fee": fee}


class PayPalProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        email = details.get("email", "")
        return isinstance(email, str) and "@" in email

    def process(self, amount: float, details: dict) -> dict:
        if amount < 0:
            return {"success": False, "error": "Amount cannot be negative"}
        if not self.validate(details):
            return {"success": False, "error": "Invalid PayPal email"}
        fee = amount * 0.034 + 0.30
        return {"success": True, "method": "paypal", "amount": amount + fee, "fee": fee}


class PaymentFactory:
    """Create the processor associated with a payment type."""

    _processors: dict[str, type[PaymentProcessor]] = {
        "credit_card": CreditCardProcessor,
        "bank_transfer": BankTransferProcessor,
        "paypal": PayPalProcessor,
    }

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        processor_class = self._processors.get(payment_type)
        if processor_class is None:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return processor_class()


if __name__ == "__main__":
    factory = PaymentFactory()
    examples = [
        ("credit_card", {"card_number": "1234567890123456", "expiry": "12/25", "cvv": "123"}),
        ("bank_transfer", {"iban": "FR7630006000011234567890189", "bic": "BNPAFRPP"}),
        ("paypal", {"email": "user@example.com"}),
    ]
    for payment_type, details in examples:
        print(factory.get_processor(payment_type).process(100.0, details))
