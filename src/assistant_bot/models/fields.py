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
        pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
        if not (isinstance(new_value, str) and re.match(pattern, new_value)):
            raise ValidationError("Invalid email format. Use name@domain.com")
        
        domain_extension = new_value.split("@")[1].rsplit(".", 1)[-1].lower()
        if domain_extension == "ru":
            raise ValidationError("Email with '.ru' domain is not allowed")

        self._value = new_value


class Phone(Field):
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        pattern = r"^\+38\d{10}$"
        if not (isinstance(new_value, str) and re.match(pattern, new_value)):
            raise ValidationError("Phone must start with +380 Example: +380977777777")

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


