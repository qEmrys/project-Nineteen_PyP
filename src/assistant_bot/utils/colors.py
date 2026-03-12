from colorama import Fore, Style, init

init(autoreset=True)


def success(text: str) -> str:
    """Bright green — successful operation confirmation."""
    return f"{Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}"


def error(text: str) -> str:
    """Bright red — validation / not-found errors."""
    return f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}"


def info(text: str) -> str:
    """Cyan — informational output (contact data, lists, etc.)."""
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"


def warning(text: str) -> str:
    """Yellow — warnings or empty-result messages."""
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"


def header(text: str) -> str:
    """Bold magenta — section headings."""
    return f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}"


def prompt(text: str) -> str:
    """Bold white — input prompt text."""
    return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"


def dim(text: str) -> str:
    """Dimmed — secondary / separator text."""
    return f"{Style.DIM}{text}{Style.RESET_ALL}"
