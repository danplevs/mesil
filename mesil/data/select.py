"""Column selectors."""
from typing import Callable, Dict

import pandas as pd


def get_selector(analysis: str) -> Callable[[pd.DataFrame], Dict[pd.Series, pd.Series]]:
    selectors = {
        'ftir': FTIR_selector,
        'xrd': XRD_selector,
        'tga': TGA_selector,
        'fls': FLS_selector,
    }
    selector = selectors.get(analysis)
    return selector
    
def FTIR_selector(data: pd.DataFrame) -> Dict[str, int]:
    return {"x": data[0], "y": data[1]}

def XRD_selector(data: pd.DataFrame) -> Dict[str, int]:
    return {"x": data[0], "y": data[1]}

def TGA_selector(data: pd.DataFrame) -> Dict[str, int]:
    return {"x": data[1], "y": data[4]}

def FLS_selector(data: pd.DataFrame) -> Dict[str, int]:
    return {"x": data[0], "y": data[1]}
    