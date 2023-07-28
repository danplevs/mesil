from pathlib import Path


def get_synthesis_code(data_file: Path) -> str:
    return data_file.stem.split("_")[0][:4]

def get_analysis(data_file: Path) -> str:
    return data_file.resolve().parts[-3]

def get_fluorescence_type(data_file: Path) -> str:
    str_path = str(data_file).lower()
    if "em" in str_path:
        return "emission"
    elif "exc" in str_path:
        return "excitation"
    return None
