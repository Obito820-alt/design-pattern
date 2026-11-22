"""Strategy Pattern: generate reports using interchangeable format strategies."""
from abc import ABC, abstractmethod
import csv
import html
import io
import json
from pathlib import Path
from typing import Iterable


class ReportFormatStrategy(ABC):
    """Contract implemented by every report output format."""

    file_extension = "txt"

    @abstractmethod
    def generate(self, data: list[dict]) -> str:
        """Return the report as text."""


class PDFFormatStrategy(ReportFormatStrategy):
    file_extension = "pdf"

    def generate(self, data: list[dict]) -> str:
        lines = ["PDF REPORT", "=" * 50]
        lines.extend(f"| {item['name']:20} | {item['value']:10} |" for item in data)
        lines.extend(["=" * 50, "End of PDF Report"])
        # A readable text representation for this exercise (not a binary PDF).
        return "\n".join(lines)


class ExcelFormatStrategy(ReportFormatStrategy):
    file_extension = "xlsx"

    def generate(self, data: list[dict]) -> str:
        lines = ["EXCEL REPORT", "-" * 50, "Name\tValue"]
        lines.extend(f"{item['name']}\t{item['value']}" for item in data)
        lines.append("-" * 50)
        # Tab-separated text representation, matching the exercise's example.
        return "\n".join(lines)


class CSVFormatStrategy(ReportFormatStrategy):
    file_extension = "csv"

    def generate(self, data: list[dict]) -> str:
        output = io.StringIO(newline="")
        writer = csv.DictWriter(output, fieldnames=["name", "value"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue().rstrip("\r\n")


class JSONFormatStrategy(ReportFormatStrategy):
    file_extension = "json"

    def generate(self, data: list[dict]) -> str:
        return json.dumps(data, indent=2)


class HTMLFormatStrategy(ReportFormatStrategy):
    """New format added without changing ReportGenerator or existing strategies."""

    file_extension = "html"

    def generate(self, data: list[dict]) -> str:
        rows = "\n".join(
            f"<tr><td>{html.escape(str(item['name']))}</td>"
            f"<td>{html.escape(str(item['value']))}</td></tr>"
            for item in data
        )
        return (
            "<!doctype html>\n<html><head><meta charset=\"utf-8\">"
            "<title>Report</title></head><body><table>"
            "<thead><tr><th>Name</th><th>Value</th></tr></thead>"
            f"<tbody>{rows}</tbody></table></body></html>"
        )


class ReportGenerator:
    """Context class that delegates formatting to the current strategy."""

    def __init__(self, data: Iterable[dict], strategy: ReportFormatStrategy | None = None):
        self.data = list(data)
        self._strategy = strategy

    def set_strategy(self, strategy: ReportFormatStrategy) -> None:
        if not isinstance(strategy, ReportFormatStrategy):
            raise TypeError("strategy must implement ReportFormatStrategy")
        self._strategy = strategy

    def generate_report(self) -> str:
        if self._strategy is None:
            raise RuntimeError("Set a report format strategy before generating a report")
        return self._strategy.generate(self.data)

    def save_report(self, filename: str) -> Path:
        if self._strategy is None:
            raise RuntimeError("Set a report format strategy before saving a report")
        path = Path(f"{filename}.{self._strategy.file_extension}")
        path.write_text(self.generate_report(), encoding="utf-8")
        return path


if __name__ == "__main__":
    data = [
        {"name": "Sales Q1", "value": 15000},
        {"name": "Sales Q2", "value": 18000},
        {"name": "Sales Q3", "value": 22000},
        {"name": "Sales Q4", "value": 25000},
    ]
    generator = ReportGenerator(data)
    for strategy in (PDFFormatStrategy(), CSVFormatStrategy(),
                     JSONFormatStrategy(), HTMLFormatStrategy()):
        generator.set_strategy(strategy)
        print(f"=== {strategy.__class__.__name__} ===")
        print(generator.generate_report())
        print()
