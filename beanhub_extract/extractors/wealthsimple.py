import csv
import datetime
import decimal
import hashlib
import typing

from ..data_types import Fingerprint
from ..data_types import Transaction
from .base import ExtractorBase


def parse_date(date_str: str) -> datetime.date:
    parts = date_str.split("-")
    return datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))


class WealthsimpleExtractor(ExtractorBase):
    EXTRACTOR_NAME = "wealthsimple"
    DEFAULT_IMPORT_ID = "{{ file | as_posix_path }}:{{ reversed_lineno }}"
    ALL_FIELDS = [
        "date",
        "transaction",
        "description",
        "amount",
        "balance",
    ]

    def detect(self) -> bool:
        reader = csv.DictReader(self.input_file)
        try:
            return reader.fieldnames == self.ALL_FIELDS
        except Exception:
            return False

    def fingerprint(self) -> Fingerprint | None:
        self.input_file.seek(0)
        reader = csv.DictReader(self.input_file)
        try:
            row = next(reader)
        except StopIteration:
            return None
        
        hash = hashlib.sha256()
        for field in reader.fieldnames:
            hash.update(row[field].encode("utf8"))
        
        return Fingerprint(
            starting_date=parse_date(row["date"]),
            first_row_hash=hash.hexdigest(),
        )

    def __call__(self) -> typing.Generator[Transaction, None, None]:
        self.input_file.seek(0)
        reader = csv.DictReader(self.input_file)
        rows = list(reader)
        row_count = len(rows)
        
        filename = getattr(self.input_file, "name", None)
        
        for i, row in enumerate(rows):
            date_str = row["date"]
            date = parse_date(date_str)
            transaction_type = row["transaction"]
            amount = decimal.Decimal(row["amount"])
            
            kwargs = dict(
                date=date,
                desc=row["description"],
                amount=amount,
                type=transaction_type,
                extra={
                    "balance": decimal.Decimal(row["balance"])
                }
            )
            
            yield Transaction(
                extractor=self.EXTRACTOR_NAME,
                file=filename,
                lineno=i + 1,
                reversed_lineno=i - row_count,
                **kwargs
            )
