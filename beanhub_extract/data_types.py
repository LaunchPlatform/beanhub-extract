import enum


@enum.unique
class AttributeType(enum.Enum):
    file = "file"
    lineno = "lineno"
    date = "date"
    post_date = "post_date"
    timestamp = "timestamp"
    desc = "desc"
    amount = "amount"
    currency = "currency"
    category = "category"
    status = "status"
    type = "type"
    source_account = "source_account"
    dest_account = "dest_account"
    note = "note"
    reference = "reference"
    payee = "payee"
