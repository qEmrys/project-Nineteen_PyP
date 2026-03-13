from collections import UserDict
from assistant_bot.models.note import Note
from assistant_bot.utils.errors import NotFoundError


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

    def find_by_id(self, note_id: int) -> Note | None:
        #Returns a note by id, or None if not found.
        return self.data.get(note_id)
    
    def find_by_content(self, search_str: str) -> list[Note]:
        search_str = search_str.lower()
        return [note for note in self.data.values() if search_str in note.content.value.lower()]
    
    def edit_note(self, note_id: int, new_content: str) -> Note:
        note = self.find_by_id(note_id)
        if note is None:
            raise NotFoundError(f"Note with id {note_id} not found")
        note.edit_content(new_content)
        return note
    
    def delete_note(self, note_id: int):
        if note_id in self.data:
            del self.data[note_id]
        else:
            raise NotFoundError(f"Note with id {note_id} not found")

    def __str__(self) -> str:
        if not self.data:
            return "No notes found."
        return "\n".join(str(note) for note in self.data.values())