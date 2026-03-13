from assistant_bot.utils.decorators import input_error
from assistant_bot.models.assistant_data import AssistantData
from assistant_bot.models.record import Record
from assistant_bot.utils.errors import NotFoundError, ValidationError
from assistant_bot.utils.decorators import autosave
from assistant_bot.storage.file_storage import save_data
from assistant_bot.utils.colors import success, error, warning
from assistant_bot.utils.tables import print_warning
from assistant_bot.utils.tables import print_contacts_table, print_phones_table
from assistant_bot.utils.tables import print_birthdays_table, print_notes_table
from assistant_bot.utils.tables import print_note_detail, print_search_results


@input_error
def show_contact(args, data: AssistantData) -> str:
    if not args:
        raise ValidationError("Usage: show <name>")

    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    return str(record)

@input_error
def add_contact(args, data: AssistantData) -> str:
    name, phone = args
    record = data.book.find(name)

    if record is None:
        record = Record(name)
        data.book.add_record(record)
    record.add_phone(phone)

    return success("Contact added.")

@input_error
def remove_contact(args, data: AssistantData) -> str:
    if not args:
        raise ValidationError("Usage: remove <name>")

    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    data.book.delete(name)
    return success("Contact removed.")

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

    return success("Name updated.")

@input_error
def add_email(args, data: AssistantData) -> str:
    name, email = args
    record: Record = data.book.find(name)

    if record is None:
        record = Record(name)
        data.book.add_record(record)
    record.add_email(email)

    return success("Email added.")

@input_error
def change_email(args, data: AssistantData) -> str:
    if len(args) != 3:
        raise ValidationError("Usage: change-email <name> <old_email> <new_email>")
    
    name, old_email, new_email = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.edit_email(old_email, new_email)

    return success("Email updated.")

@input_error
def remove_email(args, data: AssistantData) -> str:
    name, email = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.remove_email(email)
    return success("Email removed.")

@input_error
def add_address(args, data: AssistantData) -> str:
    name, *address_parts = args
    record: Record = data.book.find(name)

    if record is None:
        record = Record(name)
        data.book.add_record(record)
    record.add_address(address_parts)
    return success("Address added.")

@input_error
def change_address(args, data: AssistantData) -> str:
    name, *address_parts = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    if record.address:
        record.edit_address(address_parts)
    else:
        record.add_address(address_parts)

    return success("Address updated.")

@input_error
def remove_address(args, data: AssistantData) -> str:
    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.remove_address()
    return success("Address removed.")

@input_error
def change_phone(args, data: AssistantData) -> str:
    name, new_phone = args
    old_phone = args[2] if len(args) > 2 else None
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")
    if record.phones:
        record.edit_phone(new_phone, old_phone)
    else:
        record.add_phone(new_phone)

    return success("Contact updated.")

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
    name, phone = args
    record: Record = data.book.find(name)
    if record is None:
        raise NotFoundError("Contact not found")

    record.remove_phone(phone)
    return success("Phone removed.")


# Для пошуку по полям name, phone та email
@input_error
def find_record(args, data: AssistantData) -> str:
    if not args:
        raise ValidationError("Usage: find <query>")
    
    query = args[0]
    results = (
        data.book.find_by_name(query)
        + data.book.find_by_phone(query)
        + data.book.find_by_email(query)
    )

    if not results:
        return error("No matching contacts found.")

    return "\n".join(str(record) for record in results)

@input_error
def show_all(_, data: AssistantData) -> str:
    if not data.book.data:
        return warning("No contacts found.")

    print_contacts_table(list(data.book.data.values()))

@input_error
def add_birthday(args, data: AssistantData) -> str:
    name, birthday = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.add_birthday(birthday)
    return success("Birthday added.")

@input_error
def show_birthday(args, data: AssistantData) -> str:
    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    if record.birthday is None:
        raise NotFoundError("Birthday not found")

    return record.birthday

@input_error
def change_birthday(args, data: AssistantData) -> str:
    name, new_birthday = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    if record.birthday:
        record.edit_birthday(new_birthday)
    else:
        record.add_birthday(new_birthday)

    return success("Birthday updated.")

@input_error
def remove_birthday(args, data: AssistantData) -> str:
    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.remove_birthday()
    return success("Birthday removed.")

@input_error
def birthdays(args, data: AssistantData) -> str:
    days = 7
    if args:
        if not args[0].isdigit():
            raise ValidationError("Number of days must be a positive integer")
        days = int(args[0])

    upcoming_birthdays = data.book.get_upcoming_birthdays(days)

    if not upcoming_birthdays:
        return warning(f"No birthdays in the next {days} day(s).")

    print_birthdays_table(upcoming_birthdays, days)

@input_error
def add_note(args: list, data: AssistantData) -> str:

    # Command: add-note <content...>
    # All words after the command become the note content.
    # ID is assigned automatically as a sequential number.
    if not args:
        raise ValidationError("Usage: add-note <content>")

    content = " ".join(args)

    note = data.notes.add_note(content)
    return success(f"Note added with id: {note.id}.")

@input_error
def show_notes(args: list, data: AssistantData) -> str:

    # Command: show-notes
    # Prints a numbered list of all notes with a short preview,
    # then prompts the user to enter the id of the note to display.

    if not data.notes.data:
        return warning("No notes found.")

    print_notes_table(list(data.notes.data.values()))

    raw = input("Enter note id: ").strip()

    try:
        note_id = int(raw)
    except ValueError:
        return warning("Note id must be a number.")

    note = data.notes.find_by_id(note_id)

    if note is None:
        raise NotFoundError(f"Note with id {note_id} not found")

    print_note_detail(note)

@input_error
def search_note(args: list, data: AssistantData) -> str:
    if not args:
        raise ValidationError("Usage: search-note <search string>")

    search_str = " ".join(args)
    found_notes = data.notes.find_by_content(search_str)

    if not found_notes:
        return warning("No notes found matching the search criteria.")

    print_search_results(found_notes, search_str)

@input_error
def edit_note(args: list, data: AssistantData) -> str:
    if len(args) < 2:
        raise ValidationError("Usage: edit-note <id> <new content>")

    try:
        note_id = int(args[0])
    except ValueError:
        raise ValidationError("Note id must be a number.")

    new_content = " ".join(args[1:])
    note = data.notes.edit_note(note_id, new_content)

    return success(f"Note {note.id} updated.")

@input_error
def delete_note(args: list, data: AssistantData) -> str:
    if len(args) != 1:
        raise ValidationError("Usage: delete-note <id>")

    try:
        note_id = int(args[0])
    except ValueError:
        raise ValidationError("Note id must be a number.")

    data.notes.delete_note(note_id)
    return success(f"Note {note_id} deleted.")

def exit_command(_, data: AssistantData):
    save_data(data)
    print(success("Good bye!"))
    raise SystemExit


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

NOTE_COMMANDS = {
    "add-note": autosave(add_note),
    "show-notes": show_notes,
    "search-note": search_note,
    "edit-note": autosave(edit_note),
    "delete-note": autosave(delete_note),
}

SYSTEM_COMMANDS = {
    "hello": lambda _, __: "How can I help you?",
    "exit": exit_command,
    "close": exit_command,
}

COMMANDS = {
    **SYSTEM_COMMANDS,
    **CONTACT_COMMANDS,
    **NOTE_COMMANDS,
}
