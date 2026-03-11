from assistant_bot.storage.file_storage import load_data
from assistant_bot.handlers.commands import COMMANDS
from assistant_bot.utils.parser import parse_input


def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        handler = COMMANDS.get(command)

        if handler:
            print(handler(args, book))
        else:
            print("Invalid command.")
