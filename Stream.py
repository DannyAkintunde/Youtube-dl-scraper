import requests
from pathlib import Path
from tqdm import tqdm


class Stream:

    def __init__(self, url: str, download_path: str, resolution: str | None = None, bit_rate: str | None = '128kbps', frame_rate: int = 30,
                 is_hdr: bool = False,
                 is_audio: bool = False, title: str | None = '', file_name: str | None = None):
        self.url = url
        self.title = title
        self.is_hdr = is_hdr
        self.is_audio = is_audio
        self.is_video = not self.is_audio
        self.progressive = False
        self.adaptive = True
        self.resolution = resolution
        self.frame_rate = frame_rate
        self.bit_rate = bit_rate
        self.file_name = file_name
        self.download_path = download_path
        if resolution == '360p':
            self.adaptive = False
            self.progressive = True
        if not file_name:
            self.file_name = f'{self.title}'
            if is_audio:
                self.file_name += '.mp3'
            else:
                self.file_name += f"-{self.resolution}{self.frame_rate}{'HDR' if self.is_hdr else ''}.mp4"

        self.file_name = self.file_name.replace('"', '').replace('\\', '')

    def __str__(self):
        if self.is_audio:
            return '(audio mp4 {})'.format(self.bit_rate)
        return '({}{}{})'.format(self.resolution, self.frame_rate or '', ' HDR' if self.is_hdr else '')

    def __repr__(self):
        # return '<Stream object {}>'.format()
        return f'<Stream(title="{self.title}", resolution="{self.resolution}", frame_rate={self.frame_rate}, is_audio={self.is_audio}, is_hdr={self.is_hdr})>'

    def download(self, file_name: str | None = None, download_dir: str | None = None) -> str:
        file_name = file_name if file_name else self.file_name
        download_path = download_dir if download_dir else self.download_path
        file_path = Path(download_path).joinpath(file_name)
        try:
            with requests.get(self.url, stream=True) as response:
                if response.status_code == 200 and 'text/plain' not in response.headers.get('content-type'):
                    total_size = int(response.headers.get('content-length', 0))
                    with file_path.open('wb') as file, tqdm(
                            desc='Downloading {}'.format(file_name),
                            total=total_size,
                            unit='B',
                            unit_scale=True,
                            unit_divisor=1024,
                            ncols=80) as progress_bar:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                                progress_bar.update(len(chunk))
                        print(f"Download completed: {file_name}")
                        return str(file_path.resolve())
                else:
                    print(f"Failed to download. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occured: {e}")
            raise e
