from typing import List

import numpy.typing as npt
import pandas as pd


def percentage_by_first_value(array: npt.ArrayLike) -> npt.ArrayLike:
    """Return a percentage array based on its first value.

    Args:
        array (npt.ArrayLike): Input array.

    Returns:
        npt.ArrayLike: Divided array.
    """
    divided_array: npt.ArrayLike = (array / array[0]) * 100
    return divided_array


def add_tga_weight(data: pd.DataFrame) -> pd.DataFrame:
    data[4] = percentage_by_first_value(data[3])
    return data
