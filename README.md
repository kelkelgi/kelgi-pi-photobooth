# Raspberry Pi Photobooth

A small Raspberry Pi 3 photobooth: press a button, see a countdown, and save a JPEG.

## Install on the Pi

Use Raspberry Pi OS with the camera connected to the CSI port.

```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-gpiozero python3-pygame
python3 -m photobooth.main
```

Before starting the booth, check the camera:

```bash
rpicam-hello -t 5000
```

Connect the shutter button between BCM GPIO 16 and GND. The program uses the internal pull-up, so the button is pressed when the pin is connected to ground.

Photos are saved in `photos/`.

## Change settings

Edit `photobooth/config.py`. The defaults are:

- GPIO pin 16
- `photos/` output folder
- 1280x960 still images
- 640x480 preview
- 3-second countdown
- no printer

To use a printer command, change the default in `photobooth/config.py`, for example:

```python
printer_command = ("lp",)
```

The saved JPEG is always created before printing is attempted.

Press Escape to stop the program.

## Run the tests

The tests do not need a Raspberry Pi or camera:

```bash
python3 -m unittest discover
```
