from pathlib import Path
from typing import List

from mesil.config import Settings


def read_file_lines(file: Path) -> List[str]:
    with file.open(encoding='latin-1') as f:
        lines = f.readlines()
    return lines


def change_extension(file: Path, to_ext: str = '.csv') -> Path:
    return file.with_suffix(to_ext)


def filter_extensions(
    root: Path = Settings().paths.data.raw, extensions: List[str] = None
) -> List[Path]:
    if not extensions:
        extensions = ['.txt', '.csv']
    paths = [p for p in root.glob('**/*') if p.suffix.lower() in extensions]
    return paths


def filter_analysis(
    root: Path = Settings().paths.data.raw, analyses: List[str] = None
):
    if not analyses:
        analyses = ['fls', 'ftir', 'solid-uv', 'tga', 'xrd']
    paths = []
    for p in root.glob('**/*'):
        analysis = p.parts[2]
        if analysis in analyses:
            paths.append(p)
    return paths


def process_data_path(file: Path):
    file_parts = list(file.parts)
    file_parts[1] = 'processed'   # change data status
    out_path = Path(*file_parts)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    return change_extension(Path(*file_parts))


def get_synthesis_code(file: Path) -> str:
    return file.stem.split("_")[0]
