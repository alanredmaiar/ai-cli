from pathlib import Path

from pydantic_settings import BaseSettings
import tomli


class Settings(BaseSettings):
    PYPROJECT_PATH: Path = Path(__file__).parents[2] / "pyproject.toml"

    PYPROJECT: dict = tomli.load(PYPROJECT_PATH.open("rb"))


settings = Settings()
