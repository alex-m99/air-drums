import cv2
import numpy as np
import pygame
from drum import Drum

# Initialize pygame for sound
pygame.init()

#Instantiate drum objects
snare = Drum("snare", (200, 400), (400, 480), "snare.mp3")
ride = Drum("ride", (440, 0), (640, 200), "ride_sound.wav")
drums = [snare, ride]

cap = cv2.VideoCapture(0)

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
    
    # Check for each drum if there is a green circle curently in it and set hasCircle accordingly
    for drum in drums:
        for circle in green_circles:
            (x, y), radius = circle
            if drum.getTopLeft()[0] <= x <= drum.getBottomRight()[0] and \
               drum.getTopLeft()[1] <= y <= drum.getBottomRight()[1]:
                   drum.setHasCircle(True) 
                   break
            else:
                drum.setHasCircle(False)
            
    # Check each drum's previous state and update the new state for each case
    for drum in drums:
        if drum.getState() == 0 and drum.getHasCircle():
            drum.setState(1) #circle just got in
        elif drum.getState() == 0 and not drum.getHasCircle():
            drum.setState(0) # circle is out
        elif drum.getState() == 1 and drum.getHasCircle():
            drum.setState(2) # stayed in the rectangle
        elif drum.getState() == 1 and not drum.getHasCircle():
            drum.setState(0) # got out of the rectangle
        elif drum.getState() == 2 and drum.getHasCircle():
            drum.setState(2) # stayed in the rectangle
        elif drum.getState() == 2 and not drum.getHasCircle():
            drum.setState(0) # got out of the rectangle
    
     # Check which drums have a state of 1 and play the sound for them
    for drum in drums:
        if drum.getState() == 1:
            drum.playSound()

    # Draw rectangles on the frame
    for drum in drums:
        frame = cv2.rectangle(frame, drum.getTopLeft(), drum.getBottomRight(), (0, 0, 255), 2)

    print(ride.getState())

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
