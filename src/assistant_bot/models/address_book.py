from collections import UserDict
from datetime import date, timedelta


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def find_by_name(self, name):
        return [
            record
            for record in self.data.values()
            if name.lower() in record.name.value.lower()
        ]

    def find_by_phone(self, phone):
        return [
            record
            for record in self.data.values()
            if any(phone in p.value for p in record.phones)
        ]

    def find_by_email(self, email):
        return [
            record
            for record in self.data.values()
            if email in [e.value for e in record.emails]
        ]

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self, days: int = 7):
        """Returns a list of records with upcoming birthdays within the specified number of days."""
        today = date.today()
        result = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value.date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            delta = (birthday_this_year - today).days

            if 0 <= delta <= days:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() >= 5:
                    congratulation_date += timedelta(
                        days=7 - congratulation_date.weekday()
                    )

                result.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                        "birthday": birthday.strftime("%d.%m"),
                    }
                )

        return result
