from datetime import timedelta
from typing import Union


def format_duration(seconds: int) -> str:
    """
    Format a duration in seconds to a human-readable string with hours, minutes, and seconds.

    Args:
        seconds (int): The total duration in seconds.

    Returns:
        str: A formatted string representing the duration in the format "Xh Ym Zs" or "Xm Zs".
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def parse_duration(duration_str: str) -> str:
    """
    Parse a duration string in the format of "HH:MM:SS" or "MM:SS" and return a human-readable duration.

    Args:
        duration_str (str): A duration string, e.g., "02:15:30" or "15:30".

    Returns:
        str: A human-readable string representing the parsed duration, e.g., "2 hours, 15 minutes, 30 seconds".
    
    Raises:
        ValueError: If the input duration string is not in a valid format.
    """
    parts = list(map(int, duration_str.split(":")))
    if len(parts) == 3:
        hours, minutes, seconds = parts
    elif len(parts) == 2:
        hours = 0
        minutes, seconds = parts
    else:
        raise ValueError("Invalid duration format")

    result = []
    if hours > 0:
        result.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        result.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0:
        result.append(f"{seconds} second{'s' if seconds > 1 else ''}")

    return ", ".join(result)


def format_timedelta(seconds: int) -> str:
    """
    Convert a duration in seconds to a string representation of a timedelta.

    Args:
        seconds (int): The total duration in seconds.

    Returns:
        str: A string representation of the timedelta, e.g., "1:15:30".
    """
    td = timedelta(seconds=seconds)
    return str(td)