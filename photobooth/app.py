"""The photobooth workflow. Hardware services are passed in, so this is testable."""

import time


class Photobooth:
    def __init__(self, config, camera, button, storage, printer, display, sleep=time.sleep):
        self.config = config
        self.camera = camera
        self.button = button
        self.storage = storage
        self.printer = printer
        self.display = display
        self.sleep = sleep

    def run(self):
        self.camera.start()
        try:
            while not self.display.should_exit():
                self.display.show_idle()
                if self.button.pressed:
                    self.button.wait_for_release()
                    self.take_photo()
                self.sleep(0.05)
        finally:
            self.close()

    def take_photo(self):
        try:
            path = self._countdown_and_capture()
            printed = self.printer.print_photo(path)
            self.display.show_success(printed)
            self.sleep(2)
        except Exception as error:  # Hardware errors should be visible, not silent.
            self.display.show_error(str(error))
            self.sleep(2)

    def _countdown_and_capture(self):
        for number in range(self.config.countdown_seconds, 0, -1):
            end = time.monotonic() + 1
            while time.monotonic() < end:
                self.display.show_countdown(self.camera.preview_frame(), number)
                self.sleep(0.05)

        path = self.storage.new_photo_path()
        self.camera.capture(path)
        return path

    def close(self):
        self.camera.close()
        self.button.close()
        self.display.close()
