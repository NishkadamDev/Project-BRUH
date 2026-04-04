#!/usr/bin/env python3
import cv2
import numpy as np

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    # Try other indexes
    for i in range(1, 10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            break

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

    # Clean up mask with blur
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours of green regions
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest green object
        largest = max(contours, key=cv2.contourArea)

        if cv2.contourArea(largest) > 500:  # Ignore tiny blobs
            # Get bounding circle
            ((x, y), radius) = cv2.minEnclosingCircle(largest)

            # Draw red circle around it
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 3)

            # Label it
            cv2.putText(frame, "GREEN DETECTED", (int(x) - 80, int(y) - int(radius) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Show live feed
    cv2.imshow("MasterPi Vision", frame)
    cv2.imshow("Green Mask", mask)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Done!")
