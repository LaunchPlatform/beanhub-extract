import os
import typing

from .base import ExtractorBase
from .chase import ChaseCreditCardExtractor
from .mercury import MercuryExtractor
from .plaid import PlaidExtractor
from .wealthsimple import WealthsimpleExtractor

ALL_EXTRACTORS: dict[str, typing.Type[ExtractorBase]] = {
    MercuryExtractor.EXTRACTOR_NAME: MercuryExtractor,
    ChaseCreditCardExtractor.EXTRACTOR_NAME: ChaseCreditCardExtractor,
    PlaidExtractor.EXTRACTOR_NAME: PlaidExtractor,
    WealthsimpleExtractor.EXTRACTOR_NAME: WealthsimpleExtractor,
}


def detect_extractor(input_file: typing.TextIO) -> typing.Type[ExtractorBase]:
    for extractor_cls in ALL_EXTRACTORS.values():
        input_file.seek(os.SEEK_SET)
        if extractor_cls(input_file).detect():
            return extractor_cls
