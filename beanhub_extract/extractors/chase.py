import csv
import datetime
import decimal
import hashlib
import os
import typing

from ..data_types import Fingerprint
from ..data_types import Transaction
from .base import ExtractorBase


def parse_date(date_str: str) -> datetime.date:
    parts = date_str.split("/")
    return datetime.date(int(parts[-1]), *(map(int, parts[:-1])))


class ChaseCreditCardExtractor(ExtractorBase):
    EXTRACTOR_NAME = "chase_credit_card"
    DEFAULT_IMPORT_ID = "{{ file | as_posix_path }}:{{ reversed_lineno }}"
    ALL_FIELDS = [
        "Transaction Date",
        "Post Date",
        "Description",
        "Category",
        "Type",
        "Amount",
        "Memo",
    ]

    def detect(self) -> bool:
        reader = csv.DictReader(self.input_file)
        try:
            return reader.fieldnames == self.ALL_FIELDS
        except Exception:
            return False

    def fingerprint(self) -> Fingerprint | None:
        reader = csv.DictReader(self.input_file)
        row = None
        for row in reader:
            pass
        if row is None:
            return
        hash = hashlib.sha256()
        for field in reader.fieldnames:
            hash.update(row[field].encode("utf8"))
        return Fingerprint(
            starting_date=parse_date(row["Transaction Date"]),
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
            kwargs = dict(
                date=parse_date(row.pop("Transaction Date")),
                post_date=parse_date(row.pop("Post Date")),
                desc=row.pop("Description"),
                category=row.pop("Category"),
                type=row.pop("Type"),
                amount=decimal.Decimal(row.pop("Amount")),
                note=row.pop("Memo"),
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
