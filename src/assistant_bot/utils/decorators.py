from assistant_bot.utils.errors import ValidationError, NotFoundError
from assistant_bot.storage.file_storage import save_data
from assistant_bot.utils.colors import error as color_error


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return color_error(str(e))
        except NotFoundError as e:
            return color_error(str(e))
        except (ValueError, IndexError):
            return color_error("Invalid command format.")
        except Exception as e:
            return color_error(f"Unexpected error: {e}")

    return inner

def autosave(func):
    def inner(args, assistant):
        result = func(args, assistant)
        save_data(assistant)
        return result
    return inner
