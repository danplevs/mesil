import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Union

import pandas as pd

SUPPORTED_EXTENSIONS = ['.csv', '.txt', '.xls', '.xlsx']
SUPPORTED_ANALYSES = [
    'asap',
    'dls',
    'fls-em',
    'fls-exc',
    'ftir',
    'solid-uv',
    'tga',
    'xrd',
    'xrf',
]


def get_delimiter(data_file: Path, bytes=22000) -> str:
    """Detect file delimiter in csv files.

    Args:
        data_file (Path): Path to file.
        bytes (int, optional): Bytes chunk to evaluate. Defaults to 22000.

    Returns:
        str: File delimiter.
    """
    sniffer = csv.Sniffer()
    data = open(data_file, 'r').read(bytes)
    delimiter = sniffer.sniff(data).delimiter
    return delimiter


def csv_reader(data_file: Union[Path, str], skip_rows: Optional[int] = None) -> pd.DataFrame:
    """Reads a csv file.

    Args:
        data_file (Path): Path to file.

    Returns:
        pd.DataFrame: Tabular data contained in the csv file.
    """
    delimiter = get_delimiter(data_file)
    return pd.read_csv(data_file, sep=delimiter, encoding='latin1', skiprows=skip_rows)


def excel_reader(data_file: Union[Path, str], skip_rows: Optional[int] = None, engine: str = 'xlrd') -> pd.DataFrame:
    """Reads a single-sheet excel file.

    Args:
        data_file (Path): Path to file.

    Returns:
        pd.DataFrame: Tabular data contained in the excel file.
    """
    return pd.read_excel(data_file, engine=engine, skiprows=skip_rows)
    ...


def set_reader(extension: str) -> Callable[[Path], pd.DataFrame]:
    """Set the appropriate data reader based on the file extension.

    Args:
        extension (str): Data file extension.

    Returns:
        Callable[[Path], pd.DataFrame]: Data reader function.
    """
    readers = {
        '.csv': csv_reader,
        '.txt': csv_reader,
        '.xls': excel_reader,
        '.xlsx': excel_reader,
    }
    return readers.get(extension.lower())
    

@dataclass
class DataFile:
    r"""A data file.
    
    Contains data generated by a material characterization, in the scope of Materials Chemistry. 

    Attributes:
        path: File's path.
        analysis: Analysis's acronym.
        delimiter: Data separator in csv files.
    
    Examples:
        >>> DataFile(path='data/raw/tga/2023-05-08/DIC14.txt', analysis='tga')
        DataFile(path=WindowsPath('data/raw/tga/2023-05-08/DIC14.txt'), analysis='tga', delimiter='\t')
        
        >>> DataFile(path='data/raw/asap/2023-04-19/DIC14.XLS', analysis='asap')
        DataFile(path=WindowsPath('data/raw/asap/2023-04-19/DIC14.XLS'), analysis='asap', delimiter='')
    """
    path: Union[Path, str]
    analysis: str
    delimiter: str = field(init=False)
    _reader: Callable[[Path], pd.DataFrame] = field(init=False, repr=False)

    def validate_path(self, path, **_) -> Path:
        """Ensures that input path is casted as Pathlib's Path object,
        check if it exists, and if the extension is supported.

        Args:
            path (Path): Input path

        Raises:
            FileNotFoundError: File does not exist.
            ValueError: Extension is currently not supported.

        Returns:
            Path: Validated path.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f'No such file {path}')
        if path.is_dir():
            raise ValueError(f'Attribute path should be a file, found dir {path}')
        if not path.suffix.lower() in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f'Extension {path.suffix} not supported, try one of {SUPPORTED_EXTENSIONS}'
            )
        return path

    def validate_analysis(self, analysis, **_) -> str:
        """Ensures analysis is stored in lowercase and that is supported.

        Args:
            analysis (str): Materials characterization method acronym.

        Raises:
            ValueError: Analysis currently not supported.

        Returns:
            str: Validated analysis
        """
        analysis = analysis.lower()
        if not analysis in SUPPORTED_ANALYSES:
            raise ValueError(
                f'{analysis.upper()} analysis not supported, try one of {SUPPORTED_ANALYSES}'
            )
        return analysis

    def __post_init__(self) -> None:
        """Run validation methods if declared.
        The validation method can be a simple check
        that raises ValueError or a transformation to
        the field value.
        The validation is performed by calling a function named:
            `validate_<field_name>(self, value, field) -> field.type`
        """
        for name, field in self.__dataclass_fields__.items():
            if method := getattr(self, f'validate_{name}', None):
                setattr(self, name, method(getattr(self, name), field=field))

        self.delimiter = (
            get_delimiter(self.path)
            if self.path.suffix.lower() in ['.csv', '.txt']
            else ''
        )
        self._reader = set_reader(self.path.suffix)
        self._extension = self.path.suffix.lower()

    def read(self) -> pd.DataFrame:
        skip_rows = 30 if self.analysis == 'tga' else None # especially needed to read tga data
        self.raw_data = self._reader(self.path, skip_rows=skip_rows)
        return self.raw_data

    def cleanse(self):
        ...

    def transform(self):
        ...

    def export(self):
        ...
