import csv
import datetime
import decimal
import hashlib
import os
import typing
from dataclasses import fields

from ..data_types import Fingerprint
from ..data_types import Transaction
from ..utils import parse_date
from .base import ExtractorBase

EXCLUDED_FIELDS = frozenset(["extractor", "file", "lineno", "reversed_lineno", "extra"])
ALL_FIELDS = frozenset(field.name for field in fields(Transaction)) - EXCLUDED_FIELDS


class CSVExtractor(ExtractorBase):
    EXTRACTOR_NAME = "csv"
    DEFAULT_IMPORT_ID = "{{ file | as_posix_path }}:{{ lineno }}"

    def detect(self) -> bool:
        reader = csv.DictReader(self.input_file)
        try:
            return frozenset(reader.fieldnames).issuperset(ALL_FIELDS)
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

        date = row.pop("date")
        post_date = row.pop("post_date")
        if date.strip():
            date_value = date
        else:
            date_value = post_date
        if not date_value:
            date_value = datetime.date(1970, 1, 1)
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
            kwargs = {}
            for field in fields(Transaction):
                if field.name not in row:
                    continue
                value = row.pop(field.name)
                field_type, _ = typing.get_args(field.type)
                if value is not None and value.strip():
                    if field_type is datetime.date:
                        value = parse_date(value)
                    elif field_type is datetime.datetime:
                        value = datetime.datetime.fromisoformat(value)
                    elif field_type is decimal.Decimal:
                        value = decimal.Decimal(value)
                    elif field_type is bool:
                        value = value.lower() == "true"
                    kwargs[field.name] = value
            if row:
                kwargs["extra"] = row

            yield Transaction(
                extractor=self.EXTRACTOR_NAME,
                file=filename,
                lineno=i + 1,
                reversed_lineno=i - row_count,
                **kwargs,
            )
