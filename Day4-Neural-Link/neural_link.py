#!/usr/bin/python3
import sys
sys.path.append('/home/pi/MasterPi')
sys.path.append('/home/pi/MasterPi/masterpi_sdk/common_sdk')

from common.ros_robot_controller_sdk import Board
board = Board()
board.pwm_servo_set_position(0.5, [[1, 1800]])
import time
import signal
import common.sonar as Sonar
import common.mecanum as mecanum

# ?? Hardware ????????????????????????????????????????????
car = mecanum.MecanumChassis()
HWSONAR = Sonar.Sonar()

# ?? Constants ???????????????????????????????????????????
THRESHOLD_CM  = 30
FORWARD_POWER = 50
REVERSE_POWER = 60
BACKUP_TIME   = 1.0
PIVOT_TIME    = 0.65
LOOP_DELAY    = 0.05

running = True

def alert_obstacle():
    """Nishk bonus ? flash sonar LEDs red on obstacle detection."""
    HWSONAR.setPixelColor(0, (255, 0, 0))
    HWSONAR.setPixelColor(1, (255, 0, 0))
    time.sleep(0.2)
    HWSONAR.setPixelColor(0, (0, 0, 0))
    HWSONAR.setPixelColor(1, (0, 0, 0))

def evade():
    print("[OBSTACLE] Evading...")
    alert_obstacle()
    car.set_velocity(0, 90, 0)
    time.sleep(0.1)
    car.set_velocity(REVERSE_POWER, 270, 0)
    time.sleep(BACKUP_TIME)
    car.set_velocity(0, 90, 0)
    time.sleep(0.1)
    car.set_velocity(50, 90, -0.5)
    time.sleep(PIVOT_TIME)
    car.set_velocity(0, 90, 0)
    print("[OBSTACLE] Evasion complete. Resuming...")

def shutdown(signum, frame):
    global running
    running = False

signal.signal(signal.SIGINT, shutdown)

print("=== Neural Link Online ===")
print(f"Threshold: {THRESHOLD_CM}cm | Power: {FORWARD_POWER}%")
print("Press Ctrl+C to stop.\n")

try:
    while running:
        dist = HWSONAR.getDistance() / 10.0
        print(f"Distance: {dist:.1f} cm", end="\r")

        if dist > THRESHOLD_CM:
            car.set_velocity(FORWARD_POWER, 90, 0)
        else:
            evade()

        time.sleep(LOOP_DELAY)

finally:
    car.set_velocity(0, 90, 0)
    HWSONAR.setPixelColor(0, (0, 0, 0))
    HWSONAR.setPixelColor(1, (0, 0, 0))
    print("\n[SHUTDOWN] Neural Link offline.")
