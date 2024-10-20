import re
import requests
from langcodes import find
from pathlib import Path


def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    filename = re.findall('filename=(.+)', cd)
    if len(filename) == 0:
        return None
    return filename[0].replace('"', '').replace('\\', '')


class Caption:

    def __init__(self, caption_data: dict, api: str, title: str, download_path: str):
        self.raw_caption_data = caption_data
        self._dl_api = api
        self.title = title
        self.lang = str(find(caption_data['name']))
        self.download_dir = download_path

    def srt(self, content=False, download_path: str | None = None, filename: str | None = None):
        params = {
            'title': f'{self.title}-{self.lang}',
            'url': self.raw_caption_data['url'],
        }
        response = requests.get(self._dl_api, params=params)
        response.raise_for_status()
        if not content:
            filename = filename or get_filename_from_cd(response.headers.get('content-disposition'))
            download_path = download_path or self.download_dir
            filepath = Path(download_path).joinpath(filename)

            try:
                with filepath.open('wb') as file:
                    file.write(response.content)
                return filepath.resolve()
            except Exception as e:
                print('error saving file')
                raise e
        else:
            return response.content.decode('utf-8')

    def txt(self, content=False, download_path: str | None = None, filename: str | None = None):
        params = {
            'title': f'{self.title}-{self.lang}',
            'url': self.raw_caption_data['url'],
            'type': 'txt'
        }
        response = requests.get(self._dl_api, params=params)
        response.raise_for_status()
        if not content:
            filename = filename or get_filename_from_cd(response.headers.get('content-disposition'))
            download_path = download_path or self.download_dir
            filepath = Path(download_path).joinpath(filename)

            try:
                with filepath.open('wb') as file:
                    file.write(response.content)
                return filepath.resolve()
            except Exception as e:
                print('error saving file')
                raise e
        else:
            return response.content.decode('utf-8')

    @property
    def raw(self):
        params = {
            'title': f'{self.title}-{self.lang}',
            'url': self.raw_caption_data['url'],
            'type': 'raw'
        }
        response = requests.get(self._dl_api, params=params)
        response.raise_for_status()

        return response.text


class Captions:

    def __init__(self, title: str, caption_data: dict, download_path: str):
        self.title = title
        self.raw_caption_data = caption_data
        self._subtitles = []
        self._translations = []
        self.__subtitles = caption_data['json']['subtitles']
        self.__translations = caption_data['json']['subtitlesAutoTrans']
        self.subtitle_dl_api = caption_data['json']['urlSubtitle']
        self.download_path = download_path

    @property
    def subtitles(self):
        for subtitle in self.__subtitles:
            subtitle_copy = subtitle.copy()
            subtitle_copy.pop('url')
            self._subtitles.append(subtitle)

        return self._subtitles

    @property
    def translations(self):
        for subtitle in self.__translations:
            subtitle_copy = subtitle.copy()
            subtitle_copy.pop('url')
            subtitle_copy['code'] = str(find(subtitle['name']))
            self._translations.append(subtitle)

        return self._translations

    def get_captions_by_name(self, name: str) -> Caption:
        filtered_captions = list(filter((lambda subtitle: subtitle['name'] == name),
                                        self.__subtitles))
        if len(filtered_captions) > 0:
            return Caption(filtered_captions[0], self.subtitle_dl_api, self.title, self.download_path)

    def get_captions_by_lang_code(self, lang_code: str) -> Caption:
        filtered_captions = list(filter((lambda subtitle: subtitle['code'] == lang_code),
                                        self.__subtitles))
        if len(filtered_captions) > 0:
            return Caption(filtered_captions[0], self.subtitle_dl_api, self.title, self.download_path)

    def get_translated_captions_by_name(self, name: str) -> Caption:
        filtered_captions = list(filter((lambda subtitle: subtitle['name'].lower() == name.lower()),
                                        self.__translations))
        if len(filtered_captions) > 0:
            return Caption(filtered_captions[0], self.subtitle_dl_api, self.title, self.download_path)

    def get_translated_captions_by_lang_code(self, lang_code: str) -> Caption:
        filtered_captions = list(filter((lambda subtitle: str(find(subtitle['name'])) == lang_code),
                                        self.__translations))
        if len(filtered_captions) > 0:
            return Caption(filtered_captions[0], self.subtitle_dl_api, self.title, self.download_path)
