from assistant_bot.storage.file_storage import save_data
from assistant_bot.utils.design import console
from assistant_bot.utils.errors import NotFoundError, ValidationError


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            console.print(f"[bold red]{e}[/bold red]")
        except NotFoundError as e:
            console.print(f"[bold red]{e}[/bold red]")
        except (ValueError, IndexError):
            console.print("[bold red]Invalid command format.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Unexpected error: {e}[/bold red]")

    return inner


def autosave(func):
    def inner(args, assistant):
        result = func(args, assistant)
        save_data(assistant)
        return result

    return inner
