import cv2
import numpy as np
import pygame

# Initialize pygame for sound
pygame.init()

# Load drum sound
drum_sound = pygame.mixer.Sound('snare.mp3')

# Start video capture
cap = cv2.VideoCapture(0)

# Define the rectangle coordinates
rectangle = (200, 200, 200, 200)

# Initialize previous position
prev_pos = None

# Flag to track if drum sound is already played
sound_played = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't capture frame")
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find contours in the grayscale image
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through the contours
    for contour in contours:
        # Calculate the centroid of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            pos = (cx, cy)

            # Check if the centroid is inside the rectangle
            if rectangle[0] < cx < rectangle[0] + rectangle[2] and rectangle[1] < cy < rectangle[1] + rectangle[3]:
                # Play the drum sound if it's not already played
                if not sound_played:
                    drum_sound.play()
                    sound_played = True
            else:
                sound_played = False

            # Draw the centroid
            cv2.circle(frame, pos, 5, (0, 0, 255), -1)

            # Store the current position for next iteration
            prev_pos = pos

    # Draw rectangle on the frame
    cv2.rectangle(frame, (rectangle[0], rectangle[1]), (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3]), (0, 255, 0), 2)

    cv2.imshow('Drum Movement Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
