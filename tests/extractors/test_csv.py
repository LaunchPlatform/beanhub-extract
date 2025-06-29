import datetime
import decimal
import functools
import pathlib
from pickle import FALSE

import pytest
import pytz

from beanhub_extract.data_types import Fingerprint
from beanhub_extract.data_types import Transaction
from beanhub_extract.extractors.csv import CSVExtractor
from beanhub_extract.extractors.mercury import MercuryExtractor
from beanhub_extract.extractors.mercury import parse_date
from beanhub_extract.extractors.mercury import parse_datetime
from beanhub_extract.extractors.mercury import parse_time
from beanhub_extract.utils import strip_txn_base_path


@pytest.mark.parametrize(
    "input_file, expected",
    [
        (
            "csv.csv",
            [
                Transaction(
                    extractor="csv",
                    file="csv.csv",
                    lineno=1,
                    reversed_lineno=-2,
                    transaction_id="4c5484e6-dad0-4243-8c52-be74d6c84d59",
                    date=datetime.date(2025, 6, 28),
                    post_date=datetime.date(2025, 7, 1),
                    timestamp=datetime.datetime.fromisoformat(
                        "2025-06-29T00:32:53.036910+00:00"
                    ),
                    timezone="America/Los_Angeles",
                    desc="BeanHub subscription",
                    bank_desc="BEANHUB SUB",
                    amount=decimal.Decimal("12.34"),
                    currency="USD",
                    category="Business",
                    subcategory="Software",
                    pending=False,
                    status="Paid",
                    type="Debit",
                    source_account="Mercury",
                    note="",
                    payee="BeanHub",
                    gl_code="5100",
                    name_on_card="Fang-Pen Lin",
                    last_four_digits="1234",
                    extra=None,
                ),
                Transaction(
                    extractor="csv",
                    file="csv.csv",
                    lineno=2,
                    reversed_lineno=-1,
                    transaction_id="39751802-7646-4c24-b9bb-227c9f68a8f2",
                    date=datetime.date(2025, 7, 3),
                    timestamp=datetime.datetime.fromisoformat(
                        "2025-07-03T00:48:51.024820+00:00"
                    ),
                    timezone="America/Los_Angeles",
                    desc="CakeLens subscription",
                    bank_desc="CAKELENS",
                    amount=decimal.Decimal("5.67"),
                    currency="USD",
                    category="Business",
                    subcategory="Software",
                    pending=True,
                    status="Paid",
                    type="Debit",
                    source_account="Mercury",
                    note="AI gen video detection service",
                    payee="BeanHub",
                    gl_code="5100",
                    name_on_card="Fang-Pen Lin",
                    last_four_digits="1234",
                    extra=None,
                ),
            ],
        ),
    ],
)
def test_extractor(
    fixtures_folder: pathlib.Path, input_file: str, expected: list[Transaction]
):
    with open(fixtures_folder / input_file, "rt") as fo:
        extractor = CSVExtractor(fo)
        assert (
            list(
                map(
                    functools.partial(strip_txn_base_path, fixtures_folder), extractor()
                )
            )
            == expected
        )
