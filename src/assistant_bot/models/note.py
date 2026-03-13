from datetime import datetime

from assistant_bot.models.fields import NoteContent


class Note:
    def __init__(
        self,
        note_id: int,
        content: str = "",
        created_at: datetime = None,
        tags: list[str] = None,
    ):
        self.id = note_id
        self.created_at = created_at or datetime.now()
        self.content = NoteContent(content)
        self.tags = tags or []

    def __getattr__(self, name: str):
        if name == "created_at":
            return None
        raise AttributeError(name)

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
