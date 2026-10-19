"""Helpers for working with text and emails."""


def normalize_whitespace(text):
    """Trim the text and collapse runs of whitespace into one space."""
    return " ".join(text.split())


def slugify(text):
    """Convert text into a lowercase slug separated by hyphens."""
    cleaned = normalize_whitespace(text).lower()
    kept = [ch if ch.isalnum() else " " for ch in cleaned]
    return "-".join("".join(kept).split())


def is_valid_email(email):
    """True when email has exactly one '@' and a '.' in the domain part."""
    return email.count("@") == 1 and "." in email.split("@")[1]

def mask_email(email):
    """Hide the email username except for its first character."""
    if not is_valid_email(email):
        return email

    local, domain = email.split("@")
    return f"{local[0]}***@{domain}"