from assistant_bot.handlers.commands_registry import COMMANDS
from assistant_bot.storage.file_storage import load_data
from assistant_bot.utils.design import console, print_main_menu
from assistant_bot.utils.parser import parse_input


def main():
    assistant = load_data()

    console.print("[bold magenta]Welcome to the assistant bot![/bold magenta]")
    print_main_menu()
    console.print("[dim]Type 'hello' for a greeting or 'exit' to quit.[/dim]")

    while True:
        user_input = console.input("[bold white]Enter a command:[/bold white] ")
        command, args = parse_input(user_input)
        handler = COMMANDS.get(command)

        if handler:
            result = handler(args, assistant)
            if result is not None:
                console.print(str(result))
        else:
            console.print(
                f"[bold red]Unknown command:[/bold red] [yellow]{command}[/yellow]  "
                "[dim](type [bold]help[/bold] to see all commands)[/dim]"
            )
