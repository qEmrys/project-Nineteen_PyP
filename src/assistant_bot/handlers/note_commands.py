from assistant_bot.models.assistant_data import AssistantData
from assistant_bot.utils.decorators import autosave, input_error
from assistant_bot.utils.errors import NotFoundError, ValidationError

"""Note-related command handlers."""


@input_error
def add_note(args: list, data: AssistantData) -> str:
    if not args:
        raise ValidationError("Usage: add-note <content>")

    text_parts = []
    tags = []

    for arg in args:
        if arg.startswith("#") and len(arg) > 1:
            tags.append(arg[1:])
        else:
            text_parts.append(arg)

    content = " ".join(text_parts)
    note = data.notes.add_note(content)

    for tag in tags:
        note.add_tag(tag)

    return {
        "status": "success",
        "type": "message",
        "message": f"Note added with id: {note.id}."
    }


@input_error
def show_notes(args: list, data: AssistantData) -> str:
    if not data.notes.data:
        return {
            "status": "warning",
            "type": "message",
            "message": "No notes found."
        }

    return {
        "status": "success",
        "type": "notes_list",
        "data": list(data.notes.data.values())
    }


@input_error
def search_note(args: list, data: AssistantData) -> str:
    if not args:
        raise ValidationError("Usage: search-note <search string>")

    search_str = " ".join(args)
    found_notes = data.notes.find_by_content(search_str)

    if not found_notes:
        return {
            "status": "warning",
            "type": "message",
            "message": "No notes found matching the search criteria."
        }

    return {
        "status": "success",
        "type": "notes_search",
        "data": found_notes,
        "meta": {"query": search_str}
    }


@input_error
def search_note_by_id(args: list, data: AssistantData) -> str:
    if not args:
        raise ValidationError("Usage: show-note <id>")

    try:
        note_id = int(args[0])
    except ValueError:
        raise ValidationError("Note id must be a number.")

    note = data.notes.find_by_id(note_id)

    if not note:
        return {
            "status": "warning",
            "type": "message",
            "message": "No note found with the given id."
        }

    return {
        "status": "success",
        "type": "note_detail",
        "data": note
    }


@input_error
def edit_note(args: list, data: AssistantData) -> str:
    if len(args) < 2:
        raise ValidationError("Usage: edit-note <id> <new content>")

    try:
        note_id = int(args[0])
    except ValueError:
        raise ValidationError("Note id must be a number.")

    new_content = " ".join(args[1:])
    note = data.notes.edit_note(note_id, new_content)

    return {
        "status": "success",
        "type": "message",
        "message": f"Note {note.id} updated."
    }


@input_error
def delete_note(args: list, data: AssistantData) -> str:
    if len(args) != 1:
        raise ValidationError("Usage: delete-note <id>")

    try:
        note_id = int(args[0])
    except ValueError:
        raise ValidationError("Note id must be a number.")

    data.notes.delete_note(note_id)
    
    return {
        "status": "success",
        "type": "message",
        "message": f"Note {note_id} deleted."
    }


@input_error
def show_tags(args: list, data: AssistantData) -> str:
    if args:
        raise ValidationError("Usage: show-tags")

    tags = data.notes.get_all_tags()

    if not tags:
        return {
            "status": "warning",
            "type": "message",
            "message": "No tags found."
        }

    return {
        "status": "success",
        "type": "tags",
        "data": tags
    }


@input_error
def add_tag(args: list, data: AssistantData) -> str:
    if len(args) != 2:
        raise ValidationError("Usage: add-tag <note_id> <tag>")

    try:
        note_id = int(args[0])
    except ValueError:
        raise ValidationError("Note id must be a number.")

    tag = args[1]
    note = data.notes.find_by_id(note_id)

    if not note:
        raise NotFoundError("Note not found.")

    note.add_tag(tag)

    return {
        "status": "success",
        "type": "message",
        "message": f"Tag '{tag}' added to note {note_id}."
    }


@input_error
def remove_tag(args: list, data: AssistantData) -> str:
    if len(args) != 2:
        raise ValidationError("Usage: remove-tag <note_id> <tag>")

    try:
        note_id = int(args[0])
    except ValueError:
        raise ValidationError("Note id must be a number.")

    tag = args[1]
    note = data.notes.find_by_id(note_id)
    if not note:
        raise NotFoundError("Note not found.")
    if tag not in note.tags:
        raise NotFoundError("Tag not found in the note.")
    note.remove_tag(tag)
    
    return {
        "status": "success",
        "type": "message",
        "message": f"Tag '{tag}' removed from note {note_id}."
    }


@input_error
def search_note_by_tag(args: list, data: AssistantData) -> str:
    if len(args) != 1:
        raise ValidationError("Usage: search-tag <tag>")

    tag = args[0]
    found_notes = data.notes.search_by_tag(tag)

    if not found_notes:
        return {
            "status": "warning",
            "type": "message",
            "message": "No notes found with the given tag."
        }

    return {
        "status": "success",
        "type": "notes_list",
        "data": found_notes
    }


@input_error
def group_by_tags(args: list, data: AssistantData) -> None:
    if args:
        raise ValidationError("Usage: group-tags")

    tag_groups = data.notes.group_by_tags()

    if not tag_groups:
        return {
            "status": "warning",
            "type": "message",
            "message": "No notes found."
        }

    return {
        "status": "success",
        "type": "grouped_notes",
        "data": tag_groups
    }


NOTE_COMMANDS = {
    "add-note": autosave(add_note),
    "all-notes": show_notes,
    "show-note": search_note_by_id,
    "search-note": search_note,
    "edit-note": autosave(edit_note),
    "delete-note": autosave(delete_note),
    "show-tags": show_tags,
    "add-tag": autosave(add_tag),
    "remove-tag": autosave(remove_tag),
    "search-tag": search_note_by_tag,
    "group-tags": group_by_tags,
}
