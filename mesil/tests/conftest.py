import shutil
from pathlib import Path
from typing import Generator

import pytest

from mesil.config import Settings

RAW_DATA_DIR = Settings().paths.data.raw


def append_tmp_path(tmp_path: Path, path_to_append: Path):
    appended_tmp_path = tmp_path / path_to_append
    return appended_tmp_path


def mktree(path: Path):
    return path.mkdir(parents=True, exist_ok=True)


@pytest.fixture
def all_test_files(tmp_path: Path) -> Generator[Path, Path, Path]:
    file_paths = [
        RAW_DATA_DIR / 'ir' / '2022-12-14' / 'DIC1.CSV',
        RAW_DATA_DIR / 'tga' / '2023-02-01' / 'DIC3H.txt',
        RAW_DATA_DIR / 'fls' / '2023-03-06' / 'DIC3H_EM_3scan.txt',
    ]
    for file in file_paths:
        shutil.copy(file, tmp_path)
    return tmp_path.iterdir()


@pytest.fixture
def tga_test_file(tmp_path: Path) -> Path:
    file = RAW_DATA_DIR / 'tga' / '2023-02-01' / 'DIC3H.txt'
    shutil.copy(file, tmp_path)
    return tmp_path / file.name


@pytest.fixture
def fls_test_file(tmp_path: Path):
    file = RAW_DATA_DIR / 'fls' / '2023-03-06' / 'DIC3H_EM_3scan.txt'
    shutil.copy(file, tmp_path)
    return tmp_path / file.name


@pytest.fixture
def mev_folder(tmp_path: Path):
    folder = RAW_DATA_DIR / 'mev' / '2023-02-06'
    shutil.copytree(folder, tmp_path, dirs_exist_ok=True)
    return tmp_path
