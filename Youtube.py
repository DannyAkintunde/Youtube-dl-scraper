import atexit
import random
import json
from pathlib import Path
from .Video import Video
from ua_generator import generate as ua_gen
from ua_generator.options import Options
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page, Route, TimeoutError

"""
class OldYoutube:
    _devices = ('desktop', 'mobile')
    _platforms = ('windows', 'macos', 'ios', 'linux', 'android')
    _browsers = ('chrome', 'edge', 'firefox', 'safari')

    def __init__(self, protocol='https', proxies: dict[str] | None = None, verify_ssl: bool = True):
        self.host = f'{protocol}://retatube.com'
        self._host = 'retatube.com'
        self._form_endpoint = '/api/v1/aio/index'
        self._protocol = protocol
        self._session = requests.Session()
        self._session.headers.update(self.generate_ua('').headers.get())
        self._prefix, self._dl_endpoint = self._get_endpoint_data()

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value: str):
        self.host = '{}://{}'.format(value, self._host)
        self._protocol = value

    @staticmethod
    def generate_ua(device: str):
        options = Options(weighted_versions=True)
        ua = ua_gen(platform=Youtube._platforms, device=Youtube._devices, browser=Youtube._browsers, options=options)
        ua.headers.accept_ch('Sec-CH-UA-Platform-Version, Sec-CH-Full-Version-List')
        return ua

    def _get_endpoint_data(self) -> tuple:
        self._session.get(self.host)
        params = {
            's': self._host
        }
        print(self.host, self._host)
        form = self._session.get(f'{self.host}{self._form_endpoint}', params=params)
        form_soup = BeautifulSoup(form.content, 'html.parser')
        prefix = form_soup.find('input', attrs={'type': 'hidden'})['value']
        dl_endpoint = form_soup.find('button', attrs={'id': 'search-btn'})['hx-post']
        print(dl_endpoint)
        return prefix, dl_endpoint

    def search(self, url: str) -> Video:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        form_data = {
            'vid': url,
            'prefix': self._prefix
        }
        payload = urllib.parse.urlencode(form_data)
        print(payload)

        data = self._session.post(f'{self.host}{self._dl_endpoint}', data=payload, headers=headers)
        # print(data.text)
        # video_soup = BeautifulSoup(data.content, "html.parser")
        return Video(data.content)
"""


class Youtube:
    _devices = ('desktop', 'mobile')
    _platforms = ('windows', 'macos', 'ios', 'linux', 'android')

    def __init__(self, protocol: str = 'https', download_folder: str = 'downloads', proxies : list[dict] = []):
        self.host = f'{protocol}://retatube.com'
        self.subtitle_host = f'{protocol}://downsub.com'
        self._host = 'retatube.com'
        self._subtitle_host = 'downsub.com'
        self._protocol = protocol
        self._playwright: Playwright = sync_playwright().start()
        self.proxies = proxies
        self.proxy = None
        
        if len(self.proxies) > 1:
            self.proxy = random.choice(self.proxies)
        elif len(self.proxies) == 1:
            self.proxy = self.proxies[0]

        self._browsers: dict[str, Browser] = {
            'chromium': self._playwright.chromium.launch(proxy=self.proxy),
            'firefox': self._playwright.firefox.launch(proxy=self.proxy),
            'webkit': self._playwright.webkit.launch(proxy=self.proxy)
        }
        self._page: Page | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._browser_name: str | None = None
        self._download_data_html: str | None = None
        self.download_location = download_folder
        
        atexit.register(self.close)
        Path(self.download_location).mkdir(exist_ok=True, parents=True)

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value: str):
        self.host = '{}://{}'.format(value, self._host)
        self.subtitle_host = '{}://{}'.format(value, self._subtitle_host)
        self._protocol = value

    @staticmethod
    def generate_ua(browser: str):
        browser_options = ()
        if browser == 'chromium':
            browser_options = ('chrome', 'edge')
        elif browser == 'firefox':
            browser_options = ('firefox',)
        elif browser == 'webkit':
            browser_options = ('safari',)
        options = Options(weighted_versions=True)
        ua = ua_gen(platform=Youtube._platforms, device=Youtube._devices, browser=browser_options, options=options)
        ua.headers.accept_ch('Sec-CH-UA-Platform-Version, Sec-CH-Full-Version-List')
        return ua

    def search(self, url: str, only_caption: bool = False, only_video: bool = False) -> Video:
        browser_name = random.choice(list(self._browsers.keys()))
        browser = self._browsers[browser_name]
        context = browser.new_context(
            extra_http_headers=Youtube.generate_ua(browser_name).headers.get()
        )
        page = context.new_page()
        download_data_html = ''
        if not only_caption:
            page.goto(self.host)
            page.fill('#aio-url-input', url)
            page.click('#search-btn')
            page.wait_for_selector('div#aio-parse-result')

            download_buttons_selector = "a.button.primary:not([href='javascript:void(0);'])"

            page.evaluate(f"""
                let download_links = document.querySelectorAll("{download_buttons_selector}")
                download_links.forEach((link) => link.addEventListener('click', (e) => e.preventDefault()))
            """)

            download_buttons = page.query_selector_all(download_buttons_selector)

            for button in download_buttons:
                button.click()

            download_data_html = page.inner_html('div#aio-parse-result')
        
        caption_data = {
            'json': dict(),
            'status': 404,
            'headers': dict()
        }
        if not only_video:
            caption_data = self.get_caption_data(url, browser_context=context)

        page.close()
        context.close()

        return Video(url, download_data_html, caption_data, self.download_location, caption_only=only_caption, video_only=only_video)

    def get_caption_data(self, url: str, browser_context: BrowserContext):
        if not browser_context:
            browser_name = random.choice(list(self._browsers.keys()))
            browser = self._browsers[browser_name]
            context = browser.new_context(
                extra_http_headers=Youtube.generate_ua(browser_name).headers.get()
            )
        else:
            context = browser_context
        caption_data = {
            'json': dict(),
            'status': 404,
            'headers': dict()
        }

        def caption_api_route_handler(route: Route):
            response = route.fetch(headers={'Accept': 'application/json;charset=UTF-8', 'Accept-Charset': 'UTF-8'})
            # print(response.body())
            if response.status == 200:
                caption_data['json'] = response.json()
            caption_data['status'] = response.status
            caption_data['headers'] = response.headers
            route.abort()
            # route.fulfill(response=response)

        page = context.new_page()
        page.route('https://get-info.downsub.com/*', caption_api_route_handler)
        try:
            page.goto(f"{self.subtitle_host}?url={url}", timeout=30000, wait_until='domcontentloaded')
            page.wait_for_selector(
                "#app > div > main > div > div.container.ds-info.outlined > div > div.row.no-gutters > "
                "div.pr-1.col-sm-7.col-md-6.col-12 > div.v-card.v-card--flat.v-sheet.theme--light > "
                "div.d-flex.flex-no-wrap.justify-start > div.ma-0.mt-2.text-center > a > div > "
                "div.v-responsive__content")
            page.close()
            context.close()
        except TimeoutError:
            print("Page taking too long to load")

        finally:
            try:
                page.close()
                context.close()
            except:
                pass

        return caption_data

    def close(self):
        try:
            for browser in self._browsers.values():
                browser.close()
            self._playwright.stop()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

"""
# Testing

yt = Youtube()
vid = yt.search('https://youtu.be/McRkeActwxU?si=VXID6gkLq_xu1Qv3')
print(vid.dict())
print(vid.captions.get_captions_by_name('English'))
print(vid.captions.get_captions_by_name('English').srt(skip_existent=True))
print(vid.captions.get_captions_by_lang_code('en_auto'))
print(vid.captions.get_captions_by_lang_code('en_auto').srt(skip_existent=True))
print(vid.captions.get_translated_captions_by_name('Basque'))
print(vid.captions.get_translated_captions_by_name('Basque').srt(skip_existent=True))
print(vid.captions.get_translated_captions_by_lang_code('fr'))
print(vid.captions.get_translated_captions_by_lang_code('fr').srt())
# print(vid.streams.filter(is_audio=True)[2].download())

for aud in vid.streams.filter(is_audio=True):
    print(aud)



print(vid.streams.get_highest_resolution())
print(vid.streams.get_highest_resolution().url)
print(vid.streams.filter(is_video=True))
# print(vid.streams[0])
# print(vid.streams.filter(progressive=False)[-2].download())  # download lowest adaptive video
print(vid.streams.filter(is_audio=True)[0].download())  # download video audio


vid = yt.search("https://youtube.com/watch?v=sdgwHXt2wAk")
print(vid.title)
print(vid.owner)
print(vid.streams)
print(vid.streams.get_highest_resolution())
print(vid.streams.get_highest_resolution().url)
print(vid.streams.get_audio())
print(vid.streams.get_audio().url)

for v in vid.streams:  # .filter(is_audio=True):
    print(v)
    print(v.url)


"""
