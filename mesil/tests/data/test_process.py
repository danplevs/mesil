import pandas as pd

from mesil.config import Settings
from mesil.data.cleanse import cleanse_data
from mesil.data.files import change_extension, read_file_lines
from mesil.data.process import filter_analysis, filter_extensions, process_data

RAW_DATA_DIR = Settings().paths.data.raw


def test_read_file_lines(all_test_files):
    assert [type(read_file_lines(file)) is list for file in all_test_files]


def test_cleanse_data(fls_test_file):
    data = read_file_lines(fls_test_file)
    processed_data = cleanse_data(data)
    assert [row[-3:] != ',\n' for row in processed_data]


def test_process_data(all_test_files):
    processed_data = [process_data(file) for file in all_test_files]
    assert all(isinstance(data, pd.DataFrame) for data in processed_data)


def test_change_extension(all_test_files):
    for file in all_test_files:
        assert change_extension(file, '.csv') == file.with_suffix('.csv')


def test_filter_extensions_none(mev_folder):
    assert filter_extensions(mev_folder) == []


def test_filter_extensions_txt():
    assert (
        len(filter_extensions(root=RAW_DATA_DIR / 'fls' / '2023-03-06')) == 7
    )


def test_filter_analysis_none(mev_folder):
    assert filter_analysis(mev_folder) == []


def test_filter_analysis_fls():
    fls_folder = RAW_DATA_DIR / 'fls'
    assert len(filter_analysis(fls_folder)) == len(
        [file for file in fls_folder.glob('**/*')]
    )
