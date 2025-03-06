import datetime
import decimal
import functools
import pathlib

import pytest

from beanhub_extract.data_types import Fingerprint
from beanhub_extract.data_types import Transaction
from beanhub_extract.extractors.wealthsimple import WealthsimpleExtractor
from beanhub_extract.extractors.wealthsimple import parse_date
from beanhub_extract.utils import strip_txn_base_path


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-04-01", datetime.date(2024, 4, 1)),
    ],
)
def test_parse_date(date_str: str, expected: datetime.date):
    assert parse_date(date_str) == expected


@pytest.mark.parametrize(
    "input_file, expected",
    [
        (
            "wealthsimple.csv",
            [
                Transaction(
                    extractor="wealthsimple",
                    file="wealthsimple.csv",
                    lineno=1,
                    reversed_lineno=-5,
                    date=datetime.date(2024, 4, 1),
                    desc="Interest earned",
                    amount=decimal.Decimal("12.34"),
                    type="INT",
                    extra={"balance": decimal.Decimal("5123.45")},
                ),
                Transaction(
                    extractor="wealthsimple",
                    file="wealthsimple.csv",
                    lineno=2,
                    reversed_lineno=-4,
                    date=datetime.date(2024, 4, 2),
                    desc="Coffee Shop",
                    amount=decimal.Decimal("-4.56"),
                    type="SPEND",
                    extra={"balance": decimal.Decimal("5118.89")},
                ),
                Transaction(
                    extractor="wealthsimple",
                    file="wealthsimple.csv",
                    lineno=3,
                    reversed_lineno=-3,
                    date=datetime.date(2024, 4, 3),
                    desc="Cash back reward",
                    amount=decimal.Decimal("1.23"),
                    type="CASHBACK",
                    extra={"balance": decimal.Decimal("5120.12")},
                ),
                Transaction(
                    extractor="wealthsimple",
                    file="wealthsimple.csv",
                    lineno=4,
                    reversed_lineno=-2,
                    date=datetime.date(2024, 4, 4),
                    desc="Grocery Store",
                    amount=decimal.Decimal("-45.67"),
                    type="SPEND",
                    extra={"balance": decimal.Decimal("5074.45")},
                ),
                Transaction(
                    extractor="wealthsimple",
                    file="wealthsimple.csv",
                    lineno=5,
                    reversed_lineno=-1,
                    date=datetime.date(2024, 4, 15),
                    desc="Direct deposit",
                    amount=decimal.Decimal("1234.56"),
                    type="AFT_IN",
                    extra={"balance": decimal.Decimal("6309.01")},
                ),
            ],
        ),
    ],
)

def test_wealthsimple_extractor(
    fixtures_folder: pathlib.Path, input_file: str, expected: list[Transaction]
):
    with open(fixtures_folder / input_file, "rt", encoding="utf-8") as fo:
        extractor = WealthsimpleExtractor(fo)
        assert (
            list(
                map(
                    functools.partial(strip_txn_base_path, fixtures_folder), extractor()
                )
            )
            == expected
        )


@pytest.mark.parametrize(
    "input_file, expected",
    [
        ("wealthsimple.csv", True),
        ("mercury.csv", False),
        ("empty.csv", False),
        ("other.csv", False),
        (pytest.lazy_fixture("zip_file"), False),
    ],
)
def test_wealthsimple_detect(
    fixtures_folder: pathlib.Path, input_file: str, expected: bool
):
    with open(fixtures_folder / input_file, "rt", encoding="utf-8") as fo:
        extractor = WealthsimpleExtractor(fo)
        assert extractor.detect() == expected


def test_wealthsimple_fingerprint(fixtures_folder: pathlib.Path):
    with open(fixtures_folder / "wealthsimple.csv", "rt", encoding="utf-8") as fo:
        extractor = WealthsimpleExtractor(fo)
        assert extractor.fingerprint() == Fingerprint(
            starting_date=datetime.date(2024, 4, 1),
            first_row_hash="f9d844138962e483beecd7f44ada98f0995810e4b1e3fc6d3b27d1b6189318b6",
        )
