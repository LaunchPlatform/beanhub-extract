import csv
import datetime
import decimal
import typing

import pytz

from ..data_types import Transaction


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


class MercuryExtractor:
    EXTRACTOR_NAME = "mercury"

    def __init__(self, input_file: typing.TextIO):
        self.input_file = input_file

    def __call__(self) -> typing.Generator[Transaction, None, None]:
        filename = None
        if hasattr(self.input_file, "name"):
            filename = self.input_file.name
        reader = csv.DictReader(self.input_file)
        timezone = pytz.UTC
        for i, row in enumerate(reader):
            yield Transaction(
                extractor=self.EXTRACTOR_NAME,
                file=filename,
                lineno=i + 1,
                date=parse_date(row["Date (UTC)"]),
                desc=row["Description"],
                amount=decimal.Decimal(row["Amount"]),
                status=row["Status"],
                source_account=row["Source Account"],
                bank_desc=row["Bank Description"],
                reference=row["Reference"],
                note=row["Note"],
                category=row["Category"],
                currency=row["Original Currency"],
                timestamp=parse_datetime(row["Timestamp"]).replace(tzinfo=timezone),
                timezone="UTC",
            )
