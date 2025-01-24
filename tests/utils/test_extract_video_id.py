import pytest
from youtube_dl_scraper.utils import extract_video_id


def test_extract_video_id_standard_youtube_url_with_video_id():
    url = "https://www.youtube.com/watch?v=abc123"
    assert extract_video_id(url) == "abc123"


def test_extract_video_id_standard_youtube_url_without_video_id():
    url = "https://www.youtube.com/watch?v="
    assert extract_video_id(url) == ""


def test_extract_video_id_youtube_shorts_url_with_video_id():
    url = "https://www.youtube.com/shorts/abc123"
    assert extract_video_id(url) == "abc123"


def test_extract_video_id_youtube_embed_url_with_video_id():
    url = "https://www.youtube.com/embed/abc123"
    assert extract_video_id(url) == "abc123"


def test_extract_video_id_youtube_shortened_url_with_video_id():
    url = "https://youtu.be/abc123"
    assert extract_video_id(url) == "abc123"


def test_extract_video_id_youtube_shortened_url_without_video_id():
    url = "https://youtu.be/"
    assert extract_video_id(url) == ""


def test_extract_video_id_standard_youtube_url_without_v_parameter():
    url = "https://www.youtube.com/watch"
    assert extract_video_id(url) == ""


def test_extract_video_id_unsupported_url():
    url = "https://www.example.com"
    with pytest.raises(ValueError, match="Unsupported URL: https://www.example.com"):
        extract_video_id(url)


def test_extract_video_id_non_youtube_domain():
    url = "https://vimeo.com/12345"
    with pytest.raises(ValueError, match="Unsupported URL: https://vimeo.com/12345"):
        extract_video_id(url)


def test_extract_video_id_youtube_url_with_query_params_but_no_v():
    url = "https://www.youtube.com/watch?feature=share"
    assert extract_video_id(url) == ""
