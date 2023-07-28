from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import matplotlib.pyplot as plt
from mesil.config import Settings


def axes_from_style_sheet(
    sheet_name: str = 'default',
    sheet_folder: Path = Settings().paths.style_sheets,
) -> plt.Axes:
    """Generates a style sheet's based axes.

    Args:
        sheet_name (Union[str, Path], optional): Style sheet's file name. Defaults to "default".

    Returns:
        plt.Axes: Customized axes.
    """
    sheet_path = (sheet_folder / sheet_name).with_suffix(".mplstyle")
    plt.style.use(sheet_path)
    return plt.axes()


def customizer(analysis: str) -> None:
    analysis_params = get_analysis_parameters(analysis)
    plt.xlabel(analysis_params["xlabel"])
    plt.ylabel(analysis_params["ylabel"])
    plt.autoscale(axis='y') 

def get_analysis_parameters(
    analysis: str,
) -> Dict[str, Any]:
    parameter_generators = {
        'ftir': FTIR_parameters(),
        'xrd': XRD_parameters(),
        'tga': TGA_parameters(),
        'fls-em': FLSEM_parameters(),
        'fls-exc': FLSEXC_parameters(),
    }
    parameters = parameter_generators.get(analysis)
    return parameters


def FTIR_parameters() -> Dict[str, Any]:
    return dict(xlim=[4000, 500], xlabel=r'Wavenumber (cm$^{-1}$)', ylabel=r'Transmittance (%)')


def XRD_parameters() -> Dict[str, Any]:
    return dict(xlim=[1.2, 6.0], xlabel=r'2{\theta} (degrees)', ylabel=r'Intensity (a.u.)')


def TGA_parameters() -> Dict[str, Any]:
    return dict(xlim=[30, 600], xlabel=r'Temperature ($^\circ$C)', ylabel=r'Weight (%)')


def FLSEM_parameters() -> Dict[str, Any]:
    return dict(xlim=[450, 750], xlabel=r'Wavelength (nm)', ylabel=r'Intensity (a.u.)')
    

def FLSEXC_parameters() -> Dict[str, Any]:
    return dict(xlim=[250, 575], xlabel=r'Wavelength (nm)', ylabel=r'Intensity (a.u.)')
