import cv2
import numpy as np
import pygame
import mediapipe as mp

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Initialize pygame for sound
pygame.init()

# Load drum sound
drum_sound = pygame.mixer.Sound('snare-112754.mp3')

# Define the rectangle coordinates
rect_x, rect_y, rect_w, rect_h = 200, 200, 200, 200

# Variables to keep track of sound state
sound_played = False

# Function to check if hand is in the rectangle
def hand_in_rectangle(hand_x, hand_y):
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
    hand_landmarks = None
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            break

    if hand_landmarks:
        # Get the coordinates of the palm (average of all landmarks)
        height, width, _ = frame.shape
        palm_x = int(sum([landmark.x * width for landmark in hand_landmarks.landmark]) / 21)
        palm_y = int(sum([landmark.y * height for landmark in hand_landmarks.landmark]) / 21)

        # Draw hand landmarks on the frame
        for landmark in hand_landmarks.landmark:
            cx, cy = int(landmark.x * width), int(landmark.y * height)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

        # Check if hand is in the rectangle
        if hand_in_rectangle(palm_x, palm_y) and not sound_played:
            drum_sound.play()
            sound_played = True
    else:
        sound_played = False

    # Add rectangle to frame
    cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h), (0, 255, 0), 2)

    cv2.imshow('Air Drum', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
