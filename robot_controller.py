"""Interactive Python controller for a Raspberry Pi robotic arm.

Hardware: Raspberry Pi, PCA9685 (I2C address 0x40), and four servos.
Run with --simulate to try the commands without attached hardware.
"""

import argparse

# Channel assignments from the original Raspberry Pi build.
CHANNELS = {
    "base": 1,
    "shoulder": 2,
    "elbow": 3,
    "claw": 4,
}

# EDIT THESE before use to match your arm's mechanical limits.
# The default 0–180 range is the generic servo range, NOT a verified safe
# range for your particular printed arm or linkages.
LIMITS = {name: (0, 180) for name in CHANNELS}

# Values used while experimenting with the original claw.
CLAW_OPEN = 90
CLAW_CLOSED = 10


class SimulatedServo:
    def __init__(self):
        self.angle = None


class SimulatedKit:
    """Minimal replacement for ServoKit to practice commands on any PC."""

    def __init__(self):
        self.servo = [SimulatedServo() for _ in range(16)]


def connect(simulate=False):
    if simulate:
        print("SIMULATION: no hardware will move.")
        return SimulatedKit()

    try:
        from adafruit_servokit import ServoKit
    except ImportError as exc:
        raise RuntimeError(
            "Install dependencies using: pip install -r requirements.txt"
        ) from exc

    return ServoKit(channels=16, address=0x40)


def move_servo(kit, joint, angle):
    """Set a joint angle only after validating the configured limits."""
    if joint not in CHANNELS:
        raise ValueError(f"Unknown joint: {joint}")
    low, high = LIMITS[joint]
    if not low <= angle <= high:
        raise ValueError(f"{joint} angle must be between {low} and {high} degrees")

    # On real hardware, a command can cause immediate movement.
    kit.servo[CHANNELS[joint]].angle = angle
    print(f"{joint.capitalize()} -> {angle}° (PCA9685 channel {CHANNELS[joint]})")


def show_help():
    print("\nCommands:\n"
          "  base 90       Move base to 90 degrees\n"
          "  shoulder 90   Move shoulder to 90 degrees\n"
          "  elbow 90      Move elbow to 90 degrees\n"
          "  claw 45       Move claw to 45 degrees\n"
          "  open          Open claw (configured angle)\n"
          "  close         Close claw (configured angle)\n"
          "  help          Show commands\n"
          "  quit          Exit\n")


def handle_command(kit, command):
    """Execute a single text command. Return False to exit the loop."""
    parts = command.strip().lower().split()
    if not parts:
        return True
    if parts[0] in {"quit", "exit"} and len(parts) == 1:
        return False
    if parts == ["help"]:
        show_help()
        return True

    try:
        if parts == ["open"]:
            move_servo(kit, "claw", CLAW_OPEN)
        elif parts == ["close"]:
            move_servo(kit, "claw", CLAW_CLOSED)
        elif len(parts) == 2 and parts[0] in CHANNELS:
            move_servo(kit, parts[0], int(parts[1]))
        else:
            print("Unrecognized command. Type 'help' for examples.")
    except ValueError as exc:
        print(f"Invalid command: {exc}")
    except OSError as exc:
        print(f"Hardware communication error: {exc}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Control a four-servo Raspberry Pi arm")
    parser.add_argument(
        "--simulate", action="store_true", help="Practice without a Raspberry Pi or servos"
    )
    args = parser.parse_args()

    try:
        kit = connect(args.simulate)
    except (RuntimeError, OSError, ValueError) as exc:
        parser.exit(1, f"Unable to connect to servo controller: {exc}\n")

    print("Python Robotic Arm Controller")
    print("WARNING: Set safe joint limits and clear the workspace before moving servos.")
    print("No joints are moved automatically when the controller starts.")
    show_help()
    try:
        while True:
            if not handle_command(kit, input("arm> ")):
                break
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")


if __name__ == "__main__":
    main()
