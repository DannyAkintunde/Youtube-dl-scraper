from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> str:
    """
    Extracts video ID from YouTube video URL.

    Args:
        url (str): YouTube URL to extract video ID from.
    Returns:
        str: Extracted video ID or an empty string if no video ID is present.
    Raises:
        ValueError: If the URL is unsupported.
    """
    parsed_url = urlparse(url)
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        if "/shorts/" in parsed_url.path:
            return parsed_url.path.split("/shorts/")[1]
        elif "/embed/" in parsed_url.path:
            return parsed_url.path.split("/embed/")[1]
        query = parse_qs(parsed_url.query)
        return query.get("v", [""])[0]  # Return empty string if "v" is missing or empty
    elif parsed_url.hostname == "youtu.be":
        return (
            parsed_url.path.lstrip("/") or ""
        )  # Return empty string if no ID is present
    else:
        raise ValueError(f"Unsupported URL: {url}")
