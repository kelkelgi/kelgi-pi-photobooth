"""The few settings an installer may need to change."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    shutter_pin: int = 16
    output_directory: Path = Path("photos")
    image_width: int = 1280
    image_height: int = 960
    preview_width: int = 640
    preview_height: int = 480
    countdown_seconds: int = 3
    printer_command: tuple[str, ...] = ()


CONFIG = Config()
