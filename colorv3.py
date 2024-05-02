import cv2
import numpy as np
import pygame
from drum import Drum

# Initialize pygame for sound
pygame.init()

#Instantiate drum objects
snare = Drum("snare", (210, 300), (400, 480), "snare.mp3")
hihat = Drum("hihat", (440, 250), (640, 400), "hihat.mp3")
kick = Drum("kick", (0, 300), (200, 480), "kick.mp3")
#ride = Drum("ride", (440, 0), (640, 100), "ride_sound.wav")
crash = Drum("crash", (0, 0), (400, 90), "crash.mp3")

drums = [snare, hihat, crash, kick]

cap = cv2.VideoCapture(0)

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
        velocity = np.sqrt((x - prev_x)**2 + (y - prev_y)**2)
        velocities.append(velocity)

    # Update previous circle positions
    prev_green_circles = green_circles.copy()

   # print(velocities)

    # Draw green circles and their velocities
    for circle, velocity in zip(green_circles, velocities):
        (x, y), radius = circle
        cv2.circle(frame, (int(x), int(y)), radius, (0, 255, 0), 2)
        cv2.putText(frame, f"Velocity: {velocity:.2f}", (int(x - radius), int(y + radius + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    
    # Check for each drum if there is a green circle curently in it and set hasCircle accordingly
    for drum in drums:
        for circle, velocity in zip(green_circles, velocities):
            (x, y), radius = circle
            # if drum.getTopLeft()[0] <= x + radius <= drum.getBottomRight()[0] and \
            #    drum.getTopLeft()[1] <= y + radius <= drum.getBottomRight()[1]:
            #        drum.setHasCircle(True) 
            #        break
            if (drum.getName() == "snare" or drum.getName() == "hihat") and drum.getTopLeft()[0] <= x <= drum.getBottomRight()[0] and \
                y + radius >= drum.getTopLeft()[1]:
                    drum.setHasCircle(True)
                    drum.setVelocity(velocity)
                    break
            elif drum.getTopLeft()[0] <= x <= drum.getBottomRight()[0] and \
                drum.getTopLeft()[1] <= y <= drum.getBottomRight()[1]:
                    drum.setHasCircle(True) 
                    drum.setVelocity(velocity)
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
            #if drum.getVelocity() > 40:
            drum.playSound()

    # Draw rectangles on the frame
    for drum in drums:
        frame = cv2.rectangle(frame, drum.getTopLeft(), drum.getBottomRight(), (0, 0, 255), 2)
        cv2.putText(frame, f"Velocity: {drum.getVelocity():.2f}", (drum.getTopLeft()[0], drum.getTopLeft()[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
