import csv
import datetime
import decimal
import hashlib
import os
import typing

import iso8601

from ..data_types import Fingerprint
from ..data_types import Transaction
from .base import ExtractorBase


SIMPLE_VALUE_FIELDS = [
    "date",
    "name",
    "amount",
    "pending",
    "website",
    "datetime",
    "logo_url",
    "account_id",
    "category_id",
    "check_number",
    "account_owner",
    "merchant_name",
    "transaction_id",
    "authorized_date",
    "payment_channel",
    "transaction_code",
    "transaction_type",
    "iso_currency_code",
    "merchant_entity_id",
    "authorized_datetime",
    "pending_transaction_id",
    "unofficial_currency_code",
    "personal_finance_category_icon_url",
]
COUNTER_PARTIES_PREFIX = "counterparties__"
COUNTER_PARTIES_FIELDS = [
    "name",
    "type",
    "website",
    "logo_url",
    "entity_id",
    "phone_number",
    "confidence_level",
]
PERSONAL_FINANCE_CATEGORY_PREFIX = "personal_finance_category__"
PERSONAL_FINANCE_CATEGORY_FIELDS = ["primary", "detailed", "confidence_level"]
ALL_FIELDS = (
    SIMPLE_VALUE_FIELDS
    + list(map(lambda x: COUNTER_PARTIES_PREFIX + x, COUNTER_PARTIES_FIELDS))
    + list(
        map(
            lambda x: PERSONAL_FINANCE_CATEGORY_PREFIX + x,
            PERSONAL_FINANCE_CATEGORY_FIELDS,
        )
    )
)


def parse_date(date_str: str) -> datetime.date:
    parts = date_str.split("-")
    return datetime.date(*(map(int, parts)))


class PlaidExtractor(ExtractorBase):
    EXTRACTOR_NAME = "plaid"
    DEFAULT_IMPORT_ID = "{{ transaction_id }}"

    def detect(self) -> bool:
        reader = csv.DictReader(self.input_file)
        try:
            return reader.fieldnames == ALL_FIELDS
        except Exception:
            return False

    def fingerprint(self) -> Fingerprint | None:
        reader = csv.DictReader(self.input_file)
        try:
            row = next(reader)
        except StopIteration:
            return
        hash = hashlib.sha256()
        for field in reader.fieldnames:
            hash.update(row[field].encode("utf8"))

        raw_authorized_date = row.pop("authorized_date")
        raw_date_value = row.pop("date")
        if raw_authorized_date.strip():
            date_value = raw_authorized_date
        else:
            date_value = raw_date_value
        return Fingerprint(
            starting_date=parse_date(date_value),
            first_row_hash=hash.hexdigest(),
        )

    def __call__(self) -> typing.Generator[Transaction, None, None]:
        filename = None
        if hasattr(self.input_file, "name"):
            filename = self.input_file.name
        row_count_reader = csv.DictReader(self.input_file)
        row_count = 0
        for _ in row_count_reader:
            row_count += 1
        self.input_file.seek(os.SEEK_SET, 0)
        reader = csv.DictReader(self.input_file)
        for i, row in enumerate(reader):
            pending = row.pop("pending").lower() == "true"
            if pending:
                date = parse_date(row.pop("date"))
                post_date = None
            else:
                raw_authorized_date = row.pop("authorized_date")
                date_value = parse_date(row.pop("date"))
                post_date = date_value
                if not raw_authorized_date.strip():
                    # in some strange situation, authorized_date could be empty, such as sandbox mode plaid credit card,
                    # not sure if this could also happen in production. but regardless, if it's the case, let's just
                    # use the date value as date and post date in the same time
                    date = date_value
                else:
                    date = parse_date(raw_authorized_date)

            dt = row.pop("datetime")
            if not dt:
                timestamp = None
            else:
                timestamp = iso8601.parse_date(dt)

            txn_id = row.pop("transaction_id")
            # For some banks, such as AMEX credit cards, when a pending transaction posted, the old one will
            # be deleted and a new one with the pending transaction id for the old one will be added.
            # To avoid txn id change after it gets posted, we should always use pending txn id first if available
            pending_transaction_id = row.pop("pending_transaction_id")
            if pending_transaction_id.strip():
                txn_id = pending_transaction_id
            kwargs = dict(
                transaction_id=txn_id,
                date=date,
                post_date=post_date,
                status="pending" if pending else "posted",
                pending=pending,
                desc=row.pop("name"),
                payee=row.pop("merchant_name"),
                source_account=row.pop("account_id"),
                amount=decimal.Decimal(row.pop("amount")),
                type=row.pop("payment_channel"),
                currency=row.pop("iso_currency_code"),
                category=row.pop("personal_finance_category__primary"),
                subcategory=row.pop("personal_finance_category__detailed"),
                timestamp=timestamp,
            )
            if row:
                kwargs["extra"] = row

            yield Transaction(
                extractor=self.EXTRACTOR_NAME,
                file=filename,
                lineno=i + 1,
                reversed_lineno=i - row_count,
                **kwargs
            )
