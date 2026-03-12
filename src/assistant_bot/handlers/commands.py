from assistant_bot.utils.decorators import input_error
from assistant_bot.models.assistant_data import AssistantData
from assistant_bot.models.record import Record
from assistant_bot.utils.errors import NotFoundError, ValidationError
from assistant_bot.utils.decorators import autosave
from assistant_bot.storage.file_storage import save_data

@input_error
def add_contact(args, data: AssistantData) -> str:
    name, phone = args
    record = data.book.find(name)

    if record is None:
        record = Record(name)
        data.book.add_record(record)
    record.add_phone(phone)

    return "Contact added."

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

    return "Contact updated."

@input_error
def show_phone(args, data: AssistantData) -> str:
    name = args[0]
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    return f"{record.name.value}: {'; '.join(p.value for p in record.phones)}"

@input_error
def show_all(_, data: AssistantData) -> str:
    if not data.book.data:
        return "No contacts found."

    return "\n".join(
        f"{record.name.value}: {'; '.join(p.value for p in record.phones)}"
        for record in data.book.data.values()
    )

@input_error
def add_birthday(args, data: AssistantData) -> str:
    name, birthday = args
    record: Record = data.book.find(name)

    if record is None:
        raise NotFoundError("Contact not found")

    record.add_birthday(birthday)
    return "Birthday added."

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
        return f"No birthdays in the next {days} day(s)."

    header = f"Birthdays in the next {days} day(s):"
    lines = [
        f"  {user['name']} ({user['birthday']}) — congrats on {user['congratulation_date']}"
        for user in upcoming_birthdays
    ]
    return header + "\n" + "\n".join(lines)

@input_error
def add_note(args: list, data: AssistantData) -> str:

    # Command: add-note <content...>
    # All words after the command become the note content.
    # ID is assigned automatically as a sequential number.
    if not args:
        raise ValueError

    content = " ".join(args)

    note = data.notes.add_note(content)
    return f"Note added with id: {note.id}."

def _note_preview(note) -> str:
    #Returns a one-line preview: first 10 characters of content followed by '...'
    text = note.content.value
    return f"{text[:10]}..." if len(text) > 10 else text

@input_error
def show_notes(args: list, data: AssistantData) -> str:

    # Command: show-notes
    # Prints a numbered list of all notes with a short preview,
    # then prompts the user to enter the id of the note to display.

    if not data.notes.data:
        return "No notes found."

    # Print the list header and each note as: id - first 3 words...
    print("\nList of Notes:")
    print("-" * 30)
    for note in data.notes.data.values():
        print(f"  {note.id} - {_note_preview(note)}")
    print("-" * 30)

    # Prompt the user to put a note by id
    raw = input("Enter note id: ").strip()

    try:
        note_id = int(raw)
    except ValueError:
        return "Note id must be a number."

    note = data.notes.find(note_id)

    if note is None:
        raise NotFoundError(f"Note with id {note_id} not found")

    return str(note)

def exit_command(_, data: AssistantData):
    save_data(data)
    print("Good bye!")
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
