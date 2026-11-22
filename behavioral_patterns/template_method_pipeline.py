"""Template Method Pattern: reusable ETL workflow with source-specific steps."""
from abc import ABC, abstractmethod
from typing import Any


class DataPipeline(ABC):
    """Defines the ETL algorithm once; subclasses customize its individual steps."""

    def __init__(self, source: str):
        self.source = source
        self.data: list[dict[str, Any]] | None = None

    def run(self) -> str:
        """Template method: the order of the pipeline is fixed here."""
        try:
            self.connect()
            self.data = self.extract()
            self.transform()
            self.validate()
            self.load()
            self.after_load()  # Optional hook
            return f"{self.__class__.__name__} finished"
        finally:
            self.cleanup()

    @abstractmethod
    def connect(self) -> None:
        """Connect to the source."""

    @abstractmethod
    def extract(self) -> list[dict[str, Any]]:
        """Extract records from the source."""

    @abstractmethod
    def transform(self) -> None:
        """Transform self.data in place."""

    @abstractmethod
    def load(self) -> None:
        """Load transformed records into the destination."""

    def validate(self) -> None:
        """Shared validation: every record must be a dictionary with required fields."""
        if self.data is None:
            raise ValueError("No data was extracted")
        required = self.required_fields()
        for index, record in enumerate(self.data):
            if not isinstance(record, dict) or any(key not in record for key in required):
                raise ValueError(f"Invalid record structure at index {index}")

    @abstractmethod
    def required_fields(self) -> tuple[str, ...]:
        """Fields required in every record for this source."""

    def after_load(self) -> None:
        """Optional hook for subclasses; no action by default."""

    def cleanup(self) -> None:
        """Shared cleanup step; subclasses may extend it if needed."""
        self.data = None


class CSVPipeline(DataPipeline):
    def connect(self) -> None:
        print(f"Connecting to CSV file: {self.source}")

    def extract(self) -> list[dict[str, Any]]:
        return [
            {"id": 1, "name": "Alice", "age": "30"},
            {"id": 2, "name": "Bob", "age": "25"},
        ]

    def transform(self) -> None:
        assert self.data is not None
        for record in self.data:
            record["age"] = int(record["age"])
            record["name"] = record["name"].upper()

    def required_fields(self) -> tuple[str, ...]:
        return ("id", "name")

    def load(self) -> None:
        print(f"Loaded {len(self.data or [])} CSV records")


class APIPipeline(DataPipeline):
    def connect(self) -> None:
        print(f"Connecting to API: {self.source}")

    def extract(self) -> list[dict[str, Any]]:
        return [
            {"user_id": 101, "username": "charlie", "score": "85"},
            {"user_id": 102, "username": "diana", "score": "92"},
        ]

    def transform(self) -> None:
        assert self.data is not None
        for record in self.data:
            record["score"] = int(record["score"])
            record["username"] = record["username"].lower()
            record["grade"] = "A" if record["score"] >= 90 else "B"

    def required_fields(self) -> tuple[str, ...]:
        return ("user_id", "username")

    def load(self) -> None:
        print(f"Loaded {len(self.data or [])} API records")


class DatabasePipeline(DataPipeline):
    def connect(self) -> None:
        print(f"Connecting to database: {self.source}")

    def extract(self) -> list[dict[str, Any]]:
        return [
            {"product_id": 501, "product_name": "Laptop", "price": "1200"},
            {"product_id": 502, "product_name": "Mouse", "price": "25"},
        ]

    def transform(self) -> None:
        assert self.data is not None
        for record in self.data:
            record["price"] = float(record["price"])
            record["product_name"] = record["product_name"].title()
            record["tax"] = record["price"] * 0.2

    def required_fields(self) -> tuple[str, ...]:
        return ("product_id", "price")

    def load(self) -> None:
        print(f"Loaded {len(self.data or [])} database records")


class XMLPipeline(DataPipeline):
    """Additional XML-specific pipeline demonstrating extensibility."""

    def connect(self) -> None:
        print(f"Connecting to XML file: {self.source}")

    def extract(self) -> list[dict[str, Any]]:
        # Stand-in source data; no external XML file is required for the exercise.
        return [
            {"order_id": "9001", "customer": "alice", "total": "49.90"},
            {"order_id": "9002", "customer": "BOB", "total": "120.00"},
        ]

    def transform(self) -> None:
        assert self.data is not None
        for record in self.data:
            record["order_id"] = int(record["order_id"])
            record["customer"] = record["customer"].title()
            record["total"] = float(record["total"])

    def required_fields(self) -> tuple[str, ...]:
        return ("order_id", "customer", "total")

    def load(self) -> None:
        print(f"Loaded {len(self.data or [])} XML records")


if __name__ == "__main__":
    for pipeline in (
        CSVPipeline("data/users.csv"),
        APIPipeline("https://api.example.com/users"),
        DatabasePipeline("postgresql://localhost/mydb"),
        XMLPipeline("data/orders.xml"),
    ):
        print(f"\nRUNNING {pipeline.__class__.__name__}")
        print("=" * 60)
        print(pipeline.run())
