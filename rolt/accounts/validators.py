from django.core.exceptions import ValidationError
from django.utils import timezone


class UserValidator:
    PHONE_LENGTH = 10

    def __init__(self) -> None:
        pass

    def validate_file_size(self, file):
        max_size_kb = 500
        if file and file.size > max_size_kb * 1024:
            msg = f"Files cannot be larger than {max_size_kb}KB!"
            raise ValidationError(msg)

    def validate_phone(self, phone):
        if phone and len(phone) != self.PHONE_LENGTH:
            msg = "Phone number must be 10 digits"
            raise ValidationError(msg)

    def validate_birth_date(self, birth_date):
        if birth_date and birth_date > timezone.now().date():
            msg = "Birth date cannot be in the future"
            raise ValidationError(msg)
