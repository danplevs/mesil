from typing import List


def cleanse_data(data: List[str]) -> List[str]:
    clean_data = remove_trailing_chars(data)
    clean_data = remove_blank(clean_data)
    return clean_data


def remove_trailing_chars(data: List[str], chars=',\n') -> List[str]:
    stripped_data = [line.rstrip(chars) for line in data]
    return stripped_data


def remove_blank(data: List[str]) -> List[str]:
    filtered_data = list(filter(None, data))
    return filtered_data
