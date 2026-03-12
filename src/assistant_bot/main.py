from assistant_bot.storage.file_storage import load_data
from assistant_bot.handlers.commands import COMMANDS
from assistant_bot.utils.parser import parse_input

#Main menu
def print_main_menu():
    print("""
🤖 Available commands:
+----------------------------------+----------------------------------+
| Command                          | Description                      |
+----------------------------------+----------------------------------+
| add <name> <+380*********>       | Add new contact                  |
| change <name> <+380*********>    | Change contact phone             |
| phone <name>                     | Show phone number                |
| all                              | Show all contacts                |
| add-birthday <name> <DD.MM.YYYY> | Add birthday to contact          |
| show-birthday <name>             | Show contact birthday            |
| birthdays [days]                 | Show upcoming birthdays          |
| add-note <content>               | Add a note                       |
| show-notes                       | Show all notes                   |
| search-note <text>               | Search notes by text             |
| edit-note <id> <content>         | Edit note                        |
| delete-note <id>                 | Delete note                      |
| exit / close                     | Exit assistant                   |
+----------------------------------+----------------------------------+
""")

def main():
    assistant = load_data()

    print("Welcome to the assistant bot!")
    print_main_menu()

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        handler = COMMANDS.get(command)

        if handler:
            print(handler(args, assistant))
        else:
            print("Invalid command.")