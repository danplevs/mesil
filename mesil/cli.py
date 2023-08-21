import importlib.metadata
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.progress import (
    Progress,
    TextColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
    BarColumn,
)

from mesil.process.analysis import infer_analysis
from mesil.process.datafile import (
    SUPPORTED_EXTENSIONS,
    Analysis,
    DataFile,
)


def docstr_callback():
    """
    Process data from several different analyses and plot them.

    [red]Currently supported analyses[/red]:
        - Accelerated Surface Area and Porosity [green](asap)[/green]
        - Fluorescence Spectroscopy [green](fls-em, fls-exc)[/green]
        - Fourier Transformed Infrared Spectroscopy [green](ftir)[/green]
        - Solid-state UV-Vis Spectroscopy [green](solid-uv)[/green]
        - Thermogravimetric analysis [green](tga)[/green]
        - X-Ray diffraction [green](xrd)[/green]
        - X-Ray fluorescence [green](xrf)[/green]
    """


app = typer.Typer(rich_markup_mode='rich', callback=docstr_callback)


def version_callback(value: bool):
    if value:
        version = importlib.metadata.version('mesil')
        typer.echo(f'mesil {version}')
        raise typer.Exit()


@app.callback(invoke_without_command=False)
def version(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            '--version', callback=version_callback, help='Show current version'
        ),
    ] = False,
):
    pass


@app.command()
def process(
    path: Annotated[
        Path,
        typer.Argument(
            help='[green]File or directory[/green] with data :file_folder:.',
            show_default='Current directory',
            exists=True,
        ),
    ] = Path.cwd(),
    analysis: Annotated[
        Analysis,
        typer.Argument(
            help='[red]Analysis[/red] to process :microscope:.',
            show_default='Infer from `dir_or_file`',
            case_sensitive=False,
        ),
    ] = Analysis.infer,
    output: Annotated[
        Path,
        typer.Option(
            '--output',
            '-o',
            help='[blue]Export[/blue] results in the given output path :file_folder:.',
            show_default=False,
        ),
    ] = '',
):
    """
    Process analysis data from a file or multiple files in a directory.

    If --output is passed, data will be exported in the provided path,
    otherwise in dir_or_file.
    """
    console = Console()

    if path.is_file():
        infered_analysis = (
            infer_analysis(path) if analysis == 'infer' else analysis
        )
        data_file = DataFile(path=path, analysis=infered_analysis)
        data_file.read().clean().transform().export(output=output)
        console.log(f'[green bold]✅ Success![/] Exported {data_file._output}')
        return

    with Progress(
        TextColumn('[progress.description]{task.description}'),
        BarColumn(),
        MofNCompleteColumn(),
        TimeRemainingColumn()
    ) as progress:
        glob = [p for p in path.glob('**/*') if p.suffix.lower() in SUPPORTED_EXTENSIONS]
        total_processed = 0
        for file in progress.track(glob, description='Processing data...'):
            if file.suffix.lower() in SUPPORTED_EXTENSIONS:
                infered_analysis = (
                    infer_analysis(file) if analysis == 'infer' else analysis
                )
                data_file = DataFile(path=file, analysis=infered_analysis)
                data_file.read().clean().transform().export(output=output)
                total_processed += 1

    console.print(
        f'[green bold]✅ Success![/] Processed {total_processed} files'
    )


@app.command()
def plot():
    ...
