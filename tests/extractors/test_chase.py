import datetime
import decimal
import functools
import pathlib

import pytest

from beanhub_extract.data_types import Fingerprint
from beanhub_extract.data_types import Transaction
from beanhub_extract.extractors.chase import ChaseCreditCardExtractor
from beanhub_extract.extractors.chase import parse_date
from beanhub_extract.utils import strip_txn_base_path


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("05/04/2024", datetime.date(2024, 5, 4)),
    ],
)
def test_parse_date(date_str: str, expected: datetime.date):
    assert parse_date(date_str) == expected


@pytest.mark.parametrize(
    "input_file, expected",
    [
        (
            "chase_credit_card.csv",
            [
                Transaction(
                    extractor="chase_credit_card",
                    file="chase_credit_card.csv",
                    lineno=1,
                    reversed_lineno=-5,
                    date=datetime.date(2024, 4, 9),
                    post_date=datetime.date(2024, 4, 9),
                    desc="AUTOMATIC PAYMENT - THANK",
                    amount=decimal.Decimal("123.45"),
                    category="",
                    type="Payment",
                    note="",
                ),
                Transaction(
                    extractor="chase_credit_card",
                    file="chase_credit_card.csv",
                    lineno=2,
                    reversed_lineno=-4,
                    date=datetime.date(2024, 4, 3),
                    post_date=datetime.date(2024, 4, 5),
                    desc="APPLE.COM/BILL",
                    amount=decimal.Decimal("-1.23"),
                    category="Shopping",
                    type="Sale",
                    note="",
                ),
                Transaction(
                    extractor="chase_credit_card",
                    file="chase_credit_card.csv",
                    lineno=3,
                    reversed_lineno=-3,
                    date=datetime.date(2024, 4, 2),
                    post_date=datetime.date(2024, 4, 3),
                    desc="COSTCO WHSE #01234",
                    amount=decimal.Decimal("-4.56"),
                    category="Shopping",
                    type="Sale",
                    note="",
                ),
                Transaction(
                    extractor="chase_credit_card",
                    file="chase_credit_card.csv",
                    lineno=4,
                    reversed_lineno=-2,
                    date=datetime.date(2024, 4, 2),
                    post_date=datetime.date(2024, 4, 3),
                    desc="Amazon web services",
                    amount=decimal.Decimal("-6.54"),
                    category="Personal",
                    type="Sale",
                    note="",
                ),
                Transaction(
                    extractor="chase_credit_card",
                    file="chase_credit_card.csv",
                    lineno=5,
                    reversed_lineno=-1,
                    date=datetime.date(2024, 4, 1),
                    post_date=datetime.date(2024, 4, 2),
                    desc="GITHUB  INC.",
                    amount=decimal.Decimal("-4.00"),
                    category="Professional Services",
                    type="Sale",
                    note="",
                ),
            ],
        ),
    ],
)
def test_credit_card_extractor(
    fixtures_folder: pathlib.Path, input_file: str, expected: list[Transaction]
):
    with open(fixtures_folder / input_file, "rt") as fo:
        extractor = ChaseCreditCardExtractor(fo)
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
        ("chase_credit_card.csv", True),
        ("mercury.csv", False),
        ("empty.csv", False),
        ("other.csv", False),
        (pytest.lazy_fixture("zip_file"), False),
    ],
)
def test_credit_card_detect(
    fixtures_folder: pathlib.Path, input_file: str, expected: bool
):
    with open(fixtures_folder / input_file, "rt") as fo:
        extractor = ChaseCreditCardExtractor(fo)
        assert extractor.detect() == expected


def test_credit_card_fingerprint(fixtures_folder: pathlib.Path):
    with open(fixtures_folder / "chase_credit_card.csv", "rt") as fo:
        extractor = ChaseCreditCardExtractor(fo)
        assert extractor.fingerprint() == Fingerprint(
            starting_date=datetime.date(2024, 4, 1),
            first_row_hash="f68f953ef2d7c7a088924728b8b6b573120fcb384ff3fbd4ca382335a336acc3",
        )
