from assistant_bot.storage.file_storage import load_data, load_notes, save_notes
from assistant_bot.handlers.commands import COMMANDS, NOTE_COMMANDS
from assistant_bot.utils.parser import parse_input


def main():
    book = load_data()
    notebook = load_notes()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        handler = COMMANDS.get(command)
        note_handler = NOTE_COMMANDS.get(command)

        if handler:
            # Saving notes after the assistant bot closing 
            if command in ("exit", "close"):
                save_notes(notebook)
            print(handler(args, book))

        elif note_handler:
            print(note_handler(args, notebook))

        else:
            print("Invalid command.")