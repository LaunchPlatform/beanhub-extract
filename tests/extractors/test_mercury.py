import datetime
import decimal
import pathlib

import pytest
import pytz

from beanhub_extract.data_types import Transaction
from beanhub_extract.extractors.mercury import MercuryExtractor
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


@pytest.mark.parametrize(
    "input_file, expected",
    [
        (
            "mercury.csv",
            [
                Transaction(
                    extractor="mercury",
                    file="mercury.csv",
                    lineno=1,
                    date=datetime.date(2024, 4, 17),
                    timestamp=datetime.datetime(
                        2024, 4, 18, 4, 30, 40, tzinfo=pytz.UTC
                    ),
                    timezone="UTC",
                    desc="GUSTO",
                    bank_desc="GUSTO; FEE 111111; Launch Platform LLC",
                    amount=decimal.Decimal("-46.00"),
                    category="",
                    status="Sent",
                    source_account="Mercury Checking xx12",
                    note="",
                    reference="",
                    currency="",
                ),
                Transaction(
                    extractor="mercury",
                    file="mercury.csv",
                    lineno=2,
                    date=datetime.date(2024, 4, 16),
                    timestamp=datetime.datetime(
                        2024, 4, 16, 10, 25, 55, tzinfo=pytz.UTC
                    ),
                    timezone="UTC",
                    desc="Amazon Web Services",
                    bank_desc="Amazon web services",
                    amount=decimal.Decimal("-353.63"),
                    category="Software",
                    status="Sent",
                    source_account="Mercury Credit",
                    note="",
                    reference="",
                    currency="USD",
                ),
                Transaction(
                    extractor="mercury",
                    file="mercury.csv",
                    lineno=3,
                    date=datetime.date(2024, 4, 16),
                    timestamp=datetime.datetime(
                        2024, 4, 16, 10, 24, 57, tzinfo=pytz.UTC
                    ),
                    timezone="UTC",
                    desc="Adobe",
                    bank_desc="ADOBE  *ADOBE",
                    amount=decimal.Decimal("-54.99"),
                    category="Software",
                    status="Sent",
                    source_account="Mercury Credit",
                    note="",
                    reference="",
                    currency="USD",
                ),
                Transaction(
                    extractor="mercury",
                    file="mercury.csv",
                    lineno=4,
                    date=datetime.date(2024, 4, 15),
                    timestamp=datetime.datetime(
                        2024, 4, 15, 21, 35, 37, tzinfo=pytz.UTC
                    ),
                    timezone="UTC",
                    desc="Jane Doe",
                    bank_desc="Send Money transaction initiated on Mercury",
                    amount=decimal.Decimal("-1500.00"),
                    category="",
                    status="Sent",
                    source_account="Mercury Checking xx1234",
                    note="",
                    reference="Profit distribution",
                    currency="",
                ),
            ],
        ),
    ],
)
def test_extractor(
    fixtures_folder: pathlib.Path, input_file: str, expected: list[Transaction]
):
    with open(fixtures_folder / input_file, "rt") as fo:
        extractor = MercuryExtractor(fo)
        assert list(extractor()) == expected
