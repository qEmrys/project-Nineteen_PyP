from assistant_bot.storage.file_storage import save_data
from assistant_bot.utils.errors import NotFoundError, ValidationError


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return {"status": "error", "type": "message", "message": str(e)}
        except NotFoundError as e:
            return {"status": "error", "type": "message", "message": str(e)}
        except (ValueError, IndexError):
            return {"status": "error", "type": "message", "message": "Invalid command format."}
        except Exception as e:
            return {"status": "error", "type": "message", "message": f"Unexpected error: {e}"}
    return inner


def autosave(func):
    def inner(args, assistant):
        result = func(args, assistant)
        save_data(assistant)
        return result

    return inner
