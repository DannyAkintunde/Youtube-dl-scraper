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

    def __init__(self, caption_data: dict, api: str, title: str, download_path: str, translated: bool = False):
        self.raw_caption_data = caption_data
        self._dl_api = api
        self.title = title
        self.translated = translated
        self.lang = ('a.' if 'auto-generated' in caption_data.get('name') else '') + str(find(caption_data['name']))
        self.lang_name = caption_data['name']
        self.download_dir = download_path

    def srt(self, content=False, download_path: str | None = None, filename: str | None = None, skip_existent: bool = False):
        params = {
            'title': f'{self.title}-({self.lang})',
            'url': self.raw_caption_data['url'],
        }
        response = requests.get(self._dl_api, params=params)
        response.raise_for_status()
        if not content:
            filename = filename or get_filename_from_cd(response.headers.get('content-disposition'))
            download_path = download_path or self.download_dir
            filepath = Path(download_path).joinpath(filename)

            if filepath.exists() and skip_existent:
                if filepath.stat().st_size == len(response.content):
                    print('skipping save because file already exists')
                    return

            print("Saving file")

            try:
                with filepath.open('wb') as file:
                    file.write(response.content)
                return filepath.resolve()
            except Exception as e:
                print('error saving file')
                raise e
        else:
            return response.content.decode('utf-8')

    def txt(self, content=False, download_path: str | None = None, filename: str | None = None, skip_existent: bool = False):
        params = {
            'title': f'{self.title}-({self.lang})',
            'url': self.raw_caption_data['url'],
            'type': 'txt'
        }
        response = requests.get(self._dl_api, params=params)
        response.raise_for_status()
        if not content:
            filename = filename or get_filename_from_cd(response.headers.get('content-disposition'))
            download_path = download_path or self.download_dir
            filepath = Path(download_path).joinpath(filename)

            if filepath.exists() and skip_existent:
                if filepath.stat().st_size == len(response.content):
                    print('skipping save because file already exists')
                    return
                else:
                    print("Saving file")

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
            'title': f'{self.title}-({self.lang})',
            'url': self.raw_caption_data['url'],
            'type': 'raw'
        }
        response = requests.get(self._dl_api, params=params)
        response.raise_for_status()

        return response.text

    def __str__(self):
        return f'<Caption.Caption object lang_code: {self.lang} translated: {self.translated}>'


class Captions:

    def __init__(self, title: str, caption_data: dict, download_path: str):
        self.title = title
        self.raw_caption_data = caption_data
        self._subtitles = []
        self._translations = []
        self.__subtitles = caption_data['json'].get('subtitles', list())
        self.__translations = caption_data['json'].get('subtitlesAutoTrans', list())
        self.subtitle_dl_api = caption_data['json'].get('urlSubtitle')
        self.download_path = download_path

    @property
    def subtitles(self):
        for subtitle in self.__subtitles:
            subtitle_copy = subtitle.copy()
            subtitle_copy.pop('url')
            if 'auto' in subtitle_copy.get('name'):
                subtitle_copy['code'] = 'a.' + str(find(subtitle_copy['name']))
            self._subtitles.append(subtitle_copy)

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
        filtered_captions = list(filter((lambda subtitle: name.lower() in subtitle.get('name', '').lower()),
                                        self.__subtitles))
        out = []
        for caption in filtered_captions:
            out.append(Caption(caption, self.subtitle_dl_api, self.title, self.download_path))
        
        return out

    def get_captions_by_lang_code(self, lang_code: str) -> Caption:
        filtered_captions = list(filter((lambda subtitle: lang_code.lower() == subtitle.get('code', '').lower()),
                                        self.__subtitles))
        
        if len(filtered_captions) > 0:
            return Caption(filtered_captions[0], self.subtitle_dl_api, self.title, self.download_path)
  
    def get_translated_captions_by_name(self, name: str) -> Caption:
        filtered_captions = list(filter((lambda subtitle: name.lower() in subtitle.get('name', '').lower()),
                                        self.__translations))
        out = []
        for caption in filtered_captions:
            out.append(Caption(caption, self.subtitle_dl_api, self.title, self.download_path, True))
        
        return out
  
    def get_translated_captions_by_lang_code(self, lang_code: str) -> Caption:
        try:
            filtered_captions = list(filter((lambda subtitle: str(find(subtitle.get('name', ''))).lower() == lang_code.lower()),
                                            self.__translations))
        except: # LookupError
            return
        
        if len(filtered_captions) > 0:
            return Caption(filtered_captions[0], self.subtitle_dl_api, self.title, self.download_path, True)
        