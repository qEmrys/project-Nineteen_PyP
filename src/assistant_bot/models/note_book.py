from collections import UserDict
from assistant_bot.models.note import Note


class NoteBook(UserDict):

    # Collection of notes
    # Dictionary key is the sequential numeric id of each note.

    def __init__(self):
        super().__init__()
        # Counter for generating unique sequential ids
        self._next_id: int = 1

    def add_note(self, content: str = "") -> Note:

        # Creates a note with the next sequential id and adds it to the collection.

        note = Note(self._next_id, content)
        self.data[note.id] = note
        self._next_id += 1
        return note

    def find(self, note_id: int) -> Note | None:
        #Returns a note by id, or None if not found.
        return self.data.get(note_id)

    def __str__(self) -> str:
        if not self.data:
            return "No notes found."
        return "\n".join(str(note) for note in self.data.values())