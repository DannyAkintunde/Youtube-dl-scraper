import requests
from langcodes import find
from pathlib import Path
from typing import Optional, Union
from youtube_dl_scraper.utils.filename_extractor import get_filename_from_cd


class Caption:
    """Data class for captions."""

    def __init__(
        self,
        caption_data: dict,
        title: str,
        download_path: str,
        translated: bool = False,
    ):
        """
        Initialize the Caption object.

        Args:
            caption_data (dict): The raw caption data, including language code, name, and download URLs.
            title (str): The title of the associated video.
            download_path (str): The directory where captions will be downloaded.
            translated (bool, optional): Whether the caption is translated. Defaults to False.
        """
        self.raw_caption_data = caption_data
        self.title = title
        self.translated = translated
        self.lang = caption_data["code"]
        self.lang_name = caption_data["name"]
        self.download_dir = download_path

    def srt(
        self,
        content: bool = False,
        download_path: Optional[str] = None,
        filename: Optional[str] = None,
        skip_existent: bool = False,
    ) -> Union[str, Path]:
        """
        Download or retrieve the caption in SRT format.

        Args:
            content (bool, optional): If True, return the content as a string; if False, save it to disk. Defaults to False.
            download_path (Optional[str], optional): The directory to save the file. Defaults to self.download_dir.
            filename (Optional[str], optional): The name of the file. Extracted from the content-disposition header if not provided.
            skip_existent (bool, optional): If True, skips downloading if a matching file already exists. Defaults to False.

        Returns:
            Union[str, Path]: File path if content is False, otherwise the SRT content as a string.

        Raises:
            NotImplementedError: If the caption does not support the SRT format.
            FileNotFoundError: If the specified file path is invalid.
            PermissionError: If permissions are insufficient.
            IsADirectoryError: If the specified file path is a directory.
            IOError: For I/O-related errors.
            OSError: For OS-level errors.
        """
        dl_link = self.raw_caption_data.get("urls", dict()).get("srt")
        if not dl_link:
            raise NotImplementedError("caption object don't support the srt format")
        response = requests.get(dl_link)
        response.raise_for_status()
        if not content:
            filename = filename or get_filename_from_cd(
                response.headers.get("content-disposition")
            )
            download_path = download_path or self.download_dir
            filepath = Path(download_path).joinpath(filename)

            if filepath.exists() and skip_existent:
                if filepath.stat().st_size == len(response.content):
                    print("skipping save because file already exists")
                    return filepath.resolve()

            print("Saving file")

            try:
                with filepath.open("wb") as file:
                    file.write(response.content)
                return filepath.resolve()
            except FileNotFoundError as e:
                print("The specified file was not found.")
                raise e
            except PermissionError as e:
                print("You do not have permission to access this file.")
                raise e
            except IsADirectoryError as e:
                print("Expected a file but found a directory.")
                raise e
            except IOError as e:
                print("An IOError occurred.")
                raise e
            except OSError as e:
                print(f"An OS error occurred: {e}")
                raise e
        else:
            return response.content.decode("utf-8")

    def txt(
        self,
        content: bool = False,
        download_path: Optional[str] = None,
        filename: Optional[str] = None,
        skip_existent: bool = False,
    ) -> Union[str, Path]:
        """
        Download or retrieve the caption in TXT format.

        Args:
            content (bool, optional): If True, return the content as a string; if False, save it to disk. Defaults to False.
            download_path (Optional[str], optional): The directory to save the file. Defaults to self.download_dir.
            filename (Optional[str], optional): The name of the file. Extracted from the content-disposition header if not provided.
            skip_existent (bool, optional): If True, skips downloading if a matching file already exists. Defaults to False.

        Returns:
            Union[str, Path]: File path if content is False, otherwise the TXT content as a string.

        Raises:
            NotImplementedError: If the caption does not support the TXT format.
            FileNotFoundError: If the specified file path is invalid.
            PermissionError: If permissions are insufficient.
            IsADirectoryError: If the specified file path is a directory.
            IOError: For I/O-related errors.
            OSError: For OS-level errors.
        """
        dl_link = self.raw_caption_data.get("urls", dict()).get("txt")
        if not dl_link:
            raise NotImplementedError("caption object don't support the txt format")
        response = requests.get(dl_link)
        response.raise_for_status()
        if not content:
            filename = filename or get_filename_from_cd(
                response.headers.get("content-disposition")
            )
            download_path = download_path or self.download_dir
            filepath = Path(download_path).joinpath(filename)

            if filepath.exists() and skip_existent:
                if filepath.stat().st_size == len(response.content):
                    print("skipping save because file already exists")
                    return filepath.resolve()
                else:
                    print("Saving file")

            try:
                with filepath.open("wb") as file:
                    file.write(response.content)
                return filepath.resolve()
            except FileNotFoundError as e:
                print("The specified file was not found.")
                raise e
            except PermissionError as e:
                print("You do not have permission to access this file.")
                raise e
            except IsADirectoryError as e:
                print("Expected a file but found a directory.")
                raise e
            except IOError as e:
                print("An IOError occurred.")
                raise e
            except OSError as e:
                print(f"An OS error occurred: {e}")
                raise e
        else:
            return response.content.decode("utf-8")

    @property
    def raw(self) -> str:
        """
        Retrieve the raw caption content in SRT format.

        Returns:
            str: The raw SRT content as a string.

        Raises:
            NotImplementedError: If the caption does not support the SRT format.
        """
        url = self.raw_caption_data.get("urls", dict()).get("srt")
        if not url:
            raise NotImplementedError("caption object don't support the srt format")
        response = requests.get(url)
        response.raise_for_status()

        return response.text

    def __str__(self) -> str:
        return f"<caption.Caption object lang_code: {self.lang} translated: {self.translated}>"

    def __repr__(self) -> str:
        return self.__str__()
