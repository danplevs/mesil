from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

import matplotlib.pyplot as plt
from mesil.process.datafile import Analysis


def axes_from_style_sheet(style_sheet: Path = Path('mesil/plot/stylesheets/default.mplstyle')) -> plt.Axes:
    """Generates a style sheet's based axes.

    Args:
        style_sheet (Path): Style sheet's path.

    Returns:
        plt.Axes: Customized axes.
    """
    plt.style.use(style_sheet)
    return plt.axes()


@dataclass
class PlotCustomizer(ABC):
    """Representation of matplotlib's plot customizer."""
    
    ax: plt.Axes | None = field(init=True, default_factory=axes_from_style_sheet)
    xlim: tuple | None = field(init=False, default=None)
    ylim: tuple | None = field(init=False, default=None)
    xlabel: str | None = field(init=False, default=None)
    ylabel: str | None = field(init=False, default=None)
    xcolumn: str | int | None = field(init=False, default=None)
    ycolumn: str | int | None = field(init=False, default=None)
    
    

    def __post_init__(self):
        if self.ax is None:
            self.ax = axes_from_style_sheet(self.style_sheet)

    @abstractmethod
    def customize(self) -> plt.Axes:
        """Customize plot axes."""
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)


class CustomizerFactory:
    @classmethod
    def from_analysis(cls, analysis: Analysis, **kwargs) -> PlotCustomizer:
        FACTORIES = {
            'asap-bet': AsapBETCustomizer,
            'asap-bjh': AsapBJHCustomizer,
            'fls-em': FlsEmissionCustomizer,
            'fls-exc': FlsExcitationCustomizer,
            'ftir': FTIRCustomizer,
            'solid-uv': UVCustomizer,
            'tga': TGACustomizer,
            'xrd': XRDCustomizer,
        }
        customizer = FACTORIES.get(analysis, DefaultCustomizer)
        return customizer(**kwargs)


class DefaultCustomizer(PlotCustomizer):
    pass


class AsapBETCustomizer(PlotCustomizer):
    """ASAP nitrogen isotherms customizer."""
    
    xlim = (0, 1)
    xlabel = r'Relative Pressure (P/P_{0})'
    ylabel = r'Quantity Adsorbed (cm^{3}/g STP)'
    xcolumn = 

    
    def customize(self) -> plt.Axes:
        super().customize()
        return self.ax


class AsapBJHCustomizer(PlotCustomizer):
    """ASAP diameter distribution customizer."""

    xlim = (2, 10)
    xlabel = r'Pore diamater (nm)'
    ylabel = r'dV/dlog(D) Pore Volume (cm^{3}/g)'

    def customize(self) -> plt.Axes:
        super().customize()
        return self.ax


class FlsEmissionCustomizer(PlotCustomizer):
    """Fluorescence Spectroscopy emission spectrum customizer."""

    xlabel = r'Wavelength (nm)'
    ylabel = r'Intensity (a.u.)'

    def customize(self) -> plt.Axes:
        super().customize()
        return self.ax


class FlsExcitationCustomizer(PlotCustomizer):
    """Fluorescence Spectroscopy excitation spectrum customizer."""

    xlabel = r'Wavelength (nm)'
    ylabel = r'Intensity (a.u.)'

    def customize(self) -> plt.Axes:
        super().customize()
        return self.ax


class FTIRCustomizer(PlotCustomizer):
    """Fourier Transformed Infrared Spectroscopy spectrum customizer."""

    xlabel = r'Wavenumber (cm$^{-1}$)'
    ylabel = r'Transmittance (%)'

    def customize(self) -> plt.Axes:
        super().customize()
        return self.ax


class UVCustomizer(PlotCustomizer):
    """UV-Vis Spectroscopy spectrum customizer."""

    xlabel = r'Wavelength (nm)'
    ylabel = r'Absorbance (a.u.)'

    def customize(self) -> plt.Axes:
        super().customize()
        return self.ax


class TGACustomizer(PlotCustomizer):
    """Thermogravimetric analysis customizer."""

    xlabel = r'Temperature ($^\circ$C)'
    ylabel = r'Weight (%)'

    def customize(self) -> plt.Axes:
        super().customize()
        return self.ax

@dataclass
class XRDCustomizer(PlotCustomizer):
    """Thermogravimetric analysis customizer."""
    
    xlabel = r'2{\theta} (degrees)'
    ylabel = r'Intensity (a.u.)'
    
    def customize(self) -> plt.Axes:
        super().customize()
        return self.ax


def main():
    print(Path.cwd())
    analysis = 'asap-bet'
    customizer = CustomizerFactory.from_analysis(analysis)
    ax = customizer.customize()
    print(ax.get_xlabel())

if __name__ == '__main__':
    main()
