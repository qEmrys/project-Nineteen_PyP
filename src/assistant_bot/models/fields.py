from datetime import datetime
from assistant_bot.utils.errors import ValidationError
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValidationError("Name cannot be empty")

        super().__init__(value)


class Address(Field):
    def __init__(self, value):
        if not value:
            raise ValidationError("Address cannot be empty")

        super().__init__(value)


class Email(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not (isinstance(new_value, str) and re.match(pattern, new_value)):
            raise ValidationError("Invalid email format. Use name@domain.com")

        self._value = new_value


class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not (
            isinstance(new_value, str) and new_value.isdigit() and len(new_value) == 10
        ):
            raise ValidationError("Phone must contain exactly 10 digits")

        self._value = new_value


class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            self._value = datetime.strptime(new_value, "%d.%m.%Y")
        except ValueError:
            raise ValidationError("Invalid date format. Use DD.MM.YYYY")
        
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class NoteContent(Field):

    def __init__(self, value: str = ""):
        if not value or not value.strip():
            raise ValidationError("Note content cannot be empty")
        super().__init__(value.strip())
