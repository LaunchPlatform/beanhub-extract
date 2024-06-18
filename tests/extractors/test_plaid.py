import datetime
import decimal
import functools
import pathlib

import pytest
import pytz

from beanhub_extract.data_types import Fingerprint
from beanhub_extract.data_types import Transaction
from beanhub_extract.extractors.plaid import parse_date
from beanhub_extract.extractors.plaid import PlaidExtractor
from beanhub_extract.utils import strip_txn_base_path


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-05-04", datetime.date(2024, 5, 4)),
    ],
)
def test_parse_date(date_str: str, expected: datetime.date):
    assert parse_date(date_str) == expected


@pytest.mark.parametrize(
    "input_file, expected",
    [
        (
            "plaid.csv",
            [
                Transaction(
                    extractor="plaid",
                    file="plaid.csv",
                    lineno=1,
                    reversed_lineno=-5,
                    transaction_id="R55WBQZRx5h8J8dEKmPbFeda45RL6RCapLk7B",
                    date=datetime.date(2024, 1, 7),
                    post_date=datetime.date(2024, 1, 8),
                    desc="Uber 072515 SF**POOL**",
                    amount=decimal.Decimal("6.33"),
                    currency="USD",
                    category="TRANSPORTATION",
                    subcategory="TRANSPORTATION_TAXIS_AND_RIDE_SHARES",
                    status="posted",
                    type="online",
                    source_account="g554pPNvm5hG9GNgnzDpirvLMz5WaAcENmPM1",
                    payee="Uber",
                    extra={
                        "account_owner": "",
                        "authorized_datetime": "",
                        "category_id": "22016000",
                        "check_number": "",
                        "counterparties__confidence_level": "VERY_HIGH",
                        "counterparties__entity_id": "eyg8o776k0QmNgVpAmaQj4WgzW9Qzo6O51gdd",
                        "counterparties__logo_url": "https://plaid-merchant-logos.plaid.com/uber_1060.png",
                        "counterparties__name": "Uber",
                        "counterparties__phone_number": "",
                        "counterparties__type": "merchant",
                        "counterparties__website": "uber.com",
                        "logo_url": "https://plaid-merchant-logos.plaid.com/uber_1060.png",
                        "merchant_entity_id": "eyg8o776k0QmNgVpAmaQj4WgzW9Qzo6O51gdd",
                        "pending_transaction_id": "",
                        "personal_finance_category__confidence_level": "VERY_HIGH",
                        "personal_finance_category_icon_url": "https://plaid-category-icons.plaid.com/PFC_TRANSPORTATION.png",
                        "transaction_code": "",
                        "transaction_type": "special",
                        "unofficial_currency_code": "",
                        "website": "uber.com",
                    },
                ),
                Transaction(
                    extractor="plaid",
                    file="plaid.csv",
                    lineno=2,
                    reversed_lineno=-4,
                    transaction_id="vPPEBM3p8PiAjAKZ1oRzCVEAwb7BK7iq6Pear",
                    date=datetime.date(2024, 1, 20),
                    post_date=datetime.date(2024, 1, 21),
                    desc="SparkFun",
                    amount=decimal.Decimal("89.4"),
                    currency="USD",
                    category="GENERAL_MERCHANDISE",
                    subcategory="GENERAL_MERCHANDISE_OTHER_GENERAL_MERCHANDISE",
                    status="posted",
                    type="in store",
                    source_account="g554pPNvm5hG9GNgnzDpirvLMz5WaAcENmPM1",
                    payee="FUN",
                    extra={
                        "account_owner": "",
                        "authorized_datetime": "",
                        "category_id": "13005000",
                        "check_number": "",
                        "counterparties__confidence_level": "LOW",
                        "counterparties__entity_id": "",
                        "counterparties__logo_url": "",
                        "counterparties__name": "FUN",
                        "counterparties__phone_number": "",
                        "counterparties__type": "merchant",
                        "counterparties__website": "",
                        "logo_url": "",
                        "merchant_entity_id": "",
                        "pending_transaction_id": "",
                        "personal_finance_category__confidence_level": "LOW",
                        "personal_finance_category_icon_url": "https://plaid-category-icons.plaid.com/PFC_GENERAL_MERCHANDISE.png",
                        "transaction_code": "",
                        "transaction_type": "place",
                        "unofficial_currency_code": "",
                        "website": "",
                    },
                ),
                Transaction(
                    extractor="plaid",
                    file="plaid.csv",
                    lineno=3,
                    reversed_lineno=-3,
                    transaction_id="9AAqkd5G9AfRlRAp731jcGx1pAnM9nH4x3yzA",
                    date=datetime.date(2024, 1, 22),
                    post_date=datetime.date(2024, 1, 22),
                    desc="Starbucks",
                    amount=decimal.Decimal("4.33"),
                    currency="USD",
                    category="FOOD_AND_DRINK",
                    subcategory="FOOD_AND_DRINK_COFFEE",
                    status="posted",
                    type="in store",
                    source_account="g554pPNvm5hG9GNgnzDpirvLMz5WaAcENmPM1",
                    payee="Starbucks",
                    extra={
                        "account_owner": "",
                        "authorized_datetime": "",
                        "category_id": "13005043",
                        "check_number": "",
                        "counterparties__confidence_level": "VERY_HIGH",
                        "counterparties__entity_id": "NZAJQ5wYdo1W1p39X5q5gpb15OMe39pj4pJBb",
                        "counterparties__logo_url": "https://plaid-merchant-logos.plaid.com/starbucks_956.png",
                        "counterparties__name": "Starbucks",
                        "counterparties__phone_number": "",
                        "counterparties__type": "merchant",
                        "counterparties__website": "starbucks.com",
                        "logo_url": "https://plaid-merchant-logos.plaid.com/starbucks_956.png",
                        "merchant_entity_id": "NZAJQ5wYdo1W1p39X5q5gpb15OMe39pj4pJBb",
                        "pending_transaction_id": "",
                        "personal_finance_category__confidence_level": "VERY_HIGH",
                        "personal_finance_category_icon_url": "https://plaid-category-icons.plaid.com/PFC_FOOD_AND_DRINK.png",
                        "transaction_code": "",
                        "transaction_type": "place",
                        "unofficial_currency_code": "",
                        "website": "starbucks.com",
                    },
                ),
                Transaction(
                    extractor="plaid",
                    file="plaid.csv",
                    lineno=4,
                    reversed_lineno=-2,
                    transaction_id="yeeGdMDA8eTWvWBMELzxcgGnVP7m67i46ZnkE",
                    date=datetime.date(2024, 1, 22),
                    post_date=datetime.date(2024, 1, 22),
                    desc="McDonald's",
                    amount=decimal.Decimal("12.0"),
                    currency="USD",
                    category="FOOD_AND_DRINK",
                    subcategory="FOOD_AND_DRINK_FAST_FOOD",
                    status="posted",
                    type="in store",
                    source_account="g554pPNvm5hG9GNgnzDpirvLMz5WaAcENmPM1",
                    payee="McDonald's",
                    extra={
                        "account_owner": "",
                        "authorized_datetime": "",
                        "category_id": "13005032",
                        "check_number": "",
                        "counterparties__confidence_level": "VERY_HIGH",
                        "counterparties__entity_id": "vzWXDWBjB06j5BJoD3Jo84OJZg7JJzmqOZA22",
                        "counterparties__logo_url": "https://plaid-merchant-logos.plaid.com/mcdonalds_619.png",
                        "counterparties__name": "McDonald's",
                        "counterparties__phone_number": "",
                        "counterparties__type": "merchant",
                        "counterparties__website": "mcdonalds.com",
                        "logo_url": "https://plaid-merchant-logos.plaid.com/mcdonalds_619.png",
                        "merchant_entity_id": "vzWXDWBjB06j5BJoD3Jo84OJZg7JJzmqOZA22",
                        "pending_transaction_id": "",
                        "personal_finance_category__confidence_level": "VERY_HIGH",
                        "personal_finance_category_icon_url": "https://plaid-category-icons.plaid.com/PFC_FOOD_AND_DRINK.png",
                        "transaction_code": "",
                        "transaction_type": "place",
                        "unofficial_currency_code": "",
                        "website": "mcdonalds.com",
                    },
                ),
                Transaction(
                    extractor="plaid",
                    file="plaid.csv",
                    lineno=5,
                    reversed_lineno=-1,
                    transaction_id="mkkQJgar8kcVzV63onKQCAkqG6og3oSgylpKq",
                    date=datetime.date(2024, 1, 23),
                    post_date=datetime.date(2024, 1, 23),
                    desc="United Airlines",
                    amount=decimal.Decimal("-500.0"),
                    currency="USD",
                    category="TRAVEL",
                    subcategory="TRAVEL_FLIGHTS",
                    status="posted",
                    type="in store",
                    source_account="g554pPNvm5hG9GNgnzDpirvLMz5WaAcENmPM1",
                    payee="United Airlines",
                    extra={
                        "account_owner": "",
                        "authorized_datetime": "",
                        "category_id": "22001000",
                        "check_number": "",
                        "counterparties__confidence_level": "VERY_HIGH",
                        "counterparties__entity_id": "NKDjqyAdQQzpyeD8qpLnX0D6yvLe2KYKYYzQ4",
                        "counterparties__logo_url": "https://plaid-merchant-logos.plaid.com/united_airlines_1065.png",
                        "counterparties__name": "United Airlines",
                        "counterparties__phone_number": "",
                        "counterparties__type": "merchant",
                        "counterparties__website": "united.com",
                        "logo_url": "https://plaid-merchant-logos.plaid.com/united_airlines_1065.png",
                        "merchant_entity_id": "NKDjqyAdQQzpyeD8qpLnX0D6yvLe2KYKYYzQ4",
                        "pending_transaction_id": "",
                        "personal_finance_category__confidence_level": "VERY_HIGH",
                        "personal_finance_category_icon_url": "https://plaid-category-icons.plaid.com/PFC_TRAVEL.png",
                        "transaction_code": "",
                        "transaction_type": "special",
                        "unofficial_currency_code": "",
                        "website": "united.com",
                    },
                ),
            ],
        ),
    ],
)
def test_extractor(
    fixtures_folder: pathlib.Path, input_file: str, expected: list[Transaction]
):
    with open(fixtures_folder / input_file, "rt") as fo:
        extractor = PlaidExtractor(fo)
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
        ("plaid.csv", True),
        ("mercury.csv", False),
        ("chase_credit_card.csv", False),
        ("empty.csv", False),
        ("other.csv", False),
        (pytest.lazy_fixture("zip_file"), False),
    ],
)
def test_detect(fixtures_folder: pathlib.Path, input_file: str, expected: bool):
    with open(fixtures_folder / input_file, "rt") as fo:
        extractor = PlaidExtractor(fo)
        assert extractor.detect() == expected


def test_fingerprint(fixtures_folder: pathlib.Path):
    with open(fixtures_folder / "plaid.csv", "rt") as fo:
        extractor = PlaidExtractor(fo)
        assert extractor.fingerprint() == Fingerprint(
            starting_date=datetime.date(2024, 1, 7),
            first_row_hash="264b70b31bf27298bef4357774ed2ca09f4a4e64e7e73cfb985b3afff76b5b06",
        )
