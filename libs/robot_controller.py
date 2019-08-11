"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

# TODO: Implement the Snatch3r class as needed when working the sandox exercises
import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        self.running = True
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()

    def drive_inches(self, distance_inches, speed_sp):
        """ Drive the robert a fixed number of inches with constant speed
        :param distance_inches: inches
        :param speed_sp: degree per seconds
        :return: None
        """
        assert self.left_motor.connected
        assert self.right_motor.connected

        while True:
            if speed_sp == 0 or distance_inches == 0:
                break
            position_sp = distance_inches * 90

            self.left_motor.run_to_rel_pos(position_sp=position_sp, speed_sp=speed_sp, stop_action="brake")
            self.right_motor.run_to_rel_pos(position_sp=position_sp, speed_sp=speed_sp, stop_action="brake")

            self.left_motor.wait_while("running")
            self.right_motor.wait_while("running")

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """ Turns a set of degrees, positive is left turn
        :param degrees_to_turn: degrees
        :param turn_speed_sp: degrees/seconds
        :return: None
        """
        assert self.left_motor.connected
        assert self.right_motor.connected

        while True:
            if degrees_to_turn == 0 or turn_speed_sp == 0:
                break
            position_sp = degrees_to_turn
            speed_sp = turn_speed_sp

            self.left_motor.run_to_rel_pos(position_sp=-position_sp, speed_sp=speed_sp, stop_action="brake")
            self.right_motor.run_to_rel_pos(position_sp=position_sp, speed_sp=speed_sp, stop_action="brake")

            self.left_motor.wait_while("running")
            self.right_motor.wait_while("running")

    def arm_calibration(self):
        """
        Runs the arm up until the touch sensor is hit then back to the bottom again, beeping at both locations.
        Once back at in the bottom position, gripper open, set the absolute encoder position to 0.  You are calibrated!
        The Snatch3r arm needs to move 14.2 revolutions to travel from the touch sensor to the open position.
        """
        assert self.arm_motor.connected
        assert self.touch_sensor.connected

        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while("running")
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0

    def arm_up(self):
        """
        Moves the Snatch3r arm to the up position.
        """
        assert self.arm_motor.connected
        assert self.touch_sensor.connected

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=arm_revolutions_for_full_range, speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):
        """
        Moves the Snatch3r arm to the down position.
        """
        assert self.arm_motor.connected
        assert self.touch_sensor.connected

        self.arm_motor.run_to_abs_pos(position_sp=0)
        self.arm_motor.wait_while("running")  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()
    #
    #
    # def main_sensor(self):
    #
    #
    # def color_sensor(self):