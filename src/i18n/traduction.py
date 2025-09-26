import json
from pathlib import Path

from src.domain.constants import LANGUAGE


def tr(key: str) -> str:
    file_path = Path(f"src/i18n/{LANGUAGE}.json")
    with open(file_path, "r") as file:
        traductions = json.load(file)
    return traductions.get(key, key)  # type: ignore
