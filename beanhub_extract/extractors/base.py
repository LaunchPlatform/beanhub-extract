import typing

from ..data_types import Fingerprint
from ..data_types import Transaction


class ExtractorBase:
    def __init__(self, input_file: typing.TextIO):
        self.input_file = input_file

    def detect(self) -> bool:
        raise NotImplementedError()

    def fingerprint(self) -> Fingerprint | None:
        raise NotImplementedError()

    def __call__(self) -> typing.Generator[Transaction, None, None]:
        raise NotImplementedError()
