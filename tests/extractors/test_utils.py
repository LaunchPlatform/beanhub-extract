import datetime

import pytest

from beanhub_extract.utils import parse_date


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-05-04", datetime.date(2024, 5, 4)),
    ],
)
def test_parse_date(date_str: str, expected: datetime.date):
    assert parse_date(date_str) == expected
