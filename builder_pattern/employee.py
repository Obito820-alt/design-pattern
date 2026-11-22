"""Builder Pattern example: readable Employee construction."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: str
    manager_id: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: Optional[str] = None
    contract_type: str = "permanent"


class EmployeeBuilder:
    """Build an Employee through small, chainable configuration methods."""

    def __init__(self) -> None:
        self._data = {
            "first_name": None, "last_name": None, "email": None,
            "department": None, "position": None, "salary": None, "start_date": None,
        }
        self._optional_data = {
            "manager_id": None, "phone": None, "address": None,
            "emergency_contact": None, "has_parking": False, "has_laptop": False,
            "has_vpn_access": False, "has_admin_rights": False,
            "office_location": None, "contract_type": "permanent",
        }

    def with_name(self, first_name: str, last_name: str):
        self._data.update(first_name=first_name, last_name=last_name)
        return self

    def with_email(self, email: str):
        self._data["email"] = email
        return self

    def with_job(self, department: str, position: str, salary: float, start_date: str = ""):
        self._data.update(department=department, position=position, salary=salary)
        if start_date:
            self._data["start_date"] = start_date
        return self

    def with_start_date(self, start_date: str):
        self._data["start_date"] = start_date
        return self

    def with_equipment(self, laptop: bool = False, parking: bool = False):
        self._optional_data.update(has_laptop=laptop, has_parking=parking)
        return self

    def with_access(self, vpn: bool = False, admin: bool = False):
        self._optional_data.update(has_vpn_access=vpn, has_admin_rights=admin)
        return self

    def with_manager(self, manager_id: Optional[int]):
        self._optional_data["manager_id"] = manager_id
        return self

    def with_contact(self, phone: Optional[str] = None, address: Optional[str] = None,
                     emergency_contact: Optional[str] = None):
        self._optional_data.update(phone=phone, address=address, emergency_contact=emergency_contact)
        return self

    def with_office(self, office_location: Optional[str]):
        self._optional_data["office_location"] = office_location
        return self

    def with_contract(self, contract_type: str = "permanent"):
        self._optional_data["contract_type"] = contract_type
        return self

    def build(self) -> Employee:
        required = ("first_name", "last_name", "email", "department", "position", "salary", "start_date")
        missing = [key for key in required if self._data.get(key) in (None, "")]
        if missing:
            raise ValueError("Missing required employee fields: " + ", ".join(missing))
        if "@" not in self._data["email"]:
            raise ValueError("Valid email is required")
        if self._data["salary"] < 0:
            raise ValueError("Salary cannot be negative")
        return Employee(**self._data, **self._optional_data)


class DeveloperBuilder(EmployeeBuilder):
    """Convenience builder with sensible defaults for a developer."""

    def __init__(self, first_name: str, last_name: str, email: str):
        super().__init__()
        self.with_name(first_name, last_name).with_email(email)
        self.with_job("Engineering", "Developer", 0.0, "")
        self.with_equipment(laptop=True).with_access(vpn=True, admin=False)
        self.with_contract("permanent")


if __name__ == "__main__":
    employee = (EmployeeBuilder().with_name("John", "Doe")
                .with_email("john.doe@company.com")
                .with_job("Engineering", "Senior Developer", 75000, "2024-01-15")
                .with_equipment(laptop=True).with_access(vpn=True, admin=True)
                .with_office("Paris HQ").build())
    print(employee)
    developer = DeveloperBuilder("Jane", "Smith", "jane.smith@company.com").with_job(
        "Engineering", "Junior Developer", 35000, "2024-02-01"
    ).build()
    print(developer)
