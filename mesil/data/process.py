import logging
from pathlib import Path

import pandas as pd

from mesil.data.files import (change_extension, filter_analysis, filter_extensions, read_data)
from mesil.data.metadata import get_analysis
from mesil.data.transform import add_tga_weight

logging.basicConfig(level=logging.INFO)


def process_data(data_file: Path) -> pd.DataFrame:
    origin = read_data(data_file)
    clean_data = origin.dropna(axis="columns").dropna(axis="index")
    if get_analysis(data_file) == "tga":
        add_tga_weight(clean_data)
    return clean_data


def process_path(data_file: Path) -> Path:
    file_parts = list(data_file.parts)
    file_parts[1] = 'processed'   # change data status
    out_path = Path(*file_parts)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    return change_extension(Path(*file_parts))


def write_data(data: pd.DataFrame, to_path: Path):
    data.to_csv(
        process_path(to_path),
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
        output_path = process_path(file)
        write_data(data, output_path)
        
        logging.info(f'Processed {file} -> {output_path}')
        
    logging.info('SUCCESS: processed all files!')


if __name__ == '__main__':
    main()
