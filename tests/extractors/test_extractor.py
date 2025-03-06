import pathlib

import pytest

from beanhub_extract.extractors import detect_extractor


@pytest.mark.parametrize(
    "input_file, extractor_name",
    [
        ("mercury.csv", "mercury"),
        ("chase_credit_card.csv", "chase_credit_card"),
        ("wealthsimple.csv", "wealthsimple"),
        ("other.csv", None),
        (pytest.lazy_fixture("zip_file"), None),
    ],
)
def test_detect_extractor(
    fixtures_folder: pathlib.Path, input_file: str, extractor_name: str | None
):
    with open(fixtures_folder / input_file, "rt") as fo:
        extractor_cls = detect_extractor(fo)
        if extractor_name is None:
            assert extractor_cls is None
        else:
            assert extractor_cls.EXTRACTOR_NAME == extractor_name
