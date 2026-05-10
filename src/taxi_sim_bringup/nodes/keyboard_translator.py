#!/usr/bin/env python
# keyboard_translator.py — Python 2.7 compatible
import sys
import tty
import termios
import rospy
from prius_msgs.msg import Control

THROTTLE_STEP = 0.1
STEER_STEP = 0.1
BRAKE_STEP = 0.2

MSG = """
=== Taxi Sim Keyboard Control ===
  W     : throttle up
  S     : brake
  A/D   : steer left / right
  F     : FORWARD gear
  R     : REVERSE gear
  N     : NEUTRAL
  SPACE : emergency brake
  Q     : quit
=================================
"""

class KeyboardTranslator:
    def __init__(self):
        rospy.init_node('keyboard_translator')
        self.pub = rospy.Publisher('prius', Control, queue_size=1)
        self.throttle    = 0.0
        self.brake       = 0.0
        self.steer       = 0.0
        self.shift_gears = Control.FORWARD
        self.rate = rospy.Rate(20)
        print(MSG)
        print("Current gear: FORWARD — press F to confirm then W to go!")

    def publish(self):
        cmd = Control()
        cmd.header.stamp = rospy.Time.now()
        cmd.throttle     = self.throttle
        cmd.brake        = self.brake
        cmd.steer        = self.steer
        cmd.shift_gears  = self.shift_gears
        self.pub.publish(cmd)

    def process_key(self, key):
        if key == 'w':
            self.throttle = min(1.0, self.throttle + THROTTLE_STEP)
            self.brake    = 0.0
        elif key == 's':
            self.brake    = min(1.0, self.brake + BRAKE_STEP)
            self.throttle = 0.0
        elif key == 'a':
            self.steer = max(-1.0, self.steer - STEER_STEP)
        elif key == 'd':
            self.steer = min(1.0, self.steer + STEER_STEP)
        elif key == 'f':
            self.shift_gears = Control.FORWARD
            self.throttle = 0.0
            self.brake    = 0.0
            print("Gear: FORWARD")
        elif key == 'r':
            self.shift_gears = Control.REVERSE
            self.throttle = 0.0
            self.brake    = 0.0
            print("Gear: REVERSE")
        elif key == 'n':
            self.shift_gears = Control.NEUTRAL
            self.throttle = 0.0
            print("Gear: NEUTRAL")
        elif key == ' ':
            self.throttle = 0.0
            self.brake    = 1.0
            self.steer    = 0.0
            print("EMERGENCY BRAKE")
        elif key == 'q':
            rospy.signal_shutdown("User quit")
            return

        # Decay steer toward center when not steering
        if key not in ('a', 'd'):
            self.steer = self.steer * 0.7
        if key not in ('w',):
            self.throttle = self.throttle * 0.8

    def run(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while not rospy.is_shutdown():
                key = sys.stdin.read(1)
                self.process_key(key)
                self.publish()
                self.rate.sleep()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == '__main__':
    KeyboardTranslator().run()