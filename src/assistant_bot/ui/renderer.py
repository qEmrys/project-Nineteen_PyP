from assistant_bot.ui.output import (
    print_main_menu,
    print_success,
    print_error,
    print_warning,
    print_contact_panel,
    print_contacts_table,
    print_phones_table,
    print_birthdays_table,
    print_notes_table,
    print_note_detail,
    print_search_results,
)


def render(result):
    if not result:
        return

    status = result.get("status")
    rtype = result.get("type")

    # --- MESSAGE ---
    if rtype == "message":
        message = result.get("message", "")

        if status == "error":
            print_error(message)
        elif status == "warning":
            print_warning(message)
        else:
            print_success(message)

        return

    # --- CONTACT DETAIL ---
    if rtype == "contact_detail":
        print_contact_panel(result["data"])
        return

    # --- CONTACTS LIST ---
    if rtype == "contacts_list":
        print_contacts_table(result["data"])
        return

    # --- PHONES ---
    if rtype == "phones":
        print_phones_table(result["data"])
        return

    # --- BIRTHDAY (single) ---
    if rtype == "birthday":
        birthday = result["data"]
        print_success(f"Birthday: {birthday}")
        return

    # --- BIRTHDAYS TABLE ---
    if rtype == "birthdays":
        data = result["data"]
        days = result.get("meta", {}).get("days", 7)
        print_birthdays_table(data, days)
        return

    # --- NOTES LIST ---
    if rtype == "notes_list":
        print_notes_table(result["data"])
        return

    # --- NOTE DETAIL ---
    if rtype == "note_detail":
        print_note_detail(result["data"])
        return

    # --- NOTES SEARCH ---
    if rtype == "notes_search":
        data = result["data"]
        query = result.get("meta", {}).get("query", "")
        print_search_results(data, query)
        return

    # --- TAGS ---
    if rtype == "tags":
        tags = result["data"]
        print_success("Tags:")
        for tag in tags:
            print(f"- {tag}")
        return

    # --- GROUPED NOTES ---
    if rtype == "grouped_notes":
        tag_groups = result["data"]

        for tag, notes in sorted(tag_groups.items()):
            print_success(f"Tag: {tag}")
            print_notes_table(notes)

        return
    
    # --- HELP ---
    if rtype == "help":
        print_main_menu()
        return
    
    # --- EXIT ---
    if rtype == "exit":
        print_success(result.get("message", ""))
        return

    # --- FALLBACK ---
    print_error(f"Unknown render type: {rtype}")
