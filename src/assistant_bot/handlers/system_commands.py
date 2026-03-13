from assistant_bot.models.assistant_data import AssistantData
from assistant_bot.storage.file_storage import save_data
from assistant_bot.utils.decorators import input_error
from assistant_bot.utils.design import print_main_menu, print_success


@input_error
def hello_command(args, data: AssistantData) -> str:
    return "Hello! How can I assist you today?"


@input_error
def exit_command(_, data: AssistantData):
    save_data(data)
    print_success("Good bye!")
    raise SystemExit


SYSTEM_COMMANDS = {
    "hello": hello_command,
    "help": lambda _args, _data: print_main_menu() or None,
    "exit": exit_command,
    "close": exit_command,
}
