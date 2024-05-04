import datetime

import pytest

from beanhub_extract.extractors.mercury import parse_date
from beanhub_extract.extractors.mercury import parse_datetime
from beanhub_extract.extractors.mercury import parse_time


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("05-04-2024", datetime.date(2024, 5, 4)),
    ],
)
def test_parse_date(date_str: str, expected: datetime.date):
    assert parse_date(date_str) == expected


@pytest.mark.parametrize(
    "time_str, expected",
    [
        ("14:35:37", datetime.time(14, 35, 37)),
    ],
)
def test_parse_time(time_str: str, expected: datetime.time):
    assert parse_time(time_str) == expected


@pytest.mark.parametrize(
    "datetime_str, expected",
    [
        ("05-04-2024 14:35:37", datetime.datetime(2024, 5, 4, 14, 35, 37)),
    ],
)
def test_parse_datetime(datetime_str: str, expected: datetime.datetime):
    assert parse_datetime(datetime_str) == expected
