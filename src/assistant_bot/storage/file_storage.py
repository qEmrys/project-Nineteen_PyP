import pickle
from pathlib import Path
from assistant_bot.models.address_book import AddressBook

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_FILE = BASE_DIR / "data" / "addressbook.pkl"

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
