from assistant_bot.models.fields import Name, Phone, Birthday
from assistant_bot.utils.errors import NotFoundError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)

        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise NotFoundError("Phone not found")

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)

        if phone_obj:
            phone_obj.value = new_phone
        else:
            raise NotFoundError("Phone not found")

    def find_phone(self, phone):
        for p in self.phones:

            if p.value == phone:
                return p

        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = (
            self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday"
        )

        return f"{self.name.value}: {phones}; Birthday: {birthday}"
