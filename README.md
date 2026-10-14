# Raspberry Pi Robotic Arm Controller (Python)

A compact Python project for controlling a **four-servo robotic arm** using a **Raspberry Pi 5**, a **PCA9685 PWM servo driver**, and Adafruit's `ServoKit` library.

This is a **clean reconstruction** of the original Python controller from my personal robotic-arm project, not a verbatim export of the earlier script. It focuses on the Python portion only; the later ESP32/C++ firmware is not included.

## Features

- Text commands to move the base, shoulder, elbow, and claw
- `open` and `close` claw shortcuts
- Configurable joint limits to prevent commands outside the specified range
- `--simulate` mode for trying the controller without hardware
- Unit tests using a simulated servo controller
- No movement on startup

## Hardware

- Raspberry Pi 5 with I2C enabled
- PCA9685 16-channel PWM servo driver (default address `0x40`)
- Four compatible servo motors and their robotic-arm mechanism
- **Separate, appropriately rated servo power supply**; shared ground with the Pi

### PCA9685 wiring (Raspberry Pi 40-pin header)

| PCA9685 pin | Raspberry Pi connection |
| --- | --- |
| VCC (logic) | 3.3 V (physical pin 1) |
| GND | GND (physical pin 6) |
| SDA | GPIO 2 / SDA (physical pin 3) |
| SCL | GPIO 3 / SCL (physical pin 5) |
| V+ (servo power) | External servo power supply, **not** Raspberry Pi 3.3 V |

Connect the external servo supply's ground to the common ground. Never power four servos from the Pi's 3.3 V rail. Size the external supply for your servos' current requirements.

The original project's PCA9685 channel mapping:

| Joint | Channel |
| --- | --- |
| Base | 1 |
| Shoulder | 2 |
| Elbow | 3 |
| Claw | 4 |

**Note:** Change the `CHANNELS` mapping if your hardware is wired differently.

## Setup on Raspberry Pi

1. Enable I2C with `sudo raspi-config` under **Interface Options > I2C** and reboot if needed.
2. Optionally verify the controller appears at address `0x40` with `i2cdetect -y 1` (install `i2c-tools` if needed).
3. Install the Python dependencies in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. **Before moving hardware**, adjust `LIMITS` in `robot_controller.py` to match your arm's real mechanical travel. The generic defaults (`0`–`180`) are **not** known-safe for your arm. Confirm the claw's `CLAW_OPEN` and `CLAW_CLOSED` angles too.
5. Run the controller:

```bash
python robot_controller.py
```

## Try it without hardware

```bash
python robot_controller.py --simulate
```

Example session:

```text
arm> base 90
arm> shoulder 80
arm> elbow 60
arm> open
arm> close
arm> quit
```

**Safety:** Servo commands can cause an immediate movement. Keep hands clear of pinch points, test one joint at a time, and start with a clear workspace. This demonstration does not include collision detection, velocity limiting, current sensing, or an emergency-stop circuit.

## Tests

The built-in `unittest` suite requires no extra packages or connected hardware:

```bash
python -m unittest discover -s tests -v
```

## Project scope

This repository intentionally contains **Python servo control only**. Voice recognition and the later ESP32/C++ version are not claimed as working features here. Those can be developed in separate projects.

## Portfolio context

Personal electronics and software project exploring Python control of physical hardware, I2C communication, input validation, and basic automated testing.
