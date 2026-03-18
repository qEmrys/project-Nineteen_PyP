from assistant_bot.models.assistant_data import AssistantData
from assistant_bot.storage.file_storage import save_data
from assistant_bot.utils.decorators import input_error


@input_error
def hello_command(args, data: AssistantData) -> str:
    return {
        "status": "success",
        "type": "message",
        "message": "Hello! How can I assist you today?"
    }


@input_error
def help_command(_, __):
    return {
        "status": "success",
        "type": "help"
    }


@input_error
def exit_command(_, data: AssistantData):
    save_data(data)
    return {
        "status": "success",
        "type": "exit",
        "message": "Good bye!"
    }


SYSTEM_COMMANDS = {
    "hello": hello_command,
    "help": help_command,
    "exit": exit_command,
    "close": exit_command,
}
