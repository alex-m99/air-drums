import cv2
import numpy as np
import pygame

from util import get_limits

# Initialize pygame for sound
pygame.init()

# Load sound effects
snare_sound = pygame.mixer.Sound('snare.mp3')
ride_sound = pygame.mixer.Sound('ride_sound.wav')

# Define rectangle coordinates at the bottom and top right of the screen
bottom_rectangle = [(200, 400), (400, 480)]
top_right_rectangle = [(440, 0), (640, 200)]

# Flags to track if the sounds have been played
snare_sound_played = False
ride_sound_played = False

# Blue color in BGR colorspace
green = [0, 255, 0]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=green)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Detect blue object
    bbox = cv2.boundingRect(mask)

    if bbox[2] > 0 and bbox[3] > 0:
        x, y, w, h = bbox

        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)

        # Check if the blue object hits the bottom rectangle
        if y + h >= bottom_rectangle[0][1]:
            if not snare_sound_played:
                snare_sound.play()
                snare_sound_played = True
        else:
            snare_sound_played = False

        # Check if any point of the bounding box is inside the top right rectangle
        points = [(x, y), (x+w, y), (x, y+h), (x+w, y+h)]
        for point in points:
            if top_right_rectangle[0][0] <= point[0] <= top_right_rectangle[1][0] and \
               top_right_rectangle[0][1] <= point[1] <= top_right_rectangle[1][1]:
                if not ride_sound_played:
                    ride_sound.play()
                    ride_sound_played = True
                break
        else:
            ride_sound_played = False

    # Draw rectangles on the frame
    frame = cv2.rectangle(frame, bottom_rectangle[0], bottom_rectangle[1], (0, 0, 255), 2)
    frame = cv2.rectangle(frame, top_right_rectangle[0], top_right_rectangle[1], (0, 0, 255), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
