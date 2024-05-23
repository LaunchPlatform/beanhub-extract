import pathlib
import zipfile

import pytest

TEST_PACKAGE_FOLDER = pathlib.Path(__file__).parent
FIXTURE_FOLDER = TEST_PACKAGE_FOLDER / "fixtures"


@pytest.fixture
def fixtures_folder() -> pathlib.Path:
    return FIXTURE_FOLDER


@pytest.fixture
def zip_file(tmp_path: pathlib.Path) -> pathlib.Path:
    text_file = tmp_path / "hello.txt"
    text_file.write_text("BeanHub is awesome")
    zip_file = tmp_path / "hello.zip"
    with zipfile.ZipFile(zip_file, "w") as zip:
        zip.write(text_file)
    return zip_file
