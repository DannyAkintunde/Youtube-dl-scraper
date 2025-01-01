from .caption import Caption
from typing import List, Tuple, Optional


class CaptionArray:
    """A class for managing a collection of captions, including subtitles and translations."""

    def __init__(self, caption_data: dict, download_path: str):
        """
        Initialize the CaptionArray object.

        Args:
            caption_data (dict): The raw caption data, including subtitles and translations.
            download_path (str): The directory where captions will be downloaded.
        """
        self.raw_caption_data = caption_data
        self.title = caption_data.get("title", "")
        self.duration = caption_data.get("duration")
        self.thumbnail = caption_data.get("thumbnail")
        self._subtitles: List[dict] = []
        self._translations: List[dict] = []
        self.__subtitles = caption_data.get("subtitles", list())
        self.__translations = caption_data.get("translations", list())
        self.download_path = download_path

    @property
    def subtitles(self) -> Tuple[dict, ...]:
        """
        Get the list of avaliable subtitles.

        Returns:
            Tuple[dict, ...]: A tuple of avaliable subtitles.
        """
        for subtitle in self.__subtitles:
            subtitle_copy = subtitle.copy()
            subtitle_copy.pop("urls")
            self._subtitles.append(subtitle_copy)

        return tuple(self._subtitles)

    @property
    def translations(self) -> Tuple[dict, ...]:
        """
        Get the list of avaliable translations.

        Returns:
            Tuple[dict, ...]: A tuple of avaliable translations.
        """
        for subtitle in self.__translations:
            subtitle_copy = subtitle.copy()
            subtitle_copy.pop("urls")
            self._translations.append(subtitle_copy)

        return tuple(self._translations)

    def get_captions_by_name(self, name: str) -> List[Caption]:
        """
        Get a list of captions filtered by name.

        Args:
            name (str): The name to filter the captions by.

        Returns:
            List[Caption]: A list of Caption objects matching the specified name.
        """
        filtered_captions = list(
            filter(
                lambda subtitle: name.lower() in subtitle.get("name", "").lower(),
                self.__subtitles,
            )
        )
        out = []
        for caption in filtered_captions:
            out.append(Caption(caption, self.title, self.download_path))

        return out

    def get_captions_by_lang_code(self, lang_code: str) -> Optional[Caption]:
        """
        Get a caption filtered by language code.

        Args:
            lang_code (str): The language code to filter the captions by.

        Returns:
            Optional[Caption]: A Caption object if a matching caption is found, otherwise None.
        """
        filtered_captions = list(
            filter(
                lambda subtitle: lang_code.lower() == subtitle.get("code", "").lower(),
                self.__subtitles,
            )
        )

        if filtered_captions:
            return Caption(filtered_captions[0], self.title, self.download_path)
        return None

    def get_translated_captions_by_name(self, name: str) -> List[Caption]:
        """
        Get a list of translated captions filtered by name.

        Args:
            name (str): The name to filter the translated captions by.

        Returns:
            List[Caption]: A list of translated Caption objects matching the specified name.
        """
        filtered_captions = list(
            filter(
                lambda subtitle: name.lower() in subtitle.get("name", "").lower(),
                self.__translations,
            )
        )
        out = []
        for caption in filtered_captions:
            out.append(Caption(caption, self.title, self.download_path, True))

        return out

    def get_translated_captions_by_lang_code(self, lang_code: str) -> Optional[Caption]:
        """
        Get a translated caption filtered by language code.

        Args:
            lang_code (str): The language code to filter the translated captions by.

        Returns:
            Optional[Caption]: A translated Caption object if a matching caption is found, otherwise None.
        """
        filtered_captions = list(
            filter(
                lambda subtitle: lang_code.lower() == subtitle.get("code", "").lower(),
                self.__translations,
            )
        )

        if filtered_captions:
            return Caption(filtered_captions[0], self.title, self.download_path, True)
        return None
