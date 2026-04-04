#!/usr/bin/env python3
import sys
import time
sys.path.insert(0, '/home/pi/MasterPi/masterpi_sdk/common_sdk')
from common.ros_robot_controller_sdk import Board

board = Board()
print("Board initialized!")
time.sleep(1)

# Home position
print("Moving to home position...")
board.pwm_servo_set_position(1.0, [[1, 1500], [3, 500], [4, 2400], [5, 780], [6, 1500]])
time.sleep(2)

# Wave motion - 3 times
print("Starting wave motion...")
for i in range(3):
    # Wave up
    board.pwm_servo_set_position(0.5, [[4, 2000], [5, 580]])
    time.sleep(1)

    # Wave down
    board.pwm_servo_set_position(0.5, [[4, 2400], [5, 780]])
    time.sleep(1)

    print(f"Wave {i+1} complete!")

# Return home
print("Returning to home...")
board.pwm_servo_set_position(1.0, [[1, 1500], [3, 500], [4, 2400], [5, 780], [6, 1500]])
time.sleep(2)
print("Done!")
