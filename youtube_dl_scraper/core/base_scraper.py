class BaseScraper:
    """Base class for scrapers"""

    __host__ = ""
    __name__ = "Base"

    def __init__(self, download_path: str):
        self.download_path = download_path

    def scrape(self, url: str):
        """Scrape youtube video data from site"""
        raise NotImplementedError("This method should be overwritten")

    async def async_scrape(self, url: str):
        """Scrapes youtube video data from sites asynchronously"""
        raise NotImplementedError("This method should be overwritten")

    # overwrite if scraper supports captions
    def scrape_captions(self, url: str):
        """Scrape youtube caprions data from site"""
        raise NotImplementedError("This method should be overwritten")

    async def async_scrape_captions(self, url: str):
        """Scrape youtube caprions data from site asynchronously"""
        raise NotImplementedError("This method should be overwritten")

    # use to add custom props
    def custom_prop(self, obj, data: str):
        """adds custom properties in data to obj"""
        return obj
