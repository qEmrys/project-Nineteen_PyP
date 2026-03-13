from .contact_commands import CONTACT_COMMANDS
from .note_commands import NOTE_COMMANDS
from .system_commands import SYSTEM_COMMANDS

COMMANDS = {
    **SYSTEM_COMMANDS,
    **CONTACT_COMMANDS,
    **NOTE_COMMANDS,
}
