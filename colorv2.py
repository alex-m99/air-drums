import cv2
import numpy as np
import pygame
from circle import Circle

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

cap = cv2.VideoCapture(0)
#is_in_bottom_rectangle = False
#is_in_top_right_rectangle = False


state = 0
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

            circle = Circle(center, radius)

            green_circles.append(circle)
    
    
    # Check green circles for sound and position
    # for circle in green_circles:
    #     x, y = circle.getCenter()
    #     #points = [(x,y), (x + radius,y), (x-radius, y), (x,  y+radius), (x, y-radius)]
    #     # Check if the green circle is in the bottom  rectangle
    #     # for point in points:
    #     #     if bottom_rectangle[0][0] <= point[0] <= bottom_rectangle[1][0] and \
    #     #     bottom_rectangle[0][1] <= point[1] <= bottom_rectangle[1][1]:
    #     #         if not ride_sound_played:
    #     #             snare_sound.play()
    #     #             snare_sound_played = True
    #     # else:
    #     #     snare_sound_played= False

    #     # Check if the green circle is in the top right rectangle
    #     if top_right_rectangle[0][0] <= x <= top_right_rectangle[1][0] and \
    #        top_right_rectangle[0][1] <= y <= top_right_rectangle[1][1]:
    #         if state == 0:
    #             state = 1
    #         elif state == 1:
    #             state = 2
    #     else:
    #         state = 0

    #Check each rectangle for any circles

    for rectangle in rectangles:
        for circle in green_circles:
            x, y = circle.getCenter()

            if rectangle[0][0] <= x <= rectangle[1][0] and \
            rectangle[0][1] <= y <= trectangle[1][1] and not played:
                stare_cerc = 1
                
            else:
                stare_cerc = 0 # afara

    for rectangle in recrangle
        for circle in green_circles:
            x, y = circle.getCenter()

            
    if state == 1:
        ride_sound.play()
    
    print(state)
    # for circle in green_circles:
    #     print("Is in ride: ", circle.getIsInRideRectangle())
    #     #print("Is set Played: ", circle.getPlayedRideRectangle())
    #     print("\n")
    #     if circle.getIsInRideRectangle() and circle.getPlayedRideRectangle() == False:
    #         ride_sound.play()
    #         circle.setIsInRideRectangle(True)
    #         circle.setPlayedRideRectangle(True)
    #         #print("Is set Played: ", circle.getPlayedRideRectangle())

    #     elif circle.getIsInRideRectangle() and circle.getPlayedRideRectangle():
    #         print("AAAAAAAAAAAAAAAAAAAAAA")
    #         circle.setIsInRideRectangle(True)
    #         circle.setPlayedRideRectangle(True)
    #     elif not circle.getIsInRideRectangle():
    #         circle.setIsInRideRectangle(False)
    #         circle.setPlayedRideRectangle(False)


    # Draw rectangles on the frame
    frame = cv2.rectangle(frame, bottom_rectangle[0], bottom_rectangle[1], (0, 0, 255), 2)
    frame = cv2.rectangle(frame, top_right_rectangle[0], top_right_rectangle[1], (0, 0, 255), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
