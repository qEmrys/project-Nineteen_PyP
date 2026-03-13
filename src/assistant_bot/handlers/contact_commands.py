from assistant_bot.models.assistant_data import AssistantData
from assistant_bot.models.record import Record
from assistant_bot.utils.decorators import autosave, input_error
from assistant_bot.utils.design import (
    print_birthdays_table,
    print_contact_panel,
    print_contacts_table,
    print_phones_table,
    print_success,
    print_warning,
)
from assistant_bot.utils.errors import NotFoundError, ValidationError

"""Contact management commands: add, show, find, all, remove, change-name, show-phone"""


@input_error
def show_contact(args, data: AssistantData) -> None:
    if not args:
        raise ValidationError("Usage: show <name>")

    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    print_contact_panel(record)


@input_error
def add_contact(args, data: AssistantData) -> str:
    if len(args) != 2:
        raise ValidationError("Usage: add <name> <phone>")
    name, phone = args
    record = data.book.find(name)

    if record is None:
        record = Record(name)

    record.add_phone(phone)

    if data.book.find(name) is None:
        data.book.add_record(record)

    print_success("Contact added.")
    return


@input_error
def remove_contact(args, data: AssistantData) -> str:
    if not args:
        raise ValidationError("Usage: remove <name>")

    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    data.book.delete(name)
    print_success("Contact removed.")
    return


@input_error
def change_name(args, data: AssistantData) -> str:
    if len(args) != 2:
        raise ValidationError("Usage: change-name <old_name> <new_name>")

    old_name, new_name = args
    record: Record = data.book.find(old_name)

    if record is None:
        raise NotFoundError("Contact not found")

    data.book.delete(old_name)
    record.name.value = new_name
    data.book.add_record(record)

    print_success("Name updated.")
    return


"""Email management commands: add-email, change-email, remove-email"""


@input_error
def add_email(args, data: AssistantData) -> str:
    if len(args) != 2:
        raise ValidationError("Usage: add-email <name> <email>")

    name, email = args
    record: Record = data.book.find(name)

    if record is None:
        record = Record(name)
        data.book.add_record(record)
    record.add_email(email)

    print_success("Email added.")
    return


@input_error
def change_email(args, data: AssistantData) -> str:
    if len(args) != 3:
        raise ValidationError("Usage: change-email <name> <old_email> <new_email>")

    name, old_email, new_email = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.edit_email(old_email, new_email)

    print_success("Email updated.")
    return


@input_error
def remove_email(args, data: AssistantData) -> str:
    if len(args) != 2:
        raise ValidationError("Usage: remove-email <name> <email>")

    name, email = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.remove_email(email)
    print_success("Email removed.")
    return


"""Address management commands: add-address, change-address, remove-address"""


@input_error
def add_address(args, data: AssistantData) -> str:
    if len(args) < 2:
        raise ValidationError("Usage: add-address <name> <address>")

    name, *address_parts = args
    record: Record = data.book.find(name)

    if record is None:
        record = Record(name)
        data.book.add_record(record)
    record.add_address(address_parts)
    print_success("Address added.")
    return


@input_error
def change_address(args, data: AssistantData) -> str:
    if len(args) < 2:
        raise ValidationError("Usage: change-address <name> <address>")

    name, *address_parts = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    if record.address:
        record.edit_address(address_parts)
    else:
        record.add_address(address_parts)

    print_success("Address updated.")
    return


@input_error
def remove_address(args, data: AssistantData) -> str:
    if len(args) != 1:
        raise ValidationError("Usage: remove-address <name>")

    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.remove_address()
    print_success("Address removed.")
    return


"""Phone management commands: show-phone, change-phone, remove-phone"""


@input_error
def change_phone(args, data: AssistantData) -> str:
    if len(args) != 3:
        raise ValidationError("Usage: change-phone <name> <old_phone> <new_phone>")

    name, old_phone, new_phone = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")
    if record.phones:
        record.edit_phone(old_phone, new_phone)
    else:
        record.add_phone(new_phone)

    print_success("Contact updated.")
    return


@input_error
def show_phone(args, data: AssistantData) -> str:
    if not args:
        raise ValidationError("Usage: phone <name>")
    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    print_phones_table(record)


@input_error
def remove_phone(args, data: AssistantData) -> str:
    if len(args) != 2:
        raise ValidationError("Usage: remove-phone <name> <phone>")

    name, phone = args
    record: Record = data.book.find(name)
    if record is None:
        raise NotFoundError("Contact not found")

    record.remove_phone(phone)
    print_success("Phone removed.")
    return


"""Search commands: find, all"""


@input_error
def find_record(args, data: AssistantData) -> None:
    if not args:
        raise ValidationError("Usage: find <query>")

    query = args[0]
    results = (
        data.book.find_by_name(query)
        + data.book.find_by_phone(query)
        + data.book.find_by_email(query)
    )

    if not results:
        print_warning("No matching contacts found.")
        return

    print_contacts_table(results)


@input_error
def show_all(_, data: AssistantData) -> None:
    if not data.book.data:
        print_warning("No contacts found.")
        return

    print_contacts_table(list(data.book.data.values()))


"""Name management command: change-name"""


@input_error
def add_birthday(args, data: AssistantData) -> str:
    if len(args) != 2:
        raise ValidationError("Usage: add-birthday <name> <birthday>")

    name, birthday = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.add_birthday(birthday)
    print_success("Birthday added.")
    return


@input_error
def show_birthday(args, data: AssistantData) -> str:
    if len(args) != 1:
        raise ValidationError("Usage: show-birthday <name>")

    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    if record.birthday is None:
        raise NotFoundError("Birthday not found")

    return record.birthday


@input_error
def change_birthday(args, data: AssistantData) -> str:
    if len(args) != 2:
        raise ValidationError("Usage: change-birthday <name> <birthday>")
    name, new_birthday = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    if record.birthday:
        record.edit_birthday(new_birthday)
    else:
        record.add_birthday(new_birthday)

    print_success("Birthday updated.")
    return


@input_error
def remove_birthday(args, data: AssistantData) -> str:
    if len(args) != 1:
        raise ValidationError("Usage: remove-birthday <name>")
    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.remove_birthday()
    print_success("Birthday removed.")
    return


@input_error
def birthdays(args, data: AssistantData) -> str:
    days = 7
    if args:
        if not args[0].isdigit():
            raise ValidationError("Number of days must be a positive integer")
        days = int(args[0])

    upcoming_birthdays = data.book.get_upcoming_birthdays(days)

    if not upcoming_birthdays:
        print_warning(f"No birthdays in the next {days} day(s).")
        return

    print_birthdays_table(upcoming_birthdays, days)


CONTACT_COMMANDS = {
    "add": autosave(add_contact),
    "show": show_contact,
    "find": find_record,
    "all": show_all,
    "remove": autosave(remove_contact),
    "change-name": autosave(change_name),
    "show-phone": show_phone,
    "change-phone": autosave(change_phone),
    "remove-phone": autosave(remove_phone),
    "add-email": autosave(add_email),
    "change-email": autosave(change_email),
    "remove-email": autosave(remove_email),
    "add-birthday": autosave(add_birthday),
    "show-birthday": show_birthday,
    "change-birthday": autosave(change_birthday),
    "remove-birthday": autosave(remove_birthday),
    "add-address": autosave(add_address),
    "change-address": autosave(change_address),
    "remove-address": autosave(remove_address),
    "birthdays": birthdays,
}
