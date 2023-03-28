from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, BaseSettings
from pydantic.env_settings import SettingsSourceCallable


def yml_config_setting(settings: BaseSettings) -> dict[str, Any]:
    config_path = Path(__file__).parent / 'conf/config.yml'
    with config_path.open() as file:
        return yaml.safe_load(file)


class DataPaths(BaseModel):
    raw: Path
    external: Path
    interim: Path
    processed: Path


class Paths(BaseModel):
    data: DataPaths
    style_sheets: Path
    figures: Path


class Settings(BaseSettings):
    paths: Paths

    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            # Add load from yml file, change priority and remove file secret option
            return (
                init_settings,
                yml_config_setting,
                env_settings,
                file_secret_settings,
            )
