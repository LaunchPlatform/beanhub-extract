import enum


@enum.unique
class AttributeType(enum.Enum):
    # the filename of import source
    file = "file"
    # the entry line number of the source file
    lineno = "lineno"
    # date of the transaction
    date = "date"
    # date when the transaction posted
    post_date = "post_date"
    # timestamp of the transaction
    timestamp = "timestamp"
    # description of the transaction
    desc = "desc"
    # transaction amount
    amount = "amount"
    # ISO 4217 currency symbol
    currency = "currency"
    # category of the transaction, like Entertainment, Shopping, etc..
    category = "category"
    # status of the transaction
    status = "status"
    # type of the transaction, such as Sale, Return, Debit, etc
    type = "type"
    # Source account of the transaction
    source_account = "source_account"
    # destination account of the transaction
    dest_account = "dest_account"
    # note or memo for the transaction
    note = "note"
    # Reference value
    reference = "reference"
    # Payee of the transaction
    payee = "payee"
