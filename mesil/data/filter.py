from typing import List

from mesil.data.header import last_header_index


def filter_numeric_data(data: List[str]) -> List[str]:
    filter = last_header_index(data)
    if filter:
        return data[filter:]
    else:
        return data
