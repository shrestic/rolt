from rolt.accounts.models.employee_model import Employee
from rolt.common.services import model_update
from rolt.users.models import BaseUser


class EmployeeService:
    def __init__(self) -> None:
        pass

    def employee_create(self, *, user: BaseUser) -> Employee:
        employee = Employee(user=user)
        employee.full_clean()
        employee.save()

        return employee

    def employee_update(self, *, employee: Employee, data) -> Employee:
        fields: list[str] = [
            "phone",
            "address",
            "birth_date",
        ]
        employee, has_updated = model_update(
            instance=employee,
            fields=fields,
            data=data,
        )
        return employee
