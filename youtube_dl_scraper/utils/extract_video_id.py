from typing import Optional
from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> Optional[str]:
    """
    Extracts video id from toutube video url

    Args:
        url (str): Youtube URL to extract video id from.
    Returns:
        Optional[str]: Extracted video id or None if URL is invalid.
    """
    parsed_url = urlparse(url)
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        if "/shorts/" in parsed_url.path:
            return parsed_url.path.split("/shorts/")[1]
        query = parse_qs(parsed_url.query)
        return query.get("v", [None])[0]
    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/")
    return None
