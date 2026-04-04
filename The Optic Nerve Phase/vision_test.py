#!/usr/bin/env python3
import sys
sys.path.append('/home/pi/MasterPi/')
import cv2
import numpy as np
import os
os.system("sudo fuser -k /dev/video0 2>/dev/null")
time.sleep(1)

# Open camera using Hiwonder's method
cap = cv2.VideoCapture(-1)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_SATURATION, 40)

if not cap.isOpened():
    print("Failed to open camera!")
    exit()

print("Camera opened! Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define bright green range in HSV
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])

    # Create mask for green pixels
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 500:
            ((x, y), radius) = cv2.minEnclosingCircle(largest)
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 3)
            cv2.putText(frame, "GREEN DETECTED", (int(x) - 80, int(y) - int(radius) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imshow("MasterPi Vision", frame)
    cv2.imshow("Green Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Done!")
