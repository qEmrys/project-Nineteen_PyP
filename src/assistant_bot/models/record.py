from assistant_bot.models.fields import Address, Birthday, Email, Name, Phone
from assistant_bot.utils.errors import NotFoundError


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.address = None
        self.birthday = None
        self.phones = []
        self.emails = []

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def add_email(self, email: str):
        self.emails.append(Email(email))

    def add_address(self, address: list[str]):
        self.address = Address(address)

    def remove_email(self, email: str):
        email_obj = self.find_email(email)

        if email_obj:
            self.emails.remove(email_obj)
        else:
            raise NotFoundError("Email not found")

    def find_email(self, email: str):
        for e in self.emails:

            if e.value == email:
                return e

        return None

    def edit_email(self, old_email: str, new_email: str):
        email_obj = self.find_email(old_email)

        if email_obj:
            email_obj.value = new_email
        else:
            raise NotFoundError("Email not found")

    def remove_address(self):
        if self.address:
            self.address = None
        else:
            raise NotFoundError("Address not found")

    def edit_address(self, new_address: list[str]):
        if self.address:
            self.address.value = new_address
        else:
            raise NotFoundError("Address not found")

    def remove_phone(self, phone: str):
        phone_obj = self.find_phone(phone)

        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise NotFoundError("Phone not found")

    def edit_phone(self, old_phone: str, new_phone: str):
        phone_obj = self.find_phone(old_phone)

        if phone_obj:
            phone_obj.value = new_phone
        else:
            raise NotFoundError("Phone not found")

    def find_phone(self, phone: str):
        for p in self.phones:

            if p.value == phone:
                return p

        return None

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def edit_birthday(self, new_birthday: str):
        if self.birthday:
            self.birthday.value = new_birthday
        else:
            raise NotFoundError("Birthday not found")

    def remove_birthday(self):
        if self.birthday:
            self.birthday = None
        else:
            raise NotFoundError("Birthday not found")

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = (
            self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday"
        )
        address = " ".join(self.address.value) if self.address else "No address"
        emails = "; ".join(e.value for e in self.emails) if self.emails else "No emails"
        return f"{self.name.value}: {phones}; Birthday: {birthday}; Address: {address}; Emails: {emails}"
