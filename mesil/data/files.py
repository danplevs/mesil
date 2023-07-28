import csv
from pathlib import Path
from typing import List, Union

import pandas as pd

from mesil.config import Settings
from mesil.data.metadata import get_analysis


def read_data(data_file: Path) -> pd.DataFrame:
    delimiter = get_delimiter(data_file)
    skip_rows = determine_rows_to_skip(data_file)
    data = pd.read_csv(data_file, skiprows=skip_rows, sep=delimiter, header=None, encoding="latin1").dropna(axis="columns", how="all")
    return data

def determine_rows_to_skip(data_file: Path) -> Union[int, None]:
    analysis = get_analysis(data_file)
    if analysis == "tga":
        return 33
    elif analysis == "fls-em" or analysis == "fls-exc":
        return 22
    else:
        return None


def get_delimiter(data_file: Path, bytes=22000):
    sniffer = csv.Sniffer()
    data = open(data_file, "r").read(bytes)
    delimiter = sniffer.sniff(data).delimiter
    return delimiter


def change_extension(data_file: Path, to_ext: str = '.csv') -> Path:
    return data_file.with_suffix(to_ext)


def filter_extensions(
    data_root: Path = Settings().paths.data.raw, extensions: List[str] = None
) -> List[Path]:
    if not extensions:
        extensions = ['.txt', '.csv']
    paths = [p for p in data_root.glob('**/*') if p.suffix.lower() in extensions]
    return paths


def filter_analysis(
    data_root: Path = Settings().paths.data.raw, analyses: List[str] = None
):
    if not analyses:
        analyses = ['fls-exc', 'fls-em', 'ftir', 'solid-uv', 'tga', 'xrd']
    paths = [data_file for data_file in data_root.glob('**/*') if get_analysis(data_file) in analyses]
    return paths
