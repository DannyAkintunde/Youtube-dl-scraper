import re
from typing import Optional


def get_filename_from_cd(cd: str) -> Optional[str]:
    """
    Get filename from content-disposition
    """
    if not cd:
        return
    filename = re.findall("filename=(.+)", cd)
    if len(filename) == 0:
        return None
    return filename[0].replace('"', "").replace("\\", "")
