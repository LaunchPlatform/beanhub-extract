import csv
import datetime
import decimal
import hashlib
import os
import typing

import pytz

from ..data_types import Fingerprint
from ..data_types import Transaction
from .base import ExtractorBase


def parse_date(date_str: str) -> datetime.date:
    parts = date_str.split("-")
    return datetime.date(int(parts[-1]), *(map(int, parts[:-1])))


def parse_time(time_str: str) -> datetime.time:
    parts = time_str.split(":")
    return datetime.time(*(map(int, parts)))


def parse_datetime(timestamp_str: str) -> datetime.datetime:
    parts = timestamp_str.split(" ")
    date = parse_date(parts[0])
    time = parse_time(parts[1])
    return datetime.datetime.combine(date, time)


class MercuryExtractor(ExtractorBase):
    EXTRACTOR_NAME = "mercury"
    DEFAULT_IMPORT_ID = "{{ file | as_posix_path }}:{{ reversed_lineno }}"
    ALL_FIELDS = [
        "Date (UTC)",
        "Description",
        "Amount",
        "Status",
        "Source Account",
        "Bank Description",
        "Reference",
        "Note",
        "Last Four Digits",
        "Name On Card",
        "Category",
        "GL Code",
        "Timestamp",
        "Original Currency",
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
            starting_date=parse_date(row["Date (UTC)"]),
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
        timezone = pytz.UTC
        for i, row in enumerate(reader):
            kwargs = dict(
                date=parse_date(row.pop("Date (UTC)")),
                desc=row.pop("Description"),
                amount=decimal.Decimal(row.pop("Amount")),
                status=row.pop("Status"),
                source_account=row.pop("Source Account"),
                bank_desc=row.pop("Bank Description"),
                reference=row.pop("Reference"),
                note=row.pop("Note"),
                category=row.pop("Category"),
                currency=row.pop("Original Currency"),
                name_on_card=row.pop("Name On Card"),
                last_four_digits=row.pop("Last Four Digits"),
                gl_code=row.pop("GL Code"),
                timestamp=timezone.localize(parse_datetime(row.pop("Timestamp"))),
            )
            if row:
                kwargs["extra"] = row

            yield Transaction(
                extractor=self.EXTRACTOR_NAME,
                file=filename,
                lineno=i + 1,
                reversed_lineno=i - row_count,
                timezone="UTC",
                **kwargs
            )
