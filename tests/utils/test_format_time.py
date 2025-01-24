import pytest
from youtube_dl_scraper.utils.format_time import format_duration, parse_duration


@pytest.mark.parametrize(
    ("seconds", "expected_output"),
    [
        (0, "0s"),
        (30, "30s"),
        (60, "1m 0s"),
        (90, "1m 30s"),
        (3600, "1h 0m 0s"),
        (3665, "1h 1m 5s"),
        (98765, "27h 26m 5s"),
    ],
)
def test_format_duration_with_valid_inputs(seconds, expected_output):
    duration = format_duration(seconds)
    assert duration == expected_output


@pytest.mark.parametrize(
    ("seconds",), [("",), ("30",), ("abcd",), ([30, 20],), ({"30": 30}), (None,)]
)
def test_format_duration_with_invalid_inputs(seconds):
    with pytest.raises(TypeError):
        format_duration(seconds)


@pytest.mark.parametrize(
    ("duration", "expected_output"),
    [
        ("01:02:03", "1 hour, 2 minutes, 3 seconds"),
        ("10:00:00", "10 hours"),
        ("99:59:59", "99 hours, 59 minutes, 59 seconds"),
        ("00:59:59", "59 minutes, 59 seconds"),
        ("00:45:30", "45 minutes, 30 seconds"),
        ("15:45", "15 minutes, 45 seconds"),
        ("00:30:00", "30 minutes"),
        ("00:00:30", "30 seconds"),
        ("01:00", "1 minute"),
        ("00:01", "1 second"),
    ],
)
def test_parse_duration_with_valid_inputs(duration, expected_output):
    fduration = parse_duration(duration)
    assert fduration == expected_output


@pytest.mark.parametrize(
    ("duration", "expected_output"),
    [
        ("00:00:00", ""),
        ("0:0:0", ""),
        ("00:00", ""),
        ("0:0", ""),
        ("01:00:00", "1 hour"),
        ("00:01:01", "1 minute, 1 second"),
        ("00:00:01", "1 second"),
        ("1:0:0", "1 hour"),
    ],
)
def test_parse_duration_edge_cases(duration, expected_output):
    fduration = parse_duration(duration)
    assert fduration == expected_output


@pytest.mark.parametrize(
    ("duration", "raised_error"),
    [
        ("abc:def:ghi", ValueError),
        ("12", ValueError),
        ("1:2:3:4", ValueError),
        ("01:02:", ValueError),
        (":01:02", ValueError),
        ("", ValueError),
        (None, TypeError),
        ([1, 2, 3], TypeError),
    ],
)
def test_parse_duration_invalid_inputs_raises_error(duration, raised_error):
    with pytest.raises(raised_error):
        parse_duration(duration)


@pytest.mark.parametrize(
    ("duration", "expected_output"),
    [
        (" 01:30:30", "1 hour, 30 minutes, 30 seconds"),
        (" 01:30", "1 minute, 30 seconds"),
        ("  01:30:30", "1 hour, 30 minutes, 30 seconds"),
        ("  01:30", "1 minute, 30 seconds"),
    ],
)
def test_parse_duration_leading_spaces(duration, expected_output):
    fduration = parse_duration(duration)
    assert fduration == expected_output


@pytest.mark.parametrize(
    ("duration", "expected_output"),
    [
        ("01:30:30 ", "1 hour, 30 minutes, 30 seconds"),
        ("01:30 ", "1 minute, 30 seconds"),
        ("01:30:30  ", "1 hour, 30 minutes, 30 seconds"),
        ("01:30  ", "1 minute, 30 seconds"),
    ],
)
def test_parse_duration_trailing_spaces(duration, expected_output):
    fduration = parse_duration(duration)
    assert fduration == expected_output


@pytest.mark.parametrize(
    ("duration", "expected_output"),
    [
        (" 01:30:30 ", "1 hour, 30 minutes, 30 seconds"),
        (" 01:30 ", "1 minute, 30 seconds"),
        ("  01:30:30  ", "1 hour, 30 minutes, 30 seconds"),
        ("  01:30  ", "1 minute, 30 seconds"),
    ],
)
def test_parse_duration_leading_and_trailing_spaces(duration, expected_output):
    fduration = parse_duration(duration)
    assert fduration == expected_output
