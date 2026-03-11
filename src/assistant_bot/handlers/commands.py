from assistant_bot.utils.decorators import input_error
from assistant_bot.models.address_book import AddressBook
from assistant_bot.models.record import Record
from assistant_bot.utils.errors import NotFoundError
from assistant_bot.utils.decorators import autosave
from assistant_bot.storage.file_storage import save_data


@input_error
def add_contact(args, book: AddressBook) -> str:
    name, phone = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)

    record.add_phone(phone)

    return "Contact added."

@input_error
def change_contact(args, book: AddressBook) -> str:
    name, phone = args
    record: Record = book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    if record.phones:
        record.edit_phone(record.phones[0].value, phone)
    else:
        record.add_phone(phone)

    return "Contact updated."

@input_error
def show_phone(args, book: AddressBook) -> str:
    name = args[0]
    record: Record = book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    return f"{record.name.value}: {'; '.join(p.value for p in record.phones)}"

@input_error
def show_all(_, book: AddressBook) -> str:
    if not book.data:
        return "No contacts found."

    return "\n".join(
        f"{record.name.value}: {'; '.join(p.value for p in record.phones)}"
        for record in book.data.values()
    )

@input_error
def add_birthday(args, book: AddressBook) -> str:
    name, birthday = args
    record: Record = book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook) -> str:
    name = args[0]
    record: Record = book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    if record.birthday is None:
        raise NotFoundError("Birthday not found")

    return record.birthday

@input_error
def birthdays(_, book: AddressBook) -> str:
    upcoming_birthdays = book.get_upcoming_birthdays()

    if not upcoming_birthdays:
        return "No upcoming birthdays found."

    return "\n".join(
        f"{user['name']} - {user['congratulation_date']}" for user in upcoming_birthdays
    )

def exit_command(_, book: AddressBook):
    save_data(book)
    print("Good bye!")
    raise SystemExit


COMMANDS = {
    "hello": lambda _, __: "How can I help you?",

    "add": autosave(add_contact),
    "change": autosave(change_contact),

    "phone": show_phone,
    "all": show_all,

    "add-birthday": autosave(add_birthday),

    "show-birthday": show_birthday,
    "birthdays": birthdays,
    "exit": exit_command,
    "close": exit_command,
}
