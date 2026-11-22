import unittest

from factory_pattern.payment import PaymentFactory
from builder_pattern.employee import EmployeeBuilder, DeveloperBuilder
from singleton_pattern.config_manager import ConfigManager


class FactoryPatternTests(unittest.TestCase):
    def setUp(self):
        self.factory = PaymentFactory()

    def test_credit_card_payment(self):
        result = self.factory.get_processor("credit_card").process(
            100.0, {"card_number": "1234567890123456", "cvv": "123"}
        )
        self.assertTrue(result["success"])
        self.assertAlmostEqual(result["fee"], 2.9)
        self.assertAlmostEqual(result["amount"], 102.9)

    def test_bank_transfer_payment(self):
        result = self.factory.get_processor("bank_transfer").process(
            100.0, {"iban": "FR7630006000011234567890189"}
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["fee"], 1.5)

    def test_paypal_payment(self):
        result = self.factory.get_processor("paypal").process(100.0, {"email": "a@example.com"})
        self.assertTrue(result["success"])
        self.assertAlmostEqual(result["fee"], 3.7)

    def test_invalid_details_and_unknown_method(self):
        result = self.factory.get_processor("credit_card").process(
            10, {"card_number": "bad", "cvv": "1"}
        )
        self.assertFalse(result["success"])
        with self.assertRaises(ValueError):
            self.factory.get_processor("crypto")


class BuilderPatternTests(unittest.TestCase):
    def test_build_employee(self):
        employee = (EmployeeBuilder().with_name("John", "Doe")
                    .with_email("john@example.com")
                    .with_job("Engineering", "Developer", 75000, "2024-01-15")
                    .with_equipment(laptop=True).with_access(vpn=True).build())
        self.assertEqual(employee.first_name, "John")
        self.assertTrue(employee.has_laptop)
        self.assertTrue(employee.has_vpn_access)

    def test_validation(self):
        with self.assertRaises(ValueError):
            EmployeeBuilder().build()

    def test_developer_builder(self):
        employee = DeveloperBuilder("Jane", "Smith", "jane@example.com").with_job(
            "Engineering", "Developer", 40000, "2024-02-01"
        ).build()
        self.assertTrue(employee.has_laptop)


class SingletonPatternTests(unittest.TestCase):
    def test_same_instance_and_nested_get(self):
        first = ConfigManager.get_instance()
        second = ConfigManager.get_instance()
        self.assertIs(first, second)
        self.assertEqual(first.get("database.host"), "localhost")
        self.assertIsNone(first.get("missing.value"))


if __name__ == "__main__":
    unittest.main()
