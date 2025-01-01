class YouTubeDLScraperError(Exception):
    """Base class for all exceptions"""


# scraper errors
class ScraperNotFoundError(YouTubeDLScraperError):
    """Raised when a requested scraper is not found."""

    def __init__(self, scraper_type, scraper_name):
        message = f"No {scraper_type} scraper found with name '{scraper_name}'."
        super().__init__(message)


class ScraperExecutionError(YouTubeDLScraperError):
    """Raised when a scraper fails during execution."""

    def __init__(self, scraper_name, details="An error occurred during scraping."):
        message = f"Error in scraper '{scraper_name}': {details}"
        super().__init__(message)


class VideoNotFoundError(ScraperExecutionError):
    """Raised when no captions were found"""


class CaptionsNotFoundError(ScraperExecutionError):
    """Raised when no captions were found"""


class UnsupportedScraperMethodError(YouTubeDLScraperError):
    """Raised when a scraper does not support the requested method."""

    def __init__(self, scraper_name, method_name):
        message = (
            f"Scraper '{scraper_name}' does not support the method '{method_name}'."
        )
        super().__init__(message)


class FileExistsError(YouTubeDLScraperError):
    "Reaised when a file exists"

    def __init__(self, file_exist, path):
        message = f"{file_exist} in {path}"
        super().__init__(message)


class PlaywrightError(YouTubeDLScraperError):
    """Raised when Playwright payload execution fails"""

    def __init__(
        self, message, status_code=200, successfull_process=False, error="", output=""
    ):
        self.message = f"Reason: {message} Status code: {status_code}"
        self.status_code = status_code
        self.successfull_process = successfull_process
        self.error = error or message
        self.output = output

        super().__init__(self.message)
