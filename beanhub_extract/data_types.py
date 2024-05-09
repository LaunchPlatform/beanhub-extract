import dataclasses
import datetime
import decimal


@dataclasses.dataclass(frozen=True)
class Transaction:
    extractor: str
    # the filename of import source
    file: str | None = None
    # the entry line number of the source file
    lineno: int | None = None
    # the entry line number of the source file in reverse order. comes handy for CSV files in desc datetime order
    reversed_lineno: int | None = None
    # date of the transaction
    date: datetime.date | None = None
    # date when the transaction posted
    post_date: datetime.date | None = None
    # timestamp of the transaction
    timestamp: datetime.datetime | None = None
    # timezone of the transaction, needs to be one of timezone value supported by pytz
    timezone: str | None = None
    # description of the transaction
    desc: str | None = None
    # description of the transaction provided by the bank
    bank_desc: str | None = None
    # transaction amount
    amount: decimal.Decimal | None = None
    # ISO 4217 currency symbol
    currency: str | None = None
    # category of the transaction, like Entertainment, Shopping, etc..
    category: str | None = None
    # status of the transaction
    status: str | None = None
    # type of the transaction, such as Sale, Return, Debit, etc
    type: str | None = None
    # Source account of the transaction
    source_account: str | None = None
    # destination account of the transaction
    dest_account: str | None = None
    # note or memo for the transaction
    note: str | None = None
    # Reference value
    reference: str | None = None
    # Payee of the transaction
    payee: str | None = None
    # General Ledger Code
    gl_code: str | None = None
    # Name on the credit/debit card
    name_on_card: str | None = None
    # Last 4 digits of credit/debit card
    last_four_digits: str | None = None
    # All the columns not handled and put into `Transaction`'s attributes by the extractor goes here
    extra: dict | None = None
