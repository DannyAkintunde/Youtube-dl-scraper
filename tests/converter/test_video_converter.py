import pytest
from unittest.mock import patch
from youtube_dl_scraper.converter.video_converter import VideoConverter


@pytest.fixture
def get_codecs_return_value():
    return {"video": "h264", "audio": "aac"}


def test_convert_successful_conversion(get_codecs_return_value):
    """
    Test successful audio conversion with re-encoding.
    """
    converter = VideoConverter(
        input_path="input.mp4",
        output_path="output.mp4",
        video_codec="av1",
        audio_codec="aac",
        force_render=True,
    )

    with patch(
        "os.path.exists", side_effect=(lambda path: path in ["input.mp4", "output.mp4"])
    ), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.delete_existing_output_file",
        return_value=True,
    ), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.get_codecs",
        return_value=get_codecs_return_value,
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion:

        result = converter.convert()
        assert result == "output.mp4"
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "output.mp4",
            {"strict": "experimental", "vcodec": "av1", "acodec": "aac"},
        )


def test_convert_defualt_output_path_successful_conversion(get_codecs_return_value):
    """
    Test successful video conversion with re-encoding and auto generated output path.
    """
    converter = VideoConverter(
        input_path="input.mp4",
        output_path=".",
        video_codec="av1",
        audio_codec="aac",
        force_render=True,
    )

    with patch(
        "os.path.exists",
        side_effect=(lambda path: path in ["input.mp4", "input-converted.mp4"]),
    ), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.delete_existing_output_file",
        return_value=True,
    ), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.get_codecs",
        return_value=get_codecs_return_value,
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion:

        result = converter.convert()
        assert result == "input-converted.mp4"
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "input-converted.mp4",
            {"strict": "experimental", "vcodec": "av1", "acodec": "aac"},
        )


def test_convert_without_force_rerender_convertion_successful_output(
    get_codecs_return_value,
):
    """
    Test successful video conversion without re-encoding and auto generated output path.
    """
    converter = VideoConverter(
        input_path="input.mp4",
        output_path="output.mp4",
        video_codec="h264",
        audio_codec="aac",
        force_render=False,
    )

    with patch(
        "os.path.exists", side_effect=(lambda path: path in ["input.mp4", "output.mp4"])
    ), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.delete_existing_output_file",
        return_value=True,
    ), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.get_codecs",
        return_value=get_codecs_return_value,
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion:

        result = converter.convert()
        assert result == "output.mp4"
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "output.mp4",
            {
                "strict": "experimental",
                "codec": "copy",
            },
        )


def test_convert_with_force_rerender_convertion_successful_output(
    get_codecs_return_value,
):
    """
    Test successful video conversion with re-encoding and auto generated output path.
    """
    converter = VideoConverter(
        input_path="input.mp4",
        output_path="output.mp4",
        video_codec="h264",
        audio_codec="aac",
        force_render=True,
    )

    with patch(
        "os.path.exists", side_effect=(lambda path: path in ["input.mp4", "output.mp4"])
    ), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.delete_existing_output_file",
        return_value=True,
    ), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.get_codecs",
        return_value=get_codecs_return_value,
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion:

        result = converter.convert()
        assert result == "output.mp4"
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "output.mp4",
            {"strict": "experimental", "vcodec": "h264", "acodec": "aac"},
        )


def test_convert_input_file_not_found():
    """
    Test conversion fails when the input file does not exist.
    """
    converter = VideoConverter(
        input_path="missing.mp4",
        output_path="output.mp4",
        video_codec="av1",
        audio_codec="aac",
    )

    with patch("os.path.exists", side_effect=(lambda path: path != "missing.mp4")):
        with pytest.raises(
            FileNotFoundError, match="Input file 'missing.mp4' not found."
        ):
            converter.convert()

def test_convert_output_file_not_found(get_codecs_return_value):
    """
    Test conversion fails when the output file does not exist.
    """
    converter = VideoConverter(
        input_path="input.mp4",
        output_path="missing.mp4",
        video_codec="av1",
        audio_codec="aac"
    )
    with patch("os.path.exists", side_effect=lambda path: path == "input.mp4"), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.delete_existing_output_file",
        return_value=True,
    ), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.get_codecs",
        return_value=get_codecs_return_value,
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ):
        with pytest.raises(FileNotFoundError, match="Output file was not created."):
            converter.convert()

def test_convert_matching_codec_without_force_conversion(get_codecs_return_value):
    """
    Test conversion skips rendering when codecs match and force_render is False.
    """
    converter = VideoConverter(
        input_path="input.mp4",
        output_path="output.mp4",
        video_codec="h264",
        audio_codec="aac",
        force_render=False
    )
    with patch("os.path.exists", side_effect=lambda path: path in ["input.mp4", "output.mp4"]), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.get_codecs",
        side_effect=lambda path: path == "output.mp4" and get_codecs_return_value,
    ):
        result = converter.convert()
        
        assert result == "output.mp4"

def test_convert_matching_codec_with_force_conversion_overwites_output(get_codecs_return_value):
    """
    Test conversion skips rendering when codecs match and force_render is True.
    """
    converter = VideoConverter(
        input_path="input.mp4",
        output_path="output.mp4",
        video_codec="h264",
        audio_codec="aac",
        force_render=True
    )
    with patch("os.path.exists", side_effect=lambda path: path in ["input.mp4", "output.mp4"]), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.get_codecs",
        return_value=get_codecs_return_value,
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion, patch(
        "os.remove"
    ) as mock_remove:
        
        result = converter.convert()
        
        assert result == "output.mp4"
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "output.mp4",
            {
                "strict": "experimental",
                "vcodec": "h264",
                "acodec": "aac"
            }
        )
        mock_remove.assert_called_once_with("output.mp4")
        
def test_convert_codec_not_matching_video_codec_overwrite_output(get_codecs_return_value):
    """
    Test conversion overwrites an existing output file with a different codec.
    """
    converter = VideoConverter(
        input_path="input.mp4",
        output_path="output.mp4",
        video_codec="av1",
        audio_codec="aac",
    )
    
    with patch(
        "os.path.exists", side_effect=lambda path: path in ["input.mp4", "output.mp4"]
    ), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.get_codecs",
        return_value=get_codecs_return_value,
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion, patch(
        "os.remove"
    ) as mock_remove:
        result = converter.convert()
        
        assert result == "output.mp4"
        mock_remove.assert_called_once_with("output.mp4")
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "output.mp4",
            {
                "strict": "experimental",
                "vcodec": "av1",
                "acodec": "aac"
            }
        )
        
def test_convert_codec_not_matching_audio_codec_overwrite_output(get_codecs_return_value):
    """
    Test conversion overwrites an existing output file with a different codec.
    """
    converter = VideoConverter(
        input_path="input.mp4",
        output_path="output.mp4",
        video_codec="h264",
        audio_codec="opus",
    )
    
    with patch(
        "os.path.exists", side_effect=lambda path: path in ["input.mp4", "output.mp4"]
    ), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.get_codecs",
        return_value=get_codecs_return_value,
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion, patch(
        "os.remove"
    ) as mock_remove:
        result = converter.convert()
        
        assert result == "output.mp4"
        mock_remove.assert_called_once_with("output.mp4")
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "output.mp4",
            {
                "strict": "experimental",
                "vcodec": "h264",
                "acodec": "opus"
            }
        )
        
def test_convert_codec_not_matching_video_and_audio_codec_overwrite_output(get_codecs_return_value):
    """
    Test conversion overwrites an existing output file with a different codec.
    """
    converter = VideoConverter(
        input_path="input.mp4",
        output_path="output.mp4",
        video_codec="h265",
        audio_codec="opus",
    )
    
    with patch(
        "os.path.exists", side_effect=lambda path: path in ["input.mp4", "output.mp4"]
    ), patch(
        "youtube_dl_scraper.converter.video_converter.VideoConverter.get_codecs",
        return_value=get_codecs_return_value,
    ), patch(
        "youtube_dl_scraper.converter.base_converter.BaseConverter.run_conversion"
    ) as mock_run_conversion, patch(
        "os.remove"
    ) as mock_remove:
        result = converter.convert()
        
        assert result == "output.mp4"
        mock_remove.assert_called_once_with("output.mp4")
        mock_run_conversion.assert_called_once_with(
            "input.mp4",
            "output.mp4",
            {
                "strict": "experimental",
                "vcodec": "h265",
                "acodec": "opus"
            }
        )