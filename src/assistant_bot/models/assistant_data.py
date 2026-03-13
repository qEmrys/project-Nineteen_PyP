from assistant_bot.models.address_book import AddressBook
from assistant_bot.models.note_book import NoteBook


class AssistantData:
    def __init__(self):
        self.book = AddressBook()
        self.notes = NoteBook()
