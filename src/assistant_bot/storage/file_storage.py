import pickle
from pathlib import Path
from assistant_bot.models.assistant_data import AssistantData

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "assistant.pkl"

DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def save_data(data: AssistantData, filename: Path = DATA_FILE) -> None:
    # Серіалізує AssistantData у файл через pickle.
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_data(filename=DATA_FILE):
    # Завантажує AssistantData з файлу.
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AssistantData()
