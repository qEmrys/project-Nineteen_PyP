from assistant_bot.utils.errors import ValidationError, NotFoundError
from assistant_bot.storage.file_storage import save_data


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return str(e)
        except NotFoundError as e:
            return str(e)
        except (ValueError, IndexError):
            return "Invalid command format."
        except Exception as e:
            return f"Unexpected error: {e}"

    return inner

def autosave(func):
    def inner(args, book):
        result = func(args, book)
        save_data(book)
        return result
    return inner
