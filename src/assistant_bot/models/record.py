from assistant_bot.models.fields import Address, Name, Phone, Birthday, Email
from assistant_bot.utils.errors import NotFoundError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.address = None 
        self.birthday = None
        self.phones = []
        self.emails = []
        
        
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    def add_email(self, email):
        self.emails.append(Email(email))
    def add_address(self, address):
        self.address = Address(address)
    def remove_email(self, email):
        email_obj = self.find_email(email)

        if email_obj:
            self.emails.remove(email_obj)
        else:
            raise NotFoundError("Email not found")
    def find_email(self, email):
        for e in self.emails:

            if e.value == email:
                return e

        return None
    def edit_email(self, old_email, new_email):
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
    def edit_address(self, new_address):
        if self.address:
            self.address.value = new_address
        else:
            raise NotFoundError("Address not found")
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
        address = " ".join(self.address.value) if self.address else "No address"
        emails = "; ".join(e.value for e in self.emails) if self.emails else "No emails"
        return f"{self.name.value}: {phones}; Birthday: {birthday}; Address: {address}; Emails: {emails}"