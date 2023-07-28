"""Column selectors."""
from numbers import Number
from typing import Callable, Dict, List

import pandas as pd


def get_selector(analysis: str) -> Callable[[pd.DataFrame], Dict[pd.Series, pd.Series]]:
    selectors = {
        'ftir': FTIR_selector,
        'xrd': XRD_selector,
        'tga': TGA_selector,
        'fls-em': FLSEM_selector,
        'fls-exc': FLSEXC_selector,
    }
    selector = selectors.get(analysis)
    return selector
    
def FTIR_selector(data: pd.DataFrame, xlim: List[Number]) -> Dict[str, pd.Series]:
    return {"x": data[0], "y": data[1]}

def XRD_selector(data: pd.DataFrame, xlim: List[Number]) -> Dict[str, pd.Series]:
    return {"x": data[0], "y": data[1]}

def TGA_selector(data: pd.DataFrame, xlim: List[Number]) -> Dict[str, pd.Series]:
    return {"x": data[1], "y": data[4]}

def FLSEM_selector(data: pd.DataFrame, xlim: List[Number]) -> Dict[str, pd.Series]:
    return {"x": data[0], "y": data[1]}

def FLSEXC_selector(data: pd.DataFrame, xlim: List[Number]) -> Dict[str, pd.Series]:
    return {"x": data[0], "y": data[1]}
