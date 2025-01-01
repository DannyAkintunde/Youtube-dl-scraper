import ffmpeg
import os
from typing import Optional
from .base_converter import BaseConverter


class AudioConverter(BaseConverter):
    """
    AudioConverter class provides functionality to convert audio files into different formats
    by re-encoding or copying the existing audio stream with the specified audio codec.

    Attributes:
        input_path (str): Path to the input audio or video file.
        output_path (str): Path to the output audio file.
        audio_codec (str): Desired audio codec (e.g., "aac", "mp3").
        bitrate (Optional[str]): Desired audio bitrate (e.g., "128k", "192k").
        force_render (bool): If True, forces re-rendering even if codecs match.
        experimental (bool): If True, allow for experimental codec supported by ffmpeg else don't.
    """
    def __init__(
        self,
        input_path: str,
        output_path: str,
        audio_codec: Optional[str],
        bitrate: Optional[str] = None,
        force_render: bool = False,
        experimental: bool = True
    ):
        """
        Initialize the converter.

        Args:
            input_path (str): Path to the input file (audio or video).
            output_path (str): Path to the output audio file.
            audio_codec (Optional[str]): Desired audio codec (e.g., "aac", "mp3").
            bitrate (Optional[str]): Desired audio bitrate (e.g., "128k", "192k").
            force_render (bool): If True, force re-rendering even if codecs match.
            experimental (bool): If True, allow for experimental codec supported by ffmpeg else don't.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.audio_codec = audio_codec
        self.bitrate = bitrate
        self.force_render = force_render
        self.experimental = experimental

    @staticmethod
    def get_audio_codec(file_path: str) -> Optional[str]:
        """
        Retrieve the audio codec of a file using ffmpeg-python.

        Args:
            file_path (str): Path to the file (audio or video).

        Returns:
            Optional[str]: The audio codec of the file, or None if no audio stream is found.
        """
        probe = ffmpeg.probe(file_path)
        audio_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "audio"),
            None,
        )
        return audio_stream["codec_name"] if audio_stream else None

    def get_default_extension(self) -> str:
        """
        Determine the appropriate file extension based on the audio codec.

        Returns:
            str: A suitable file extension (e.g., ".mp3", ".m4a").
        """
        codec_to_extension = {
            "aac": "m4a",  # AAC is typically stored in M4A
            "mp3": "mp3",
            "flac": "flac",
            "opus": "opus",
            "wav": "wav",
        }
        return codec_to_extension.get(
            self.audio_codec, "m4a"
        )  # Default to m4a for unsupported codecs

    def convert(self) -> str:
        """
        Perform the conversion.

        Converts input audio or video file into the desired audio format, with an optional bitrate.

        Returns:
            str: Path to the converted audio file if successful.

        Raises:
            FileNotFoundError: If the input file does not exist or the output file was not created.
        """
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input file '{self.input_path}' not found.")

        # Handle output path being "."
        if self.output_path == ".":
            base, _ = os.path.splitext(self.input_path)
            self.output_path = f"{base}-audio-converted{'-' + self.bitrate if self.bitrate else ''}.{self.get_default_extension()}"

        if os.path.exists(self.output_path):
            output_codec = self.get_audio_codec(self.output_path)
            print(f"Output Audio Codec: {output_codec}")

            if output_codec == self.audio_codec:
                print("Output file exists and matches the specified codec.")
                return self.output_path
            else:
                print(
                    "Output file exists but does not match the specified codec. Overwriting..."
                )
                os.remove(self.output_path)

        input_codec = self.get_audio_codec(self.input_path)
        print(f"Input Audio Codec: {input_codec}")

        # Extract or convert the audio stream
        if not self.force_render and input_codec == self.audio_codec:
            print("Codec matches! Copying audio stream without re-rendering...")
            (
                ffmpeg.input(self.input_path)
                .output(self.output_path, codec="copy", vn=None, strict=(self.experimental and 'experimental') or None)
                .run()
            )
        else:
            print(
                "Extracting and/or re-rendering audio with the specified codec and bitrate..."
            )
            ffmpeg_output_options = {"acodec": self.audio_codec or "copy", "vn": None}
            if self.bitrate:
                ffmpeg_output_options["audio_bitrate"] = self.bitrate

            (
                ffmpeg.input(self.input_path)
                .output(self.output_path, **ffmpeg_output_options, strict=(self.experimental and 'experimental') or None)
                .run()
            )

        if os.path.exists(self.output_path):
            print(f"Audio conversion complete! File saved at: {self.output_path}")
            return self.output_path
        else:
            raise FileNotFoundError("Output file was not created.")