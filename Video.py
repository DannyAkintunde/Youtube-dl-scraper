import re
from bs4 import BeautifulSoup
from .Stream import Stream
from .StreamArray import StreamArray
from .Caption import Captions


class Video:
    _quality_regex = r'\((\d+p)(\d+)?(\s[A-z]{2,3})?\)'
    _bit_rate_pattern = ['48kbps', '128kbps', '32kbps']

    def __init__(self, view_url: str, raw_html='', caption_data: dict = {}, download_path: str = None, caption_only: bool = False, video_only: bool = False):
        self.captions = None
        self.duration = None
        self.streams = None
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
        if not caption_only and video_only:
          self.parse_streams_data()
        elif not video_only and caption_only:
          self.parse_caption_data()
        else:
            self.parse_streams_data()
            self.parse_caption_data()
    def parse_data(self):
        thumbnail_img = self.soup.find('div', attrs={'class': 'icon-box-img'}).find('img')
        self.thumbnail = {
            'width': int(thumbnail_img['width']),
            'height': int(thumbnail_img['height']),
            'url': thumbnail_img['src'],
            'yt-thumb': self.caption_data['json'].get('thumbnail')
        }
        self.duration = self.caption_data['json'].get('duration')
        video_info = self.soup.find('div', attrs={'class': 'icon-box-text'}).find('div', attrs={'class': 'text'})
        video_info_paragraphs = video_info.find_all('p')
        self.title = video_info_paragraphs[0].get_text()[6:].strip()
        self.owner = video_info_paragraphs[1].get_text()[6:].strip()

    def parse_streams_data(self):
        streams_data = self.soup.find_all("div", attrs={'class': 'col-inner'})[-1]
        streams_data_a = streams_data.find_all("a")[:-1]
        # print(streams_data_a[-1])
        # print(streams_data)

        self.streams = StreamArray()

        # this works but note it through observation from the site

        bit_rate_index = 0
        for stream in streams_data_a:
            url = stream['href']
            text = stream.get_text()
            if 'mp3' in text.lower():
                bit_rate = Video._bit_rate_pattern[bit_rate_index]
                st_ins = Stream(url=url, download_path=self.download_path, is_audio=True, frame_rate=0,
                                title=self.title, bit_rate=bit_rate)
                self.streams._append(st_ins)
                bit_rate_index += 1
            if re.search(self._quality_regex, text):
                resolution, frame_rate, hdr = re.search(Video._quality_regex, text).groups()
                st_ins = Stream(url=url,
                                frame_rate=(frame_rate or 30),
                                resolution=resolution, is_hdr=bool(hdr),
                                title=self.title,
                                download_path=self.download_path)
                self.streams._append(st_ins)
    
    def parse_caption_data(self):
        self.captions = Captions(self.title, self.caption_data, self.download_path)

    def dict(self):
        return {
            'title': self.title,
            'author': self.owner,
            'view_url': self.view_url,
            'duration': self.duration,
            'thumbnail': self.thumbnail,
            'captions': self.captions.subtitles,
            'translatable_captions': self.captions.translations,
            'resolutions': self.streams.get_available_resolutions(), # sorted(remove_duplicates(filter(lambda x: x is not None, [stream.resolution for stream in self.streams])), key= lambda char: int(char[:-1]),reverse=True),
            'bit_rates': self.streams.get_available_bit_rates(), # sorted(remove_duplicates(filter(lambda x: x is not None, [stream.abr for stream in self.streams.filter(only_audio=True)])), key= lambda char: int(char[:-4]),reverse=True),
            'frame_rates': self.streams.get_avaliable_frame_rates(),
            'streams': [str(stream) for stream in self.streams],
            'down_url':{
                "video": {stream.resolution: { 'url': stream.url, 'progressive': stream.progressive } for stream in self.streams},
                "audio": {stream.abr: stream.url for stream in self.streams.filter(is_audio=True)}
            }
        }
