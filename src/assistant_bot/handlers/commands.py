from unicodedata import name

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
def add_email(args, book: AddressBook) -> str:
    name, email = args
    record: Record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)

    record.add_email(email)

    return "Email added."

@input_error
def change_email(args, book: AddressBook) -> str:
    if len(args) != 3:
        raise ValueError("Usage: change-email <name> <old_email> <new_email>")
    
    name, old_email, new_email = args
    record: Record = book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.edit_email(old_email, new_email)

    return "Email updated."

@input_error
def remove_email(args, book: AddressBook) -> str:
    name, email = args
    record: Record = book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.remove_email(email)
    return "Email removed."
@input_error
def add_address(args, book: AddressBook) -> str:
    name, *address_parts = args
    record: Record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)

    record.add_address(address_parts)
    return "Address added."

@input_error
def change_address(args, book: AddressBook) -> str:
    name, *address_parts = args
    record: Record = book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    
    if record.address:
        record.edit_address(address_parts)
    else:
        record.add_address(address_parts)

    return "Address updated."
@input_error
def change_contact(args, book: AddressBook) -> str:
    name, new_phone = args
    old_phone = args[2] if len(args) > 2 else None
    record: Record = book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    if record.phones:
        record.edit_phone(new_phone, old_phone)
    else:
        record.add_phone(new_phone)

    return "Contact updated."

@input_error
def show_phone(args, book: AddressBook) -> str:
    if not args:
        raise ValueError("Usage: phone <name>")
    
    name = args[0]
    record = book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    return f"{record.name.value}: {'; '.join(p.value for p in record.phones)}"
@input_error
def remove_phone(args, book: AddressBook) -> str:
    name, phone = args
    record: Record = book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.remove_phone(phone)
    return "Phone removed."


# Для пошуку по полям name, phone та email
@input_error
def find_record(args, book: AddressBook) -> str:
    if not args:
        raise ValueError("Usage: find <query>")
    
    query = args[0]
    results = (
        book.find_by_name(query)
        + book.find_by_phone(query)
        + book.find_by_email(query)
    )

    if not results:
        return "No matching contacts found."

    return "\n".join(str(record) for record in results)

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
    if not args:
        raise ValueError("Usage: show-birthday <name>")

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
    "find": find_record,
    "phone": show_phone,
    "all": show_all,
    "add-email": autosave(add_email),
    "change-email": autosave(change_email),
    "remove-email": autosave(remove_email),
    "add-birthday": autosave(add_birthday),

    "show-birthday": show_birthday,
    "add-address": autosave(add_address),
    "change-address": autosave(change_address),
    "remove-phone": autosave(remove_phone),
    "remove-address": autosave(lambda args, book: book.find(args[0]).remove_address()),
    "birthdays": birthdays,
    "exit": exit_command,
    "close": exit_command,
}
