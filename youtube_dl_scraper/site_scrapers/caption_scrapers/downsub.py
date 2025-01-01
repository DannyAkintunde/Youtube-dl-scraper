# youtube_dl_scraper/site_scrapers/caption_scrapers/downsub.py
import re
import requests
from langcodes import find as find_language
from youtube_dl_scraper.core.caption_array import CaptionArray
from youtube_dl_scraper.core.base_scraper import BaseScraper
from youtube_dl_scraper.core.exceptions import (
    YouTubeDLScraperError,
    ScraperExecutionError,
    PlaywrightError,
    CaptionsNotFoundError,
)
from youtube_dl_scraper.utils.playwright_runner import Playwright

payload = """
# import random
from  playwright.async_api import async_playwright, Error as PlaywrightError
import asyncio

async def main():
    async with async_playwright() as pr:
        browsers = {
            "chromium": pr.chromium,
            "webkit": pr.webkit,
            "firefox": pr.firefox
        }
        # browser_name = random.choice(["chromium", "webkit", "firefox"])
        browser_name = "firefox" # using firedox bacause it dosen't get flaged by cloudfare
        browser_type = browsers[browser_name]
        print(browser_name)
        browser = await browser_type.launch()
        context = await browser.new_context()
        page = await context.new_page()
        
        caption_data = {'url': str()}
        
        async def caption_api_route_handler(route, request):
            # response = await route.fetch(headers={'Accept': 'application/json;charset=UTF-8', 'Accept-Charset': 'UTF-8'})
            
            caption_data['url'] = request.url
            print('{{' + caption_data['url'] + '}}')
            await route.abort()
            await page.screenshot(path="collected.png")
            await page.close()
        
        await page.route('https://get-info.downsub.com/*', caption_api_route_handler)
        await context.route("**/*ads**", lambda route: route.abort())
        try:
            await page.goto(f'https://downsub.com?url={url}', timeout=86400000, wait_until='domcontentloaded')
            await page.screenshot(path="loaded.png")
            await page.wait_for_selector('#app > div > main > div > div.container.ds-info.outlined > div > div.row.no-gutters > div.pr-1.col-sm-7.col-md-6.col-12 > div.v-card.v-card --flat.v-sheet.theme--light > div.d-flex.flex-no-wrap.justify-start > div.ma-0.m t-2.text-center > a > div > div.v-responsive__content')
        except PlaywrightError as e:
            if "Page.wait_for_selector: Target page, context or browser has been closed" in str(e) or "Timeout" in str(e):
                print("Page taking too long to load")
            else:
                raise e
        finally:
          try:
              await context.close()
              await browser.close()
          except:
              pass

asyncio.run(main())
"""


class DownSub(BaseScraper):
    """A scraper wrapper for downsub.com"""

    # meta data
    __name__ = "DownSub"
    __type__ = "caption"
    __host__ = "downsub.com"

    def generate_payload(self, url: str) -> str:
        """generate payload to fetch caption endpoint"""
        return f"url = '{url}'\n" + payload

    def scrape_captions(self, url: str) -> dict:
        f"""scrape {self.__host__} to get a formatted dictionary of captions"""
        try:
            response = Playwright().run(self.generate_payload(url))
            if response.get("success") and response.get("status_code") == 200:
                caption_endpoint_match = re.search(
                    r"\{\{(.+)\}\}", response.get("output", "")
                )
                if caption_endpoint_match:
                    caption_endpoint = caption_endpoint_match.group(1)
                    return self.process_response(caption_endpoint)
                else:
                    raise CaptionsNotFoundError("No captions found in response.")
            else:
                raise YouTubeDLScraperError(
                    f"Failed to fetch captions: {response.get('error', 'Unknown error')}"
                )
        except PlaywrightError as e:
            raise ScraperExecutionError(f"Playwright Error occured: {str(e)}")

    def process_response(self, caption_endpoint: str) -> dict:
        """fetch and processes data from the caption endpoint"""
        if not caption_endpoint:
            raise CaptionsNotFoundError("Caption endpoint is empty.")
        response = requests.get(caption_endpoint)
        if response.status_code == 200:
            data = response.json()
            return self.parse_caption_data(data) if data else None
        else:
            raise YouTubeDLScraperError(
                "Invalid response code: {}".format(response.status_code)
            )

    def parse_caption_data(self, data: dict) -> dict:
        """parse data from the caption endpoint to a general format"""
        if data.get("sourceName") != "Youtube":
            raise CaptionsNotFoundError("Capition found but invalid caption type")
        captions_data = {}  # the formatted dictionary for caption data
        dl_api = data.get("urlSubtitle")
        captions_data["title"] = data.get("title", "")
        captions_data["thumbnail"] = data.get("thumbnail", "")
        captions_data["duration"] = data.get("duration")
        captions_data["subtitles"] = []
        for sub in data.get("subtitles", []):
            sub["code"] = (
                "a." + str(find_language(sub["name"]))
                if "auto" in sub["code"]
                else sub["code"]
            )
            captions_data["subtitles"].append(sub)
        captions_data["translations"] = []
        for sub in data.get("subtitlesAutoTrans", []):
            sub["code"] = str(find_language(sub["name"]))  # fetch lang code
            captions_data["translations"].append(sub)
        # add more formating to include dowload url for each formart i.e. srt, txt, raw
        translation_types = ("subtitles", "translations")
        for t_type in translation_types:
            subs = captions_data[t_type]  # subtitle dict
            for sub in subs:  # for subtitle in subtitles
                sub["urls"] = {
                    "raw": f"{dl_api}?url={sub['url']}&type=raw&title={captions_data['title']}",
                    "txt": f"{dl_api}?url={sub['url']}&type=txt&title={captions_data['title']}",
                    "srt": f"{dl_api}?url={sub['url']}&title={captions_data['title']}",
                }
                sub.pop("url")

        # print(captions_data)
        return captions_data
