"""Camera service backed by Raspberry Pi's Picamera2 library."""


class Camera:
    """Capture still photos and provide frames for the preview."""

    def __init__(self, config):
        try:
            from picamera2 import Picamera2
        except ImportError as error:
            raise RuntimeError(
                "Picamera2 is not installed. Run: sudo apt install -y python3-picamera2"
            ) from error

        self._picamera = Picamera2()
        self._picamera.configure(
            self._picamera.create_still_configuration(
                main={"size": (config.image_width, config.image_height), "format": "RGB888"},
            )
        )

    def start(self):
        self._picamera.start()

    def preview_frame(self):
        return self._picamera.capture_array("main")

    def capture(self, path):
        self._picamera.capture_file(str(path))

    def close(self):
        self._picamera.stop()
        self._picamera.close()
