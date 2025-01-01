# youtube_dl_scraper/site_scrapers/video_scrapers/__init__.py
# from youtube_dl_scraper.core.base_scraoer import BaseScraper
from youtube_dl_scraper.utils.registration import register_scrapers
from .savetube import SaveTube
from .y2save import Y2Save


def register(*scraper_objs):
    """Register video scrapers"""
    register_scrapers(scrapers, *scraper_objs)


# Register video scrapers
scrapers = {}
video_scrapers = scrapers

# register scrapers
register(SaveTube)
register(Y2Save)
