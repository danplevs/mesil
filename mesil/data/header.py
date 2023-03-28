from typing import List

from mesil.data.utils import has_float_starter, regex_split


def is_header(row: str) -> bool:
    if not has_float_starter(row[0]):
        return True
    values = regex_split(row)
    return any(not has_float_starter(value) for value in values)


def last_header_index(data: List[str]) -> int:
    if not is_header(data[0]):
        return None
    index = 0
    for row in data:
        if is_header(row):
            index += 1
    return index
