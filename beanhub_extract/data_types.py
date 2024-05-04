import enum


@enum.unique
class AttributeType(enum.Enum):
    file = "file"
    lineno = "lineno"
    date = "date"
    desc = "desc"
    amount = "amount"
    currency = "currency"
