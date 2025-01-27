import pytest
from unittest.mock import patch
from youtube_dl_scraper.converter.audio_converter import AudioConverter


def test_convert_successful_conversion():
    """
    Test successful audio conversion with re-encoding.
    """
    converter = AudioConverter(
        input_path="input.mp4",
        output_path="output.m4a",
        audio_codec="mp3",
        bitrate="192k",
        force_render=True,
    )

    with patch(
        "os.path.exists",
        side_effect=lambda path: path == "input.mp4" or path == "output.m4a",
    ), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.delete_existing_output_file",
        return_value=True,
    ), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.get_audio_codec",
        return_value="aac",
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion:

        result = converter.convert()

        assert result == "output.m4a"
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "output.m4a",
            {
                "vn": None,
                "strict": "experimental",
                "acodec": "mp3",
                "audio_bitrate": "192k",
            },
        )


def test_convert_defualt_output_path_successful_conversion():
    """
    Test successful audio conversion with re-encoding and auto generated output path.
    """
    converter = AudioConverter(
        input_path="input.mp4",
        output_path=".",
        audio_codec="mp3",
        bitrate="192k",
        force_render=True,
    )

    with patch(
        "os.path.exists",
        side_effect=lambda path: path == "input.mp4" or path == "input-converted.mp3",
    ), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.delete_existing_output_file",
        return_value=True,
    ), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.get_audio_codec",
        return_value="aac",
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion:

        # Perform conversion
        result = converter.convert()

        # Assertions
        assert result == "input-converted.mp3"
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "input-converted.mp3",
            {
                "vn": None,
                "strict": "experimental",
                "acodec": "mp3",
                "audio_bitrate": "192k",
            },
        )


def test_convert_without_force_rerender_convertion_successful_output():
    """
    Test successful audio conversion without re-encoding and auto generated output path.
    """
    converter = AudioConverter(
        input_path="input.mp4",
        output_path="output.mp3",
        audio_codec="aac",
        bitrate="192k",
        force_render=False,
    )

    with patch(
        "os.path.exists",
        side_effect=lambda path: path == "input.mp4" or path == "output.mp3",
    ), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.delete_existing_output_file",
        return_value=True,
    ), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.get_audio_codec",
        return_value="aac",
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion:

        # Perform conversion
        result = converter.convert()

        # Assertions
        assert result == "output.mp3"
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "output.mp3",
            {
                "vn": None,
                "strict": "experimental",
                "codec": "copy",
            },
        )


def test_convert_with_force_rerender_convertion_successful_output():
    """
    Test successful audio conversion with re-encoding and auto generated output path.
    """
    converter = AudioConverter(
        input_path="input.mp4",
        output_path="output.mp3",
        audio_codec="aac",
        bitrate="192k",
        force_render=True,
    )

    with patch(
        "os.path.exists",
        side_effect=lambda path: path == "input.mp4" or path == "output.mp3",
    ), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.delete_existing_output_file",
        return_value=True,
    ), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.get_audio_codec",
        return_value="aac",
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion:

        # Perform conversion
        result = converter.convert()

        # Assertions
        assert result == "output.mp3"
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "output.mp3",
            {
                "vn": None,
                "strict": "experimental",
                "acodec": "aac",
                "audio_bitrate": "192k",
            },
        )


def test_convert_input_file_not_found():
    """
    Test conversion fails when the input file does not exist.
    """
    converter = AudioConverter(
        input_path="missing.mp4",
        output_path="output.m4a",
        audio_codec="mp3",
    )

    with patch("os.path.exists", side_effect=(lambda path: path != "missing.mp4")):
        with pytest.raises(
            FileNotFoundError, match="Input file 'missing.mp4' not found."
        ):
            converter.convert()


def test_convert_output_file_not_found():
    """
    Test conversion fails when the output file does not exist.
    """
    converter = AudioConverter(
        input_path="input.mp4",
        output_path="missing.m4a",
        audio_codec="mp3",
    )

    with patch("os.path.exists", side_effect=lambda path: path == "input.mp4"), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.delete_existing_output_file",
        return_value=True,
    ), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.get_audio_codec",
        return_value="aac",
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ):
        with pytest.raises(FileNotFoundError, match="Output file was not created."):
            converter.convert()


def test_convert_matching_codec_without_force_conversion():
    """
    Test conversion skips rendering when codecs match and force_render is False.
    """
    converter = AudioConverter(
        input_path="input.mp4",
        output_path="output.m4a",
        audio_codec="mp3",
        force_render=False,
    )

    with patch(
        "os.path.exists", side_effect=lambda path: path in ["input.mp4", "output.m4a"]
    ), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.get_audio_codec",
        side_effect=lambda path: path == "output.m4a" and "mp3",
    ):

        # Perform conversion
        result = converter.convert()

        # Assertions
        assert result == "output.m4a"

def test_convert_matching_codec_with_force_conversion_overwites_output():
    """
    Test conversion skips rendering when codecs match and force_render is True.
    """
    converter = AudioConverter(
        input_path="input.mp4",
        output_path="output.m4a",
        audio_codec="mp3",
        force_render=True
    )
    
    with patch(
        "os.path.exists", side_effect=lambda path: path in ["input.mp4", "output.m4a"]
    ), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.get_audio_codec",
        return_value="mp3",
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion, patch(
        "os.remove"
    ) as mock_remove:

        # Perform conversion
        result = converter.convert()

        # Assertions
        assert result == "output.m4a"
        mock_remove.assert_called_once_with("output.m4a")
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "output.m4a",
            {"vn": None, "strict": "experimental", "acodec": "mp3"},
        )


def test_convert_codec_not_matching_overwrite_output():
    """
    Test conversion overwrites an existing output file with a different codec.
    """
    converter = AudioConverter(
        input_path="input.mp4",
        output_path="output.m4a",
        audio_codec="mp3",
    )

    with patch(
        "os.path.exists", side_effect=lambda path: path in ["input.mp4", "output.m4a"]
    ), patch(
        "youtube_dl_scraper.converter.audio_converter.AudioConverter.get_audio_codec",
        side_effect=lambda path: "aac" if path == "input.mp4" else "flac",
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion, patch(
        "os.remove"
    ) as mock_remove:

        # Perform conversion
        result = converter.convert()

        # Assertions
        assert result == "output.m4a"
        mock_remove.assert_called_once_with("output.m4a")
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "output.m4a",
            {"vn": None, "strict": "experimental", "acodec": "mp3"},
        )
