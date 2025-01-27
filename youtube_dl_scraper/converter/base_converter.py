import os
import ffmpeg


class BaseConverter:
    """Base class for converters"""

    def __init__(self, input_path, output_path):
        """Intialize setup converter."""
        self.input_path = input_path
        self.output_path = output_path

    @staticmethod
    def check_path(path: str) -> bool:
        """
        Check if a file or directory exists at the specified path.

        Args:
            path (str): Path to check.

        Returns:
            bool: True if the path exists, False otherwise.
        """
        return os.path.exists(path)

    @staticmethod
    def run_conversion(input_path: str, output_path: str, options: dict):
        """
        Execute the FFmpeg conversion process with the specified options.

        Args:
            input_path (str): Path to the input file.
            output_path (str): Path to the output file.
            options (dict): FFmpeg options to apply during conversion.

        Raises:
            RuntimeError: If the FFmpeg process fails.
        """
        try:
            (ffmpeg.input(input_path).output(output_path, **options).run())
        except ffmpeg.Error as e:
            raise RuntimeError(f"FFmpeg conversion failed: {e.stderr.decode()}")

    def convert(self):
        "Converts media to specified format/codec"
        raise NotImplementedError("This method should be implemented by subclasses.")
