"""Adapter Pattern: make a legacy XML report generator usable as a JSON source."""
from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as ET
from typing import Any


class ReportGeneratorInterface(ABC):
    """Interface expected by clients such as the analytics dashboard."""

    @abstractmethod
    def generate(self, data: dict) -> str:
        """Generate and return a JSON report string."""


class LegacyReportGenerator:
    """External legacy component. Its XML interface is intentionally unchanged."""

    def generate_report(self, data: dict) -> str:
        root = ET.Element("report")
        for key, value in data.items():
            element = ET.SubElement(root, str(key))
            element.text = str(value)
        return ET.tostring(root, encoding="unicode")


class LegacyReportAdapter(ReportGeneratorInterface):
    """Wrap a legacy XML generator and expose the JSON interface clients expect."""

    def __init__(self, legacy_generator: LegacyReportGenerator):
        self._legacy_generator = legacy_generator

    @staticmethod
    def _convert_value(value: str) -> Any:
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    def generate(self, data: dict) -> str:
        xml_report = self._legacy_generator.generate_report(data)
        root = ET.fromstring(xml_report)
        report = {
            child.tag: self._convert_value(child.text or "")
            for child in root
        }
        return json.dumps(report)


class AnalyticsDashboard:
    """A simple JSON-only client."""

    def display(self, json_data: str) -> None:
        data = json.loads(json_data)
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    report_generator = LegacyReportAdapter(LegacyReportGenerator())
    dashboard = AnalyticsDashboard()
    sales = {"total_sales": 150000, "orders": 1234, "avg_order": 121.55}
    inventory = {"total_items": 5000, "low_stock": 45, "out_of_stock": 12}
    dashboard.display(report_generator.generate(sales))
    dashboard.display(report_generator.generate(inventory))
