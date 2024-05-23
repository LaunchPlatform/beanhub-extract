import os
import typing

from .base import ExtractorBase
from .mercury import MercuryExtractor

ALL_EXTRACTORS: dict[str, typing.Type[ExtractorBase]] = {
    MercuryExtractor.EXTRACTOR_NAME: MercuryExtractor,
}


def detect_extractor(input_file: typing.TextIO) -> typing.Type[ExtractorBase]:
    for extractor_cls in ALL_EXTRACTORS.values():
        input_file.seek(os.SEEK_SET)
        if extractor_cls(input_file).detect():
            return extractor_cls
