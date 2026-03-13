from assistant_bot.models.fields import NoteContent


class Note:

    # Model for a single note.
    # Contains an auto-generated sequential id and text content (NoteContent).
    # NoteContent field is defined in the shared fields.py module.


    def __init__(self, note_id: int, content: str = "", tags: list[str] = None):
        # Unique sequential number assigned by NoteBook on creation
        self.id = note_id
        self.content = NoteContent(content)
        self.tags = tags or []

    def short_view(self) -> str:
        return f"{self.id}: {self.content}"

    def edit_content(self, new_content: str):
        self.content = NoteContent(new_content)

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag.lower())

    def remove_tag(self, tag: str):
        self.tags = [t for t in self.tags if t != tag.lower()]

    def __str__(self) -> str:
        separator = "-" * 30
        return (
            f"{separator}\n"
            f"# {self.id}\n"
            f"{separator}\n"
            f"{self.content or '(empty)'}\n"
            f"Tags: {', '.join(self.tags) if self.tags else '(none)'}\n"
        )