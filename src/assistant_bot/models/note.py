from assistant_bot.models.fields import NoteContent
from datetime import datetime


class Note:

    # Model for a single note.
    # Contains an auto-generated sequential id and text content (NoteContent).
    # NoteContent field is defined in the shared fields.py module.


    def __init__(self, note_id: int, content: str = "", created_at: datetime = None):
        # Unique sequential number assigned by NoteBook on creation
        self.id = note_id
        self.created_at = created_at or datetime.now()
        self.content = NoteContent(content)

    def __getattr__(self, name: str):
        # Fallback for old pickled notes that don't have created_at
        if name == "created_at":
            return None
        raise AttributeError(name)

    def short_view(self) -> str:
        return f"{self.id}: {self.content}"

    def edit_content(self, new_content: str):
        self.content = NoteContent(new_content)

    def __str__(self) -> str:
        separator = "-" * 30
        return (
            f"{separator}\n"
            f"# {self.id}\n"
            f"{separator}\n"
            f"{self.content or '(empty)'}\n"
        )