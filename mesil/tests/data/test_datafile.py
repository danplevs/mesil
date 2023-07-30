import pandas as pd
import pytest

from mesil.data.datafile import DataFile, csv_reader, excel_reader, get_delimiter

test_datafile_read_csv_data = [('data/raw/fls-em/2023-05-15/DIC14.txt', 'fls-em'),
            ('data/raw/fls-exc/2023-04-19/DIC14.txt', 'fls-exc'),
            ('data/raw/ftir/2023-04-18/DIC14.CSV', 'ftir'),
            ('data/raw/solid-uv/2023-02-02/DIC3L.txt', 'solid-uv'),
            ('data/raw/tga/2023-05-08/DIC14.txt', 'tga'),
            ('data/raw/xrd/2023-04-14/DIC14.txt', 'xrd'),
            ('data/raw/xrf/2023-02-07/DIC3L.csv', 'xrf')]

test_csv_reader_data = [('data/raw/fls-em/2023-05-15/DIC14.txt', None),
            ('data/raw/fls-exc/2023-04-19/DIC14.txt', None),
            ('data/raw/ftir/2023-04-18/DIC14.CSV', None),
            ('data/raw/solid-uv/2023-02-02/DIC3L.txt', None),
            ('data/raw/tga/2023-05-08/DIC14.txt', 30),
            ('data/raw/xrd/2023-04-14/DIC14.txt', None),
            ('data/raw/xrf/2023-02-07/DIC3L.csv', None)]

test_get_delimiter_data = [('data/raw/fls-em/2023-05-15/DIC14.txt', ','),
            ('data/raw/fls-exc/2023-04-19/DIC14.txt', ','),
            ('data/raw/ftir/2023-04-18/DIC14.CSV', ','),
            ('data/raw/solid-uv/2023-02-02/DIC3L.txt', '\t'),
            ('data/raw/tga/2023-05-08/DIC14.txt', '\t'),
            ('data/raw/xrd/2023-04-14/DIC14.txt', ','),
            ('data/raw/xrf/2023-02-07/DIC3L.csv', ',')]

@pytest.mark.parametrize('csv_path, expected', test_get_delimiter_data)
def test_get_delimiter(csv_path, expected):
    assert get_delimiter(csv_path) == expected

@pytest.mark.parametrize('csv_path, skip_rows', test_csv_reader_data)
def test_csv_reader(csv_path, skip_rows):
    data = csv_reader(csv_path, skip_rows=skip_rows)
    assert isinstance(data, pd.DataFrame)
    
def test_excel_reader():
    data = excel_reader('data/raw/asap/2023-04-19/DIC14.XLS')
    assert isinstance(data, pd.DataFrame)


class TestDataFile:
    def test_raise_error_file_not_found(self):
        with pytest.raises(FileNotFoundError, match='No such file .*'):
            DataFile(path='xpto.txt', analysis='tga')

    def test_raise_error_is_directory(self):
        with pytest.raises(
            ValueError, match='Attribute path should be a file, found dir .*'
        ):
            DataFile(path='mesil/', analysis='tga')

    def test_raise_error_extension_not_supported(self):
        with pytest.raises(
            ValueError, match='Extension .* not supported, try one of .*'
        ):
            DataFile(path='pyproject.toml', analysis='tga')

    def test_raise_error_analysis_not_supported(self):
        with pytest.raises(
            ValueError, match='.* analysis not supported, try one of .*'
        ):
            DataFile(path='data/raw/xrf/2023-02-07/DIC3L.csv', analysis='eds')
            
    def test_uppercase_analysis_validation(self):
        data_file = DataFile(path=test_csv_reader_data[0][0], analysis='FLS-EM')
        assert data_file.analysis == 'fls-em'

    @pytest.mark.parametrize('csv_path, analysis', test_datafile_read_csv_data)
    def test_datafile_read_csv(self, csv_path: str, analysis: str):
        data_file = DataFile(path=csv_path, analysis=analysis)
        assert isinstance(data_file.read(), pd.DataFrame)
        
    def test_datafile_read_excel(self):
        data_file = DataFile(path='data/raw/asap/2023-04-19/DIC14.XLS', analysis='asap')
        assert isinstance(data_file.read(), pd.DataFrame)
        

    
    
    
    