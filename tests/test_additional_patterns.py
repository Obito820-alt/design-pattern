import json
import unittest

from structural_patterns.adapter_pattern import LegacyReportAdapter, LegacyReportGenerator
from structural_patterns.decorator_pattern import (
    BaseOrder, DiscountDecorator, ExpressShippingDecorator, GiftWrapDecorator,
    InsuranceDecorator, PremiumMemberDecorator,
)
from behavioral_patterns.strategy_report import (
    CSVFormatStrategy, ExcelFormatStrategy, HTMLFormatStrategy, JSONFormatStrategy, PDFFormatStrategy,
    ReportGenerator,
)
from behavioral_patterns.template_method_pipeline import (
    APIPipeline, CSVPipeline, DatabasePipeline, XMLPipeline,
)


class AdapterPatternTests(unittest.TestCase):
    def test_adapter_converts_legacy_xml_to_json(self):
        adapter = LegacyReportAdapter(LegacyReportGenerator())
        report = json.loads(adapter.generate({"orders": 123, "revenue": 45.5}))
        self.assertEqual(report, {"orders": 123, "revenue": 45.5})


class DecoratorPatternTests(unittest.TestCase):
    def test_decorators_can_be_composed(self):
        order = PremiumMemberDecorator(
            DiscountDecorator(
                GiftWrapDecorator(
                    InsuranceDecorator(ExpressShippingDecorator(BaseOrder(100))),
                ),
                15,
            )
        )
        expected = (((100 + 15) * 1.05 + 5) * 0.85) * 0.90
        self.assertAlmostEqual(order.get_cost(), expected)
        self.assertIn("Gift wrap", order.get_description())
        self.assertIn("Premium member", order.get_description())

    def test_invalid_discount(self):
        with self.assertRaises(ValueError):
            DiscountDecorator(BaseOrder(100), 110)


class StrategyPatternTests(unittest.TestCase):
    def setUp(self):
        self.data = [{"name": "Sales Q1", "value": 15000}]
        self.generator = ReportGenerator(self.data)

    def test_switching_strategies(self):
        self.generator.set_strategy(CSVFormatStrategy())
        self.assertEqual(self.generator.generate_report(), "name,value\nSales Q1,15000")
        self.generator.set_strategy(JSONFormatStrategy())
        self.assertEqual(json.loads(self.generator.generate_report()), self.data)

    def test_excel_strategy(self):
        self.generator.set_strategy(ExcelFormatStrategy())
        output = self.generator.generate_report()
        self.assertIn("Name\\tValue", output)
        self.assertIn("Sales Q1\\t15000", output)

    def test_html_extension_without_changing_context(self):
        self.generator.set_strategy(HTMLFormatStrategy())
        self.assertIn("<table>", self.generator.generate_report())
        self.assertIn("Sales Q1", self.generator.generate_report())

    def test_pdf_and_excel_style_output(self):
        self.generator.set_strategy(PDFFormatStrategy())
        self.assertIn("PDF REPORT", self.generator.generate_report())


class TemplateMethodPatternTests(unittest.TestCase):
    def test_all_pipeline_variants_run_and_cleanup(self):
        for pipeline in (
            CSVPipeline("users.csv"), APIPipeline("https://example.com"),
            DatabasePipeline("db"), XMLPipeline("orders.xml"),
        ):
            self.assertTrue(pipeline.run().endswith("finished"))
            self.assertIsNone(pipeline.data)

    def test_validation_rejects_missing_fields(self):
        pipeline = CSVPipeline("users.csv")
        pipeline.data = [{"id": 1}]
        with self.assertRaises(ValueError):
            pipeline.validate()


if __name__ == "__main__":
    unittest.main()
