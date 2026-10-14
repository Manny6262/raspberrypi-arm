"""Tests run without Raspberry Pi hardware or third-party libraries."""

import contextlib
import io
import unittest

from robot_controller import (
    CHANNELS,
    CLAW_CLOSED,
    CLAW_OPEN,
    SimulatedKit,
    handle_command,
    move_servo,
)


class RobotControllerTests(unittest.TestCase):
    def setUp(self):
        self.kit = SimulatedKit()

    def test_base_move(self):
        with contextlib.redirect_stdout(io.StringIO()):
            move_servo(self.kit, "base", 75)
        self.assertEqual(self.kit.servo[CHANNELS["base"]].angle, 75)

    def test_invalid_angle_is_rejected(self):
        with self.assertRaises(ValueError):
            move_servo(self.kit, "shoulder", 200)

    def test_unknown_joint_is_rejected(self):
        with self.assertRaises(ValueError):
            move_servo(self.kit, "wrist", 90)

    def test_claw_commands(self):
        with contextlib.redirect_stdout(io.StringIO()):
            handle_command(self.kit, "open")
        self.assertEqual(self.kit.servo[CHANNELS["claw"]].angle, CLAW_OPEN)
        with contextlib.redirect_stdout(io.StringIO()):
            handle_command(self.kit, "close")
        self.assertEqual(self.kit.servo[CHANNELS["claw"]].angle, CLAW_CLOSED)

    def test_quit(self):
        self.assertFalse(handle_command(self.kit, "quit"))

    def test_unrecognized_input_does_not_move_arm(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(handle_command(self.kit, "base not-a-number"))
        self.assertIsNone(self.kit.servo[CHANNELS["base"]].angle)


if __name__ == "__main__":
    unittest.main()
