import re
from unidecode import unidecode


def title_to_slug(title: str) -> str:
    """
    Converts a YouTube video title into a URL-friendly slug.

    Args:
        title (str): The YouTube video title.

    Returns:
        str: A slug suitable for use in URLs.
    """
    # Remove non-ASCII characters and accents
    title = unidecode(title)
    title = title.lower()
    title = re.sub(r"[^a-z0-9]+", "-", title)
    title = title.strip("-")

    return title
