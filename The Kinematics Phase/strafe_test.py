#!/usr/bin/env python3
import sys
import time

sys.path.insert(0, '/home/pi/MasterPi/masterpi_sdk/common_sdk')
from common.ros_robot_controller_sdk import Board

board = Board()
print("Board initialized!")
time.sleep(1)

SPEED = 45

print("Strafing RIGHT for 2 seconds...")
board.set_motor_duty([[1, SPEED], [2, SPEED], [3, -SPEED], [4, -SPEED]])
time.sleep(2)

print("Stopping...")
board.set_motor_duty([[1, 0], [2, 0], [3, 0], [4, 0]])
time.sleep(1)

print("Strafing LEFT for 2 seconds...")
board.set_motor_duty([[1, -SPEED], [2, -SPEED], [3, SPEED], [4, SPEED]])
time.sleep(2)

print("Stopping...")
board.set_motor_duty([[1, 0], [2, 0], [3, 0], [4, 0]])

print("Done!")
