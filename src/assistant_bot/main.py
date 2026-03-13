from assistant_bot.storage.file_storage import load_data
from assistant_bot.handlers.commands import COMMANDS
from assistant_bot.utils.parser import parse_input
from assistant_bot.utils.colors import header, info, error, prompt, success


def main():
    assistant = load_data()

    print(header("Welcome to the assistant bot!"))

    while True:
        user_input = input(prompt("Enter a command: "))
        command, args = parse_input(user_input)
        handler = COMMANDS.get(command)

        if handler:
            result = handler(args, assistant)
            if result is not None:
                print(info(str(result)))
        else:
            print(error("Invalid command."))