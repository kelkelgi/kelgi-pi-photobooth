## Problem Statement

The current Raspberry Pi photobooth project is not runnable for its intended user. The referenced implementation is one Python script with no dependency manifest, installation instructions, wiring assumptions, sample assets, printer setup, or verification steps. It also invokes the deprecated `raspistill` legacy camera stack.

The goal is a small, understandable Raspberry Pi 3 photobooth that a friend can assemble, install, launch, and use without reverse-engineering missing libraries or undocumented commands.

## Solution

Build a documented MVP that displays an idle screen, waits for a physical shutter button, shows a live preview and 3-2-1 countdown, captures one JPEG through Picamera2/libcamera, saves it locally with a timestamped filename, and shows success or actionable errors. Optional thermal printing may be configured, but printing must not be required for capture or risk the saved JPEG.

Use Raspberry Pi's current camera stack guidance: [Picamera2/libcamera camera software](https://www.raspberrypi.com/documentation/computers/camera_software.html).

## User Stories

1. As a photobooth operator, I want the application to start with one documented command, so that I do not need to understand the internals.
2. As a Raspberry Pi 3 owner, I want camera detection and failures reported clearly, so that wiring and software problems are diagnosable.
3. As a builder, I want supported Raspberry Pi OS assumptions, system packages, Python libraries, wiring, and GPIO numbering documented, so that a fresh installation is reproducible.
4. As a builder, I want a separate camera verification command, so that I can validate hardware before debugging the application.
5. As a guest, I want an idle screen that says the booth is ready, so that I know when to press the button.
6. As a guest, I want a live camera preview and visible 3-2-1 countdown, so that I can position myself and know when the photo is taken.
7. As a guest, I want one button press to produce exactly one photo, so that bounce or a held button cannot trigger duplicates.
8. As an operator, I want each photo saved to a predictable, automatically-created output directory with a unique timestamped name, so that photos are not overwritten.
9. As an operator, I want configurable output path, dimensions, GPIO pin, and countdown duration, so that the booth can fit different setups.
10. As an operator, I want camera, GPIO, display, storage, and printer errors shown in readable language, so that I can recover without reading source code.
11. As an operator, I want the booth to return to idle after capture, so that the next person can use it.
12. As an operator, I want optional printer support, so that the booth can work with a thermal printer without making one mandatory.
13. As an operator, I want printer failure to preserve the JPEG, so that printing cannot destroy the primary artifact.
14. As an operator, I want a clean keyboard exit and reliable resource cleanup, so that I can stop and restart the program safely.
15. As a maintainer, I want explicit idle, countdown, capture, save/print, success, and error states, so that behavior is easy to reason about.
16. As a maintainer, I want camera, input, storage, printer, and UI adapters replaceable with fakes, so that behavior can be tested without Pi hardware.
17. As a user, I want the experience to be local and account-free, so that no network or cloud service is required at runtime.

## Implementation Decisions

- Treat the application as a small single-process state machine with explicit idle, countdown, capture, persistence/printing, success, and error states.
- Use Picamera2/libcamera as the primary camera interface. Do not build the MVP around `raspistill`, `raspivid`, or legacy Picamera.
- Target Raspberry Pi 3 and document the tested Raspberry Pi OS/image assumptions and camera-module compatibility boundary.
- Use a lightweight fullscreen display appropriate for a Pi 3; no browser or network service.
- Require one physical shutter button using BCM GPIO numbering, a documented default pin, an internal pull-up or pull-down, and configurable pin settings.
- Keep shutdown/reboot out of the required MVP. If later retained, it is optional and disabled by default.
- Save the JPEG to local storage before attempting any print. Printing is optional, configurable, and non-fatal to capture.
- Centralize settings for GPIO, output directory, preview/capture size, countdown duration, and printer behavior.
- Provide install instructions using Raspberry Pi OS packages where appropriate, plus a camera test and real-device checklist.
- Generate UI screens in code or ship documented assets so missing files cannot prevent startup.
- Separate camera, button/input, storage, optional printer, and UI/orchestrator boundaries. Avoid shell pipelines in the core capture path.
- Do not require internet access at runtime.
- Use the referenced project's idle/countdown/capture/printing flow as inspiration while replacing undocumented and legacy assumptions.

## Testing Decisions

- The highest-value seam is the end-to-end photobooth controller with injected camera, input, storage, printer, and UI adapters.
- Test observable behavior: one button press creates one capture, one unique saved JPEG, and a return to idle.
- Test held/noisy buttons, countdown cancellation/exit, cleanup, camera-unavailable, storage-write, and printer-failure cases.
- Printer failure must preserve the saved JPEG and produce a visible warning/error.
- Test configuration defaults and invalid values.
- Because the repository currently has no tests or implementation, use standard-library Python tests around the injected controller/adapters. Hardware tests belong in a manual smoke checklist, not CI.
- Real-device acceptance: enumerate camera, start preview, press once, observe countdown, verify a readable JPEG, verify optional print, repeat capture, and exit cleanly.

## Out of Scope

- Cloud uploads, accounts, remote galleries, phone pairing, or network control.
- Filters, compositing, GIFs, video, burst capture, or multiple cameras.
- Web/mobile interfaces, custom OS/kernel/driver work, or automatic printer discovery.
- Guaranteed support for every OS release, sensor, display, or printer without a tested configuration.
- Production kiosk hardening, systemd autostart, enclosure/electrical design, or custom PCB work.
- A shutdown button as a required feature.
- Recreating every visual detail of the referenced project.

## Further Notes

- The local checkout is currently empty, so this is a greenfield implementation specification.
- The referenced project contains one Python file and no published dependency/setup contract. Its script uses `raspistill` and undocumented image assets/print commands.
- Raspberry Pi documents that Bookworm and later use `rpicam-*` names and that the legacy camera stack is unsupported; the implementation should explicitly prefer Picamera2.
- A later follow-up can add systemd autostart after the interactive application is reliable.
