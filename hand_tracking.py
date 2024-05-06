import cv2
import numpy as np
import pygame
import mediapipe as mp

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Initialize pygame for sound
pygame.init()

# Load drum sound
drum_sound = pygame.mixer.Sound('snare.mp3')
ride_sound = pygame.mixer.Sound('ride_sound.wav')

# Define the rectangle coordinates for drum and ride
drum_rect = (200, 400, 200, 200)
ride_rect = (500, 50, 200, 200)

# Flags to track if the sounds have been played
drum_sound_played = False
ride_sound_played = False

# Previous hand positions
prev_drum_hand_inside = False
prev_ride_hand_inside = False

# Function to check if hand is in the rectangle
def hand_in_rectangle(hand_x, hand_y, rect):
    rect_x, rect_y, rect_w, rect_h = rect
    return rect_x < hand_x < rect_x + rect_w and rect_y < hand_y < rect_y + rect_h

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Detect hand landmarks
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    # Reset the sound flags if no hands are detected within the rectangles
    drum_hand_inside = False
    ride_hand_inside = False
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the coordinates of the palm (average of all landmarks)
            height, width, _ = frame.shape
            palm_x = int(sum([landmark.x * width for landmark in hand_landmarks.landmark]) / 21)
            palm_y = int(sum([landmark.y * height for landmark in hand_landmarks.landmark]) / 21)

            # Draw hand landmarks on the frame
            for landmark in hand_landmarks.landmark:
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

            # Check if hand is in the drum rectangle and play the drum sound
            if hand_in_rectangle(palm_x, palm_y, drum_rect):
                drum_hand_inside = True
            # Check if hand is in the ride rectangle and play the ride sound
            if hand_in_rectangle(palm_x, palm_y, ride_rect):
                ride_hand_inside = True

    # Check if the hands have entered or exited the rectangles
    if drum_hand_inside and not prev_drum_hand_inside:
        drum_sound.play()
    elif not drum_hand_inside and prev_drum_hand_inside:
        drum_sound_played = False
    
    if ride_hand_inside and not prev_ride_hand_inside:
        ride_sound.play()
    elif not ride_hand_inside and prev_ride_hand_inside:
        ride_sound_played = False

    # Update previous hand positions
    prev_drum_hand_inside = drum_hand_inside
    prev_ride_hand_inside = ride_hand_inside

    # Add rectangles to frame
    cv2.rectangle(frame, (drum_rect[0], drum_rect[1]), (drum_rect[0] + drum_rect[2], drum_rect[1] + drum_rect[3]), (0, 255, 0), 2)
    cv2.rectangle(frame, (ride_rect[0], ride_rect[1]), (ride_rect[0] + ride_rect[2], ride_rect[1] + ride_rect[3]), (0, 255, 0), 2)

    cv2.imshow('Air Drum', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
