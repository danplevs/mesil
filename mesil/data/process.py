import io
import logging
from pathlib import Path

import pandas as pd

from mesil.data.cleanse import cleanse_data
from mesil.data.files import (filter_analysis, filter_extensions,
                              process_data_path, read_file_lines)
from mesil.data.filter import filter_numeric_data
from mesil.data.transform import add_tga_weight
from mesil.data.utils import use_whitespace_delimiter

logging.basicConfig(level=logging.INFO)


def process_data(file: Path) -> pd.DataFrame:
    original_data = read_file_lines(file)
    clean_data = cleanse_data(original_data)
    filtered_data = filter_numeric_data(clean_data)
    delim_whitespace = use_whitespace_delimiter(filtered_data[0])
    dataframe = pd.read_csv(
        io.StringIO('\n'.join(filtered_data)),
        delim_whitespace=delim_whitespace,
        header=None,
    )
    return dataframe


def write_data(data: pd.DataFrame, path: Path):
    data.to_csv(
        process_data_path(path),
        sep=',',
        header=False,
        index=False,
        encoding='utf-8',
    )


def main():
    files_to_process = [
        file for file in filter_extensions() if file in filter_analysis()
    ]
    for file in files_to_process:
        data = process_data(file.resolve())
        if file.parts[2] == 'tga':
            add_tga_weight(data)
        output_path = process_data_path(file)
        write_data(data, output_path)

        logging.info(f'Processed {file} -> {output_path}')
    logging.info('SUCCESS: processed all files!')


if __name__ == '__main__':
    main()
