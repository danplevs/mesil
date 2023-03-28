from mesil.data.header import is_header, last_header_index
from mesil.data.process import cleanse_data, read_file_lines


def test_is_header(all_test_files):
    results = []
    for file in all_test_files:
        first_row = read_file_lines(file)[0]
        results.append(is_header(first_row))
    assert results == [False, True, True]


def test_last_header_index(all_test_files):
    all_data = [read_file_lines(file) for file in all_test_files]
    cleaned_data = [cleanse_data(raw_data) for raw_data in all_data]
    assert [last_header_index(data) for data in cleaned_data] == [None, 27, 21]
