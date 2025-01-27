import ffmpeg
import os
from typing import Optional, Dict
from .base_converter import BaseConverter


class VideoConverter(BaseConverter):
    """
    VideoConverter class provides functionality to convert video files into different formats
    by re-encoding or copying the existing streams with specified video and audio codecs.

    Attributes:
        input_path (str): Path to the input video file.
        output_path (str): Path to the output video file.
        video_codec (str): Desired video codec (e.g., "h264", "hevc").
        audio_codec (Optional[str]): Desired audio codec (e.g., "aac", "mp3").
        force_render (bool): If True, forces re-rendering even if codecs match.
        experimental (bool): If True, allow for experimental codec supported by ffmpeg else don't.
    """

    def __init__(
        self,
        input_path: str,
        output_path: str,
        video_codec: str,
        audio_codec: Optional[str],
        force_render: bool = False,
        experimental: bool = True,
    ):
        """
        Initialize the converter.

        Args:
            input_path (str): Path to the input video file.
            output_path (str): Path to the output video file.
            video_codec (str): Desired video codec (e.g., "h264", "hevc").
            audio_codec (Optional[str]): Desired audio codec (e.g., "aac", "mp3").
            force_render (bool): If True, force re-rendering even if codecs match.
            experimental (bool): If True, allow for experimental codec supported by ffmpeg else don't.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.video_codec = video_codec
        self.audio_codec = audio_codec
        self.force_render = force_render
        self.experimental = experimental

    def delete_existing_output_file(self) -> bool:
        if self.check_path(self.output_path):
            output_codecs = self.get_codecs(self.output_path)
            output_video_codec = output_codecs["video"]
            output_audio_codec = output_codecs["audio"]

            if output_video_codec == self.video_codec and output_audio_codec == (self.audio_codec or "aac") and not self.force_render:
                print(
                    f"Output file '{self.output_path}' already matches the desired codec."
                )
                return False
            print(
                "Output file exists but does not match the specified codec or force_render in enabled. Overwriting..."
            )
            os.remove(self.output_path)
            return True

    @staticmethod
    def get_codecs(file_path: str) -> Dict[str, Optional[str]]:
        """
        Retrieve the codecs of a file using ffmpeg-python.

        Args:
            file_path (str): Path to the video file.

        Returns:
            dict: A dictionary with 'video' and 'audio' keys containing their respective codecs.
        """
        probe = ffmpeg.probe(file_path)
        video_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )
        audio_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "audio"),
            None,
        )

        return {
            "video": video_stream["codec_name"] if video_stream else None,
            "audio": audio_stream["codec_name"] if audio_stream else None,
        }

    def convert(self) -> str:
        """
        Perform the conversion.

        Skips re-rendering if the codecs already match, unless force_render is True.

        Returns:
            str: Path to the converted video if successful.
        """
        if not self.check_path(self.input_path):
            raise FileNotFoundError(f"Input file '{self.input_path}' not found.")

        # Handle output path being "."
        if self.output_path == ".":
            base, ext = os.path.splitext(self.input_path)
            self.output_path = f"{base}-converted{ext}"

        if not self.delete_existing_output_file():
            return self.output_path

        codecs = self.get_codecs(self.input_path)
        input_video_codec = codecs["video"]
        input_audio_codec = codecs["audio"]

        print(f"Input Video Codec: {input_video_codec}")
        print(f"Input Audio Codec: {input_audio_codec}")
        print(f"Output Video Codec: {self.video_codec}")
        print(f"Output Audio Codec: {self.audio_codec or 'copy'}")

        ffmpeg_options = {
            "strict": "experimental" if self.experimental else None,
        }
        # Check if re-rendering is needed
        if (
            not self.force_render
            and input_video_codec == self.video_codec
            and input_audio_codec == self.audio_codec
        ):
            print("Codecs match! Copying streams without re-rendering...")
            # Copy streams directly
            ffmpeg_options["codec"] = "copy"
        else:
            print("Re-rendering with specified codecs...")
            # Re-encode with specified codecs
            ffmpeg_options["vcodec"] = self.video_codec or "copy"
            ffmpeg_options["acodec"] = self.audio_codec or "copy"

        self.run_conversion(self.input_path, self.output_path, ffmpeg_options)

        # Verify output file creation
        if not self.check_path(self.output_path):
            raise FileNotFoundError("Output file was not created.")

        print(f"Video conversion complete! File saved at: {self.output_path}")
        return self.output_path