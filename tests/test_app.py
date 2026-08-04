import tempfile
import unittest
from pathlib import Path

from photobooth.app import Photobooth
from photobooth.config import Config
from photobooth.storage import PhotoStorage


class FakeCamera:
    def __init__(self):
        self.captures = []
        self.closed = False

    def start(self):
        pass

    def preview_frame(self):
        return "preview"

    def capture(self, path):
        self.captures.append(path)

    def close(self):
        self.closed = True


class FakeButton:
    pressed = False

    def wait_for_release(self):
        pass

    def close(self):
        pass


class FakePrinter:
    def __init__(self, result=True):
        self.result = result
        self.printed = []

    def print_photo(self, path):
        self.printed.append(path)
        return self.result


class FakeDisplay:
    def __init__(self):
        self.countdowns = []
        self.errors = []
        self.closed = False

    def show_countdown(self, frame, number):
        self.countdowns.append(number)

    def show_success(self, printed):
        self.printed = printed

    def show_error(self, message):
        self.errors.append(message)

    def close(self):
        self.closed = True


class PhotoboothTests(unittest.TestCase):
    def test_capture_saves_and_prints_one_photo(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Config(output_directory=Path(directory), countdown_seconds=0)
            camera = FakeCamera()
            printer = FakePrinter()
            display = FakeDisplay()
            app = Photobooth(
                config, camera, FakeButton(), PhotoStorage(Path(directory)), printer, display, sleep=lambda _: None
            )

            app.take_photo()

            self.assertEqual(len(camera.captures), 1)
            self.assertEqual(printer.printed, camera.captures)
            self.assertTrue(display.printed)

    def test_print_failure_does_not_discard_photo(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Config(output_directory=Path(directory), countdown_seconds=0)
            camera = FakeCamera()
            display = FakeDisplay()
            app = Photobooth(
                config,
                camera,
                FakeButton(),
                PhotoStorage(Path(directory)),
                FakePrinter(False),
                display,
                sleep=lambda _: None,
            )

            app.take_photo()

            self.assertEqual(len(camera.captures), 1)
            self.assertFalse(display.printed)
            self.assertEqual(display.errors, [])

    def test_close_releases_services(self):
        camera = FakeCamera()
        display = FakeDisplay()
        app = Photobooth(Config(countdown_seconds=0), camera, FakeButton(), object(), FakePrinter(), display)

        app.close()

        self.assertTrue(camera.closed)
        self.assertTrue(display.closed)


if __name__ == "__main__":
    unittest.main()
