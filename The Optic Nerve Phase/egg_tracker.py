#!/usr/bin/env python3
import sys
sys.path.append('/home/pi/MasterPi/')
import cv2
import numpy as np
import time

# Kill any process holding the camera
import os
os.system("sudo fuser -k /dev/video0 2>/dev/null")
time.sleep(1)

sys.path.insert(0, '/home/pi/MasterPi/masterpi_sdk/common_sdk')
from common.ros_robot_controller_sdk import Board

board = Board()
time.sleep(1)

# Camera setup
cap = cv2.VideoCapture(-1)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_SATURATION, 40)

if not cap.isOpened():
    print("Failed to open camera!")
    exit()

FRAME_W = 640
CENTER_X = FRAME_W // 2
DEAD_ZONE = 60
SPEED = 40

print("Egg Tracker started! Press Q to quit.")

def strafe_left():
    board.set_motor_duty([[1, -SPEED], [2, -SPEED], [3, SPEED], [4, SPEED]])

def strafe_right():
    board.set_motor_duty([[1, SPEED], [2, SPEED], [3, -SPEED], [4, -SPEED]])

def stop():
    board.set_motor_duty([[1, 0], [2, 0], [3, 0], [4, 0]])

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([60, 200, 5])
        upper_green = np.array([90, 255, 80])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) > 500:
                ((x, y), radius) = cv2.minEnclosingCircle(largest)
                obj_x = int(x)
                offset = obj_x - CENTER_X

                cv2.circle(frame, (obj_x, int(y)), int(radius), (0, 0, 255), 3)
                cv2.line(frame, (CENTER_X, 0), (CENTER_X, frame.shape[0]), (255, 255, 0), 2)

                if abs(offset) < DEAD_ZONE:
                    stop()
                    status = "CENTERED - STOPPED"
                elif offset < 0:
                    # Object is LEFT of center - strafe right to center it
                    strafe_right()
                    status = f"STRAFING RIGHT (offset: {offset}px)"
                else:
                    # Object is RIGHT of center - strafe left to center it
                    strafe_left()
                    status = f"STRAFING LEFT (offset: {offset}px)"

                cv2.putText(frame, status, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f"Center X: {obj_x}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            else:
                stop()
        else:
            stop()
            cv2.putText(frame, "NO TARGET", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow("Egg Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    stop()
    cap.release()
    cv2.destroyAllWindows()
    print("Stopped!")
