#!/usr/bin/env python
# -*- coding: utf-8 -*-
# keyboard_translator.py
# Subscribes to /keyboard_cmd (String) and translates to prius_msgs/Control
# Send commands via: rostopic pub /keyboard_cmd std_msgs/String "data: 'w'"

import rospy
from std_msgs.msg import String
from prius_msgs.msg import Control

THROTTLE_STEP = 0.15
STEER_STEP    = 0.15
BRAKE_STEP    = 0.3

class KeyboardTranslator:
    def __init__(self):
        rospy.init_node('keyboard_translator')
        self.pub = rospy.Publisher('prius', Control, queue_size=1)
        self.sub = rospy.Subscriber('/keyboard_cmd', String, self.callback)

        self.throttle    = 0.0
        self.brake       = 0.0
        self.steer       = 0.0
        self.shift_gears = Control.FORWARD

        # Publish at 20hz
        self.timer = rospy.Timer(rospy.Duration(0.05), self.publish)

        rospy.loginfo("=== Keyboard Translator Ready ===")
        rospy.loginfo("Send commands to /keyboard_cmd topic:")
        rospy.loginfo("  w=throttle s=brake a=left d=right")
        rospy.loginfo("  f=forward r=reverse n=neutral space=e-brake")
        rospy.loginfo("Example: rostopic pub /keyboard_cmd std_msgs/String \"data: 'w'\"")

    def publish(self, event=None):
        cmd = Control()
        cmd.header.stamp = rospy.Time.now()
        cmd.throttle     = self.throttle
        cmd.brake        = self.brake
        cmd.steer        = self.steer
        cmd.shift_gears  = self.shift_gears
        self.pub.publish(cmd)

        # Decay values over time for smooth stop
        self.throttle = self.throttle * 0.9
        self.steer    = self.steer    * 0.8
        self.brake    = self.brake    * 0.9

    def callback(self, msg):
        key = msg.data.strip().lower()
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
            rospy.loginfo("Gear: FORWARD")
        elif key == 'r':
            self.shift_gears = Control.REVERSE
            self.throttle = 0.0
            self.brake    = 0.0
            rospy.loginfo("Gear: REVERSE")
        elif key == 'n':
            self.shift_gears = Control.NEUTRAL
            self.throttle = 0.0
            rospy.loginfo("Gear: NEUTRAL")
        elif key == ' ' or key == 'space':
            self.throttle = 0.0
            self.brake    = 1.0
            self.steer    = 0.0
            rospy.loginfo("EMERGENCY BRAKE")

if __name__ == '__main__':
    KeyboardTranslator().run() if hasattr(KeyboardTranslator(), 'run') else rospy.spin()