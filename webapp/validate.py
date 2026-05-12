def validate_note(title, body):
    """
    Returns a list of error messages.
    Empty list means everything is valid.
    """
    errors = []

    # Strip whitespace first — so "   " is treated as ""
    title = title.strip()
    body  = body.strip()

    if not title:
        errors.append("Title is required.")

    elif len(title) > 100:
        errors.append("Title must be 100 characters or fewer.")

    if not body:
        errors.append("Body is required.")

    elif len(body) > 10_000:
        errors.append("Body must be 10,000 characters or fewer.")

    return errors