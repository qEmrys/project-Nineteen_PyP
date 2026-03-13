from assistant_bot.utils.decorators import input_error
from assistant_bot.models.assistant_data import AssistantData
from assistant_bot.models.record import Record
from assistant_bot.utils.errors import NotFoundError, ValidationError
from assistant_bot.utils.decorators import autosave
from assistant_bot.storage.file_storage import save_data
from assistant_bot.utils.colors import success
from assistant_bot.utils.tables import print_warning
from assistant_bot.utils.tables import print_contacts_table, print_phones_table
from assistant_bot.utils.tables import print_birthdays_table, print_notes_table
from assistant_bot.utils.tables import print_note_detail, print_search_results

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
def change_contact(args, data: AssistantData) -> str:
    name, phone = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    if record.phones:
        record.edit_phone(record.phones[0].value, phone)
    else:
        record.add_phone(phone)

    return success("Contact updated.")

@input_error
def show_phone(args, data: AssistantData) -> None:
    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    print_phones_table(record)

@input_error
def show_all(_, data: AssistantData) -> None:
    if not data.book.data:
        print_warning("No contacts found.")
        return

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
        print_warning("No notes found.")
        return

    print_notes_table(list(data.notes.data.values()))

    # Prompt the user to view a note by id
    raw = input("Enter note id (or press Enter to cancel): ").strip()
    if not raw:
        return

    try:
        note_id = int(raw)
    except ValueError:
        print_warning("Note id must be a number.")
        return

    note = data.notes.find_by_id(note_id)

    if note is None:
        raise NotFoundError(f"Note with id {note_id} not found")

    print_note_detail(note)

@input_error
def search_note(args: list, data: AssistantData) -> None:
    if not args:
        raise ValidationError("Usage: search-note <search string>")

    search_str = " ".join(args)
    found_notes = data.notes.find_by_content(search_str)

    if not found_notes:
        print_warning("No notes found matching the search criteria.")
        return

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

    return f"Note {note.id} updated."

@input_error
def delete_note(args: list, data: AssistantData) -> str:
    if len(args) != 1:
        raise ValidationError("Usage: delete-note <id>")

    try:
        note_id = int(args[0])
    except ValueError:
        raise ValidationError("Note id must be a number.")

    data.notes.delete_note(note_id)
    return f"Note {note_id} deleted."

def exit_command(_, data: AssistantData):
    save_data(data)
    print(success("Good bye!"))
    raise SystemExit


CONTACT_COMMANDS = {
    "add": autosave(add_contact),
    "change": autosave(change_contact),
    "phone": show_phone,
    "all": show_all,
    "add-birthday": autosave(add_birthday),
    "show-birthday": show_birthday,
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
