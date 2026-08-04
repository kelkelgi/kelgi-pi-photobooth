"""Physical shutter button service."""


class Button:
    """Read one button connected between a GPIO pin and ground."""

    def __init__(self, pin):
        try:
            from gpiozero import Button as GpioButton
        except ImportError as error:
            raise RuntimeError(
                "gpiozero is not installed. Run: sudo apt install -y python3-gpiozero"
            ) from error

        self._button = GpioButton(pin, pull_up=True, bounce_time=0.2)

    @property
    def pressed(self):
        return self._button.is_pressed

    def wait_for_release(self):
        self._button.wait_for_release()

    def close(self):
        self._button.close()
