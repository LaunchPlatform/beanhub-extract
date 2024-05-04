import typing

from ..data_types import Transaction


class MercuryExtractor:
    def __call__(self, *args, **kwargs) -> typing.Sequence[Transaction]:
        pass
