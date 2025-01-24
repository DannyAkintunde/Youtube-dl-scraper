import pytest
from youtube_dl_scraper.utils.filename_extractor import get_filename_from_cd


def test_get_filename_from_cd_empty_string():
    assert get_filename_from_cd("") is None


def test_get_filename_from_cd_none_input():
    assert get_filename_from_cd(None) is None


def test_get_filename_from_cd_valid_filename():
    cd = 'attachment; filename="example.txt"'
    assert get_filename_from_cd(cd) == "example.txt"


def test_get_filename_from_cd_filename_with_backslashes():
    cd = 'attachment; filename="path\\to\\example.txt"'
    assert get_filename_from_cd(cd) == "pathtoexample.txt"


def test_get_filename_from_cd_filename_without_quotes():
    cd = "attachment; filename=example.txt"
    assert get_filename_from_cd(cd) == "example.txt"


def test_get_filename_from_cd_no_filename_in_cd():
    cd = "attachment;"
    assert get_filename_from_cd(cd) is None


def test_get_filename_from_cd_filename_with_multiple_spaces():
    cd = 'attachment; filename="example file with spaces.txt"'
    assert get_filename_from_cd(cd) == "example file with spaces.txt"
