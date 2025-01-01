from youtube_dl_scraper.site_scrapers import caption_scrapers, video_scrapers
from .base_scraper import BaseScraper


class ScraperManager:
    """Manages the collection of video and caption scrapers, allowing retrieval and listing of scrapers."""

    def __init__(self):
        """
        Initialize the ScraperManager with video and caption scrapers.

        Attributes:
            video_scrapers (dict): A dictionary of video scrapers.
            caption_scrapers (dict): A dictionary of caption scrapers.
        """
        self.video_scrapers = video_scrapers
        self.caption_scrapers = caption_scrapers

    def get_scraper_class(self, scraper_type: str, name: str) -> BaseScraper:
        """
        Retrieve a specific scraper class by its type and name.

        Args:
            scraper_type (str): The type of scraper, either 'video' or 'caption'.
            name (str): The name of the specific scraper to retrieve.

        Returns:
            BaseScraper: The scraper class corresponding to the given type and name.

        Raises:
            ValueError: If no scraper is found with the provided name and type.
        """
        scrapers = getattr(self, f"{scraper_type.lower()}_scrapers", {})
        scraper = scrapers.get(name)
        if not scraper:
            raise ValueError(f"No {scraper_type} scraper found with name '{name}'")
        return scraper

    def list_scrapers(self) -> dict:
        """
        List all available scrapers by type.

        Returns:
            dict: A dictionary containing lists of available video and caption scrapers under
                  the keys "video_scrapers" and "caption_scrapers".
        """
        return {
            "video_scrapers": list(self.video_scrapers.keys()),
            "caption_scrapers": list(self.caption_scrapers.keys()),
        }
