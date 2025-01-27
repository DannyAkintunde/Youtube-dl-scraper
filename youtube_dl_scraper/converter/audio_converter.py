import ffmpeg
import os
from typing import Optional
from .base_converter import BaseConverter


class AudioConverter(BaseConverter):
    """
    AudioConverter provides functionality to convert audio files into different formats
    by either re-encoding or copying the existing audio stream with the specified audio codec.

    Attributes:
        input_path (str): Path to the input audio or video file.
        output_path (str): Path to the output audio file.
        audio_codec (str): Desired audio codec (e.g., "aac", "mp3").
        bitrate (Optional[str]): Desired audio bitrate (e.g., "128k", "192k").
        force_render (bool): If True, forces re-rendering even if codecs match.
        experimental (bool): If True, allows experimental codec support by ffmpeg.
    """

    def __init__(
        self,
        input_path: str,
        output_path: str,
        audio_codec: Optional[str],
        bitrate: Optional[str] = None,
        force_render: bool = False,
        experimental: bool = True,
    ):
        """
        Initialize the AudioConverter instance.

        Args:
            input_path (str): Path to the input audio or video file.
            output_path (str): Path to the output audio file.
            audio_codec (Optional[str]): Desired audio codec (e.g., "aac", "mp3").
            bitrate (Optional[str]): Desired audio bitrate (e.g., "128k", "192k").
            force_render (bool): If True, forces re-rendering even if codecs match.
            experimental (bool): If True, allows experimental codec support by ffmpeg.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.audio_codec = audio_codec
        self.bitrate = bitrate
        self.force_render = force_render
        self.experimental = experimental

    def delete_existing_output_file(self) -> bool:
        if self.check_path(self.output_path):
            output_codec = self.get_audio_codec(self.output_path)
            if output_codec == self.audio_codec and not self.force_render:
                print(
                    f"Output file '{self.output_path}' already matches the desired codec."
                )
                return False
            print(
                "Output file exists but does not match the specified codec or force_render is enabled. Overwriting..."
            )
            os.remove(self.output_path)
            return True

    @staticmethod
    def get_audio_codec(file_path: str) -> Optional[str]:
        """
        Retrieve the audio codec of a file using FFmpeg.

        Args:
            file_path (str): Path to the file (audio or video).

        Returns:
            Optional[str]: The audio codec of the file, or None if no audio stream is found.

        Raises:
            RuntimeError: If FFmpeg probing fails.
        """
        try:
            probe = ffmpeg.probe(file_path)
            audio_stream = next(
                (
                    stream
                    for stream in probe["streams"]
                    if stream["codec_type"] == "audio"
                ),
                None,
            )
            return audio_stream["codec_name"] if audio_stream else None
        except ffmpeg.Error as e:
            raise RuntimeError(f"FFmpeg probing failed: {e.stderr.decode()}")

    def get_default_extension(self) -> str:
        """
        Determine the appropriate file extension based on the audio codec.

        Returns:
            str: A suitable file extension (e.g., ".mp3", ".m4a").
        """
        codec_to_extension = {
            "aac": "m4a",
            "mp3": "mp3",
            "flac": "flac",
            "opus": "opus",
            "wav": "wav",
        }
        return codec_to_extension.get(self.audio_codec, "m4a")

    def convert(self) -> str:
        """
        Perform the conversion process.

        Converts the input audio or video file into the desired audio format with the specified codec and bitrate.
        If the input codec matches the desired codec and `force_render` is False, it will simply copy the stream.

        Returns:
            str: Path to the converted audio file if successful.

        Raises:
            FileNotFoundError: If the input file does not exist or the output file was not created.
            RuntimeError: If the FFmpeg conversion process fails.
        """
        # Validate input file existence
        if not self.check_path(self.input_path):
            raise FileNotFoundError(f"Input file '{self.input_path}' not found.")

        # Generate dynamic output path if output_path is "."
        if self.output_path == ".":
            base, _ = os.path.splitext(self.input_path)
            self.output_path = f"{base}-converted.{self.get_default_extension()}"

        if not self.delete_existing_output_file():
            return self.output_path

        # Check the codec of the input file
        input_codec = self.get_audio_codec(self.input_path)

        print(f"Input Audio Codec: {input_codec}")
        print(f"Output Audio Codec: {self.audio_codec or 'copy'}")

        ffmpeg_options = {
            "vn": None,
            "strict": "experimental" if self.experimental else None,
        }
        if not self.force_render and input_codec == self.audio_codec:
            print("Matching codec found. Copying audio stream without re-encoding...")
            ffmpeg_options["codec"] = "copy"
        else:
            print("Re-encoding audio to match the desired codec and bitrate...")
            ffmpeg_options["acodec"] = self.audio_codec
            if self.bitrate:
                ffmpeg_options["audio_bitrate"] = self.bitrate

        # Perform conversion
        self.run_conversion(self.input_path, self.output_path, ffmpeg_options)

        # Verify output file creation
        if not self.check_path(self.output_path):
            raise FileNotFoundError("Output file was not created.")

        print(f"Conversion complete. Output saved at: {self.output_path}")
        return self.output_path
