import re
from bs4 import BeautifulSoup
from langcodes import find
from Stream import Stream
from StreamArray import StreamArray
from Caption import Captions


class Video:
    _quality_regex = r'\((\d+p)(\d+)?(\s[A-z]{2,3})?\)'

    def __init__(self, view_url: str, raw_html, caption_data, download_path: str):
        self.captions = None
        self.duration = None
        self.streams = None
        self.shares = None
        self.views = None
        self.comments = None
        self.owner = None
        self.title = None
        self.thumbnail = None
        self._raw_html = raw_html
        self.caption_data = caption_data
        self.download_path = download_path
        self.view_url = view_url
        self.soup = BeautifulSoup(raw_html, 'html.parser')
        # print(self.soup)
        self.parse_data()
        self.parse_streams_data()

    def parse_data(self):
        thumbnail_img = self.soup.find('div', attrs={'class': 'icon-box-img'}).find('img')
        self.thumbnail = {
            'width': int(thumbnail_img['width']),
            'height': int(thumbnail_img['height']),
            'url': thumbnail_img['src'],
            'yt-thumb': self.caption_data['json']['thumbnail']
        }
        self.duration = self.caption_data['json']['duration']
        video_info = self.soup.find('div', attrs={'class': 'icon-box-text'}).find('div', attrs={'class': 'text'})
        video_info_paragraphs = video_info.find_all('p')
        self.title = video_info_paragraphs[0].get_text()[6:].strip()
        self.owner = video_info_paragraphs[1].get_text()[6:].strip()
        self.captions = Captions(self.title, self.caption_data, self.download_path)

    def parse_streams_data(self):
        streams_data = self.soup.find_all("div", attrs={'class': 'col-inner'})[-1]
        streams_data_a = streams_data.find_all("a")[:-1]
        # print(streams_data_a[-1])
        # print(streams_data)

        self.streams = StreamArray()

        for stream in streams_data_a:
            url = stream['href']
            text = stream.get_text()
            if 'mp3' in text.lower():
                st_ins = Stream(url=url, download_path=self.download_path, is_audio=True, frame_rate=0, title=self.title)
                self.streams._append(st_ins)
            if re.search(self._quality_regex, text):
                resolution, frame_rate, hdr = re.search(self._quality_regex, text).groups()
                st_ins = Stream(url=url,
                                frame_rate=(frame_rate or 30),
                                resolution=resolution, is_hdr=bool(hdr),
                                title=self.title,
                                download_path=self.download_path)
                self.streams._append(st_ins)

    def dict(self):
        return {
            'title': self.title,
            'author': self.owner,
            'duration': self.duration,
            'thumbnail': self.thumbnail,
            'down_url': self.streams.filter(is_audio=True)[2].url,
            'captions': self.captions.subtitles,
            'translatable_captions': self.captions.translations
        }
