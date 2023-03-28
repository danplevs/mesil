from pathlib import Path
import re
from typing import Any, List


def has_float_starter(string: str) -> bool:
    if not string:
        return False
    first_char = string[0]
    return first_char in '.-0123456789'


def regex_split(string: str, regex: str = r'[\s]+|,') -> List[str]:
    return re.split(regex, string.strip())


def wrap_list(lst: List[Any]) -> List[List[Any]]:
    wrapped_list = [[value] for value in lst]
    return wrapped_list


def use_whitespace_delimiter(data: str):
    if ',' in data:
        return False
    else:
        return True

def FLS_xlim(file: Path):
    str_path = str(file).lower()
    if "em" in str_path:
        xlim = [250, 450]
    if "exc" in str_path:
        xlim = [450, 750]
    return xlim
