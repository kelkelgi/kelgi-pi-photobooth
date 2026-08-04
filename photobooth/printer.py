"""Optional printer service."""

import subprocess


class Printer:
    def __init__(self, command):
        self.command = tuple(command)

    @property
    def enabled(self):
        return bool(self.command)

    def print_photo(self, path):
        if not self.enabled:
            return False

        result = subprocess.run((*self.command, str(path)), check=False)
        return result.returncode == 0
