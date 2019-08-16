import robot_controller as robo
import time


class Ev3Delegate(object):
    def __init__(self):
        self.robot = robo.Snatch3r()
        self.mqtt_client = None  # To be set later.

    def drive_inches(self, distance_inches, speed_sp):
        self.robot.drive_inches(distance_inches, speed_sp)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        self.robot.turn_degrees(degrees_to_turn, turn_speed_sp)

    def arm_calibration(self):
        self.robot.arm_calibration()

    def arm_up(self):
        self.robot.arm_up()

    def arm_down(self):
        self.robot.arm_down()

    def beep(self):
        self.robot.beep()

    def drive_to_wall(self):
        while True:
            self.robot.drive_forever()
            time.sleep(0.5)
            self.robot.distance_to_stop()

    def move_to_rel_pos(self, x, y):
        self.robot.drive_inches(x, 900)
        self.robot.turn_degrees(90, 900)
        self.robot.drive_inches(y, 900)

    def stop(self):
        self.robot.stop()

    def loop_forever(self):
        while self.robot.running:
            # do stuff
            time.sleep(0.01)
        if self.mqtt_client:
            self.mqtt_client.close()
        self.robot.shutdown()


class PcDelegate(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self):
        self.return_from_sensor = False

    def send_out(self, color_name):
        return color_name