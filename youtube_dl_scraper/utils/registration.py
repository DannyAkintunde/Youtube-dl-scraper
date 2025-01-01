from youtube_dl_scraper.core.base_scraper import BaseScraper


def register_scrapers(scrapers_dict, *scraper_objs):
    """Register scrapers in the provided dictionary"""
    for scraper in scraper_objs:
        if issubclass(scraper, BaseScraper):
            scrapers_dict[scraper.__name__.lower()] = scraper
