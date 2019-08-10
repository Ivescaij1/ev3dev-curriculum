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

    def drive_inches(self, distance_inches, speed_sp):
        """ Drive the robert a fixed number of inches with constant speed
        :param distance_inches: inches
        :param speed_sp: degree per seconds
        :return: None
        """
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        assert left_motor.connected
        assert right_motor.connected

        if speed_sp != 0 and distance_inches != 0:
            position_sp = distance_inches * 90

            left_motor.run_to_rel_pos(position_sp=position_sp, speed_sp=speed_sp, stop_action="brake")
            right_motor.run_to_rel_pos(position_sp=position_sp, speed_sp=speed_sp, stop_action="brake")

            left_motor.wait_while("running")
            right_motor.wait_while("running")

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """ Turns a set of degrees, positive is left turn
        :param degrees_to_turn: degrees
        :param turn_speed_sp: degrees/seconds
        :return: None
        """
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        # assert left_motor.connected
        # assert right_motor.connected

        if turn_speed_sp != 0 and degrees_to_turn != 0:
            position_sp = degrees_to_turn
            speed_sp = turn_speed_sp

            left_motor.run_to_rel_pos(position_sp=-position_sp, speed_sp=speed_sp, stop_action="brake")
            right_motor.run_to_rel_pos(position_sp=position_sp, speed_sp=speed_sp, stop_action="brake")

            left_motor.wait_while("running")
            right_motor.wait_while("running")

    # def arm_up(self):
    #
    #
    # def arm_down(self):
    #
    #
    # def main_sensor(self):
    #
    #
    # def color_sensor(self):