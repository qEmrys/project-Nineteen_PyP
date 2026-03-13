from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()


def print_warning(text: str) -> None:
    """Print a warning message using yellow markup."""
    console.print(f"[bold yellow]{text}[/bold yellow]")


def print_error(text: str) -> None:
    """Print an error message using red markup."""
    console.print(f"[bold red]{text}[/bold red]")


def print_success(text: str) -> None:
    """Print a success message using green markup."""
    console.print(f"[bold green]{text}[/bold green]")


def print_contact_panel(record) -> None:
    """Render a single contact's full details in a rich panel."""
    phones = "\n".join(p.value for p in record.phones) if record.phones else "—"
    birthday = (
        record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "—"
    )
    emails = "\n".join(e.value for e in record.emails) if getattr(record, "emails", None) else "—"
    address = " ".join(record.address.value) if getattr(record, "address", None) else "—"

    content = (
        f"[cyan]Phones:[/cyan]   {phones}\n"
        f"[cyan]Birthday:[/cyan] {birthday}\n"
        f"[cyan]Email:[/cyan]    {emails}\n"
        f"[cyan]Address:[/cyan]  {address}"
    )
    panel = Panel(
        content,
        title=f"[bold magenta]{record.name.value}[/bold magenta]",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)


def print_contacts_table(records: list) -> None:
    """Render all contacts as a table."""
    table = Table(
        title="Address Book",
        box=box.ROUNDED,
        show_lines=True,
        title_style="bold magenta",
        header_style="bold cyan",
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Name", style="bold white", min_width=14)
    table.add_column("Phones", min_width=18)
    table.add_column("Birthday", justify="center", min_width=12)
    table.add_column("Email", min_width=18)
    table.add_column("Address", min_width=16)

    for idx, record in enumerate(records, start=1):
        phones = "\n".join(p.value for p in record.phones) if record.phones else "—"
        birthday = (
            record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "—"
        )
        email = "; ".join(e.value for e in record.emails) if getattr(record, "emails", None) else "—"
        address = " ".join(record.address.value) if getattr(record, "address", None) else "—"

        table.add_row(str(idx), record.name.value, phones, birthday, email, address)

    console.print(table)


def print_phones_table(record) -> None:
    """Render a single contact's phones as a table."""
    table = Table(
        title=f"Phones — [bold white]{record.name.value}[/]",
        box=box.SIMPLE_HEAD,
        header_style="bold cyan",
        title_style="bold magenta",
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Phone number", style="green")

    if record.phones:
        for idx, phone in enumerate(record.phones, start=1):
            table.add_row(str(idx), phone.value)
    else:
        table.add_row("—", "[dim]No phones[/]")

    console.print(table)


def print_birthdays_table(upcoming: list, days: int) -> None:
    """Render upcoming birthdays as a table."""
    table = Table(
        title=f"Birthdays in the next {days} day(s)",
        box=box.ROUNDED,
        show_lines=True,
        title_style="bold magenta",
        header_style="bold cyan",
    )
    table.add_column("Name", style="bold white", min_width=14)
    table.add_column("Birthday", justify="center", style="green", min_width=8)
    table.add_column("Congratulate on", justify="center", style="yellow", min_width=14)

    for user in upcoming:
        table.add_row(user["name"], user["birthday"], user["congratulation_date"])

    console.print(table)


def print_notes_table(notes: list) -> None:
    """Render a list of notes (preview) as a table."""
    table = Table(
        title="Notes",
        box=box.ROUNDED,
        show_lines=True,
        title_style="bold magenta",
        header_style="bold cyan",
    )
    table.add_column("ID", style="dim", width=6, justify="right")
    table.add_column("Created", style="cyan", justify="center", min_width=16)
    table.add_column("Preview", style="white")

    for note in notes:
        text = note.content.value
        preview = (text[:60] + "…") if len(text) > 60 else text
        created_at = getattr(note, "created_at", None)
        created = created_at.strftime("%d.%m.%Y %H:%M") if created_at else "—"
        table.add_row(str(note.id), created, preview)

    console.print(table)


def print_note_detail(note) -> None:
    """Render full note content in a panel."""
    panel = Panel(
        Text(note.content.value),
        title=f"[bold cyan]Note #{note.id}[/]",
        border_style="magenta",
        padding=(1, 2),
    )
    console.print(panel)


def print_search_results(notes: list, query: str) -> None:
    """Render note search results as a table."""
    table = Table(
        title=f'Search results for "{query}"',
        box=box.ROUNDED,
        show_lines=True,
        title_style="bold magenta",
        header_style="bold cyan",
    )
    table.add_column("ID", style="dim", width=6, justify="right")
    table.add_column("Content", style="white")

    for note in notes:
        table.add_row(str(note.id), note.content.value)

    console.print(table)

MENU_COMMANDS = [
    ("add <name> <+380XXXXXXXXX>",             "Add new contact"),
    ("show <name>",                            "Show contact details"),
    ("find <query>",                           "Search by name / phone / email"),
    ("all",                                    "Show all contacts"),
    ("remove <name>",                          "Delete contact"),
    ("change-name <old> <new>",                "Rename contact"),
    ("show-phone <name>",                      "Show phone numbers"),
    ("change-phone <name> <old> <new>",        "Change phone number"),
    ("remove-phone <name> <+380XXXXXXXXX>",    "Remove phone number"),
    ("add-email <name> <user@example.com>",    "Add email address"),
    ("change-email <name> <old> <new>",        "Change email address"),
    ("remove-email <name> <email>",            "Remove email address"),
    ("add-address <name> <address>",           "Add address"),
    ("change-address <name> <address>",        "Change address"),
    ("remove-address <name>",                  "Remove address"),
    ("add-birthday <name> <DD.MM.YYYY>",       "Add birthday"),
    ("show-birthday <name>",                   "Show birthday"),
    ("change-birthday <name> <DD.MM.YYYY>",    "Change birthday"),
    ("remove-birthday <name>",                 "Remove birthday"),
    ("birthdays [days]",                       "Upcoming birthdays (default 7)"),

    ("add-note <content>",                     "Add a note (supports #tags)"),
    ("show-notes",                             "Show all notes"),
    ("search-note <text>",                     "Search notes by content"),
    ("search-note-by-id <id>",                 "Find note by ID"),
    ("edit-note <id> <content>",               "Edit note"),
    ("delete-note <id>",                       "Delete note"),

    ("show-tags",                              "Show all available tags"),
    ("add-tag <id> <tag>",                     "Add tag to note"),
    ("remove-tag <id> <tag>",                  "Remove tag from note"),
    ("search-tag <tag>",                       "Search notes by tag"),
    ("group-tags",                             "Group notes by tags"),

    ("help",                                   "Show list with available commands"),
    ("exit / close",                           "Save and exit"),
]
 
def print_main_menu() -> None:
    #Render all commands as a rich table.
    table = Table(
        title="🤖 Available commands:",
        box=box.ROUNDED,
        show_lines=True,
        title_style="bold magenta",
        header_style="bold cyan",
    )
    table.add_column("Command", style="bold yellow", no_wrap=True, min_width=42)
    table.add_column("Description", style="white", min_width=32)
 
    for cmd, desc in MENU_COMMANDS:
        table.add_row(cmd, desc)
 
    console.print(table)