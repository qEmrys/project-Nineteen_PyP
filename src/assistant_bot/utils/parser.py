def parse_input(user_input: str):
    parts = user_input.split()
    if not parts:
        return "", []
    cmd, *args = parts

    return cmd.strip().lower(), args
