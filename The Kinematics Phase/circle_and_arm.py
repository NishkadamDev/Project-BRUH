#!/usr/bin/env python3
import sys
import time
import threading

sys.path.insert(0, '/home/pi/MasterPi/masterpi_sdk/common_sdk')
from common.ros_robot_controller_sdk import Board

board = Board()
print("Board initialized!")
time.sleep(1)

running = True

def move_chassis():
    """Moves chassis in a circle by spinning one side faster"""
    print("Chassis thread started...")
    while running:
        # Circle right - left motors faster than right
        board.set_motor_duty([[1, 60], [2, 60], [3, 30], [4, 30]])
        time.sleep(0.05)  # Small sleep prevents stuttering

def move_arm():
    """Waves arm up and down continuously"""
    print("Arm thread started...")
    while running:
        # Wave up
        board.pwm_servo_set_position(0.8, [[4, 2000], [5, 580]])
        time.sleep(1)
        # Wave down
        board.pwm_servo_set_position(0.8, [[4, 2400], [5, 780]])
        time.sleep(1)

# Start both threads
chassis_thread = threading.Thread(target=move_chassis)
arm_thread = threading.Thread(target=move_arm)

chassis_thread.start()
arm_thread.start()

# Run for 6 seconds
print("Running for 6 seconds...")
time.sleep(6)

# Stop everything
running = False
print("Stopping...")
board.set_motor_duty([[1, 0], [2, 0], [3, 0], [4, 0]])
board.pwm_servo_set_position(1.0, [[1, 1500], [3, 500], [4, 2400], [5, 780], [6, 1500]])

chassis_thread.join()
arm_thread.join()
print("Done!")
