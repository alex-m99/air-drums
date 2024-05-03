import cv2
import numpy as np
import pygame
from drum import Drum
import ctypes

# Initialize pygame for sound
pygame.init()

snare_img = cv2.imread("snare.png", -1)

# Instantiate drum objects
snare = Drum("snare", (210, 300), (400, 480), "snare.mp3", snare_img)
hihat = Drum("hihat", (440, 250), (640, 400), "hihat.mp3", snare_img)
kick = Drum("kick", (0, 300), (200, 480), "kick.mp3", snare_img)
# ride = Drum("ride", (440, 0), (640, 100), "ride_sound.wav")
crash = Drum("crash", (0, 0), (400, 90), "crash.mp3", snare_img)

drums = [snare, hihat, kick]

cap = cv2.VideoCapture(0)

# Create the OpenCV window in fullscreen mode
cv2.namedWindow('web cam', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('web cam', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Initialize variables to store previous circle positions
prev_green_circles = []

while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper ranges for green color in HSV
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    # Threshold the HSV image to get only green color
    mask_green = cv2.inRange(hsvImage, lower_green, upper_green)

    # Find contours for green circles
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Process green circles
    green_circles = []
    for contour in contours_green:
        area = cv2.contourArea(contour)
        if area > 500:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)

            # Draw the circle on the frame
            cv2.circle(frame, center, radius, (0, 255, 0), 2)

            circle = (center, radius)

            green_circles.append(circle)

    # Calculate velocity for each green circle
    velocities = []
    for circle, prev_circle in zip(green_circles, prev_green_circles):
        (x, y), _ = circle
        (prev_x, prev_y), _ = prev_circle
        velocity = np.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)
        velocities.append(velocity)

    # Calculate direction for each green circle
    directions = []
    for circle, prev_circle in zip(green_circles, prev_green_circles):
        (x, y), _ = circle
        (prev_x, prev_y), _ = prev_circle
        #dx = x - prev_x
        dy = y - prev_y
        direction = "None"
        if dy > 0:
            direction = "Down"
        elif dy < 0:
            direction = "Up"
        # if abs(dx) > abs(dy):
        #     if dx > 0:
        #         direction = "Right"
        #     elif dx < 0:
        #         direction = "Left"
        # else:
        #     if dy > 0:
        #         direction = "Down"
        #     elif dy < 0:
        #         direction = "Up"
        directions.append(direction)

    # Update previous circle positions
    prev_green_circles = green_circles.copy()

    # Draw green circles and their velocities
    for circle, velocity in zip(green_circles, velocities):
        (x, y), radius = circle
        cv2.circle(frame, (int(x), int(y)), radius, (0, 255, 0), 2)
        cv2.putText(frame, f"Velocity: {velocity:.2f}", (int(x - radius), int(y + radius + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"Direction: {direction}", (int(x - radius), int(y + radius + 40)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Check for each drum if there is a green circle currently in it and set hasCircle accordingly
    for drum in drums:
        for circle, velocity, direction in zip(green_circles, velocities, directions):
            (x, y), radius = circle
            if drum.getTopLeft()[0] <= x <= drum.getBottomRight()[0] and \
                drum.getTopLeft()[1] <= y - radius <= drum.getBottomRight()[1]:
                drum.setHasCircle(True)
                #drum.setHasHit(False)
                drum.setVelocity(velocity)
                drum.setDirection(direction)
                break

            else:
                drum.setHasCircle(False)

            # elif drum.getState() == 1 and  drum.getTopLeft()[0] <= x <= drum.getBottomRight()[0] and \
            #     drum.getTopLeft()[1] + (drum.getBottomRight()[1] - drum.getTopLeft()[1])/2 <= y <= drum.getBottomRight()[1]:
            #     drum.setHasHit(True)
            # else:
            #     drum.setHasCircle(False)
            #     drum.setHasHit(Fal)

    # Check each drum's previous state and update the new state for each case
    for drum in drums:

        if not drum.getHasCircle():
            drum.setState(0)
        else:
            if drum.getState() == 0:
                drum.setState(1)  # circle just got in
            elif drum.getState() == 1:
                drum.setState(2)  # stayed in the rectangle and hasn't hit
            elif drum.getState() == 2:
                drum.setState(2)  # stayed in the rectangle

    # Check which drums have a state of 1 and play the sound for them
    for drum in drums:
        if drum.getState() == 1:
            if drum.getVelocity() > 10:
                if drum.getDirection() == "Down":
                    drum.playSound()

    # Draw rectangles on the frame
    # for drum in drums:
    #     frame = cv2.rectangle(frame, drum.getTopLeft(), drum.getBottomRight(), (0, 0, 255), 2)
    #     cv2.putText(frame, f"Velocity: {drum.getVelocity():.2f}", (drum.getTopLeft()[0], drum.getTopLeft()[1] - 20),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    #     cv2.putText(frame, f"Direction: {drum.getDirection()}", (drum.getTopLeft()[0], drum.getTopLeft()[1] - 10),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    
        # Overlay drum images onto the frame
    for drum in drums:
        drum_img = drum.getImage(drum.getBottomRight()[0] - drum.getTopLeft()[0], drum.getBottomRight()[1] - drum.getTopLeft()[1])
        if drum_img is not None:
            top_left = drum.getTopLeft()
            bottom_right = drum.getBottomRight()
            drum_h, drum_w, _ = drum_img.shape
            y1, y2 = top_left[1], top_left[1] + drum_h
            x1, x2 = top_left[0], top_left[0] + drum_w

            # Overlay the drum image onto the frame
            alpha = 0.5
            drum_area = frame[y1:y2, x1:x2]
            drum_area_resized = cv2.resize(drum_img, (drum_area.shape[1], drum_area.shape[0]))
            blended = cv2.addWeighted(drum_area_resized, alpha, drum_area, 1 - alpha, 0)
            frame[y1:y2, x1:x2] = blended


    cv2.imshow('web cam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
