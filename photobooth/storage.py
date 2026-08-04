"""Save captured photos without overwriting previous photos."""

from datetime import datetime


class PhotoStorage:
    def __init__(self, output_directory):
        self.output_directory = output_directory
        self.output_directory.mkdir(parents=True, exist_ok=True)

    def new_photo_path(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        return self.output_directory / f"photo_{timestamp}.jpg"
