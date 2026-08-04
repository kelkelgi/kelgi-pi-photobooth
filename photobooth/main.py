"""Application entry point."""

from .app import Photobooth
from .button import Button
from .camera import Camera
from .config import CONFIG
from .display import Display
from .printer import Printer
from .storage import PhotoStorage


def main():
    config = CONFIG
    try:
        camera = Camera(config)
        button = Button(config.shutter_pin)
        storage = PhotoStorage(config.output_directory)
        printer = Printer(config.printer_command)
        display = Display(config.preview_width, config.preview_height)
        Photobooth(config, camera, button, storage, printer, display).run()
    except RuntimeError as error:
        print(f"Startup error: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
