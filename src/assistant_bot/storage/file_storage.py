import pickle
from pathlib import Path
from assistant_bot.models.address_book import AddressBook
from assistant_bot.models.note_book import NoteBook

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_FILE = BASE_DIR / "data" / "addressbook.pkl"
NOTES_FILE = BASE_DIR / "data" / "notebook.pkl"

DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def save_data(book, filename=DATA_FILE):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename=DATA_FILE):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def save_notes(notebook: NoteBook, filename: Path = NOTES_FILE) -> None:
    #Серіалізує NoteBook у файл через pickle.
    with open(filename, "wb") as f:
        pickle.dump(notebook, f)

def load_notes(filename: Path = NOTES_FILE) -> NoteBook:
    #Завантажує NoteBook з файлу.
    #Якщо файл ще не існує — повертає порожню книгу нотаток.
    
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NoteBook()