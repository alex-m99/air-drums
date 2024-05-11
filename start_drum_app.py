import cv2
import numpy as np
from drum import Drum

mouse_clicked = False

# Define the drum app function
def start_drum_app(snare_img_path, kick_img_path, rythm_img_path, accent_img_path, mode_name):
    global mouse_clicked
    snare_img = cv2.imread(snare_img_path, -1)
    kick_img = cv2.imread(kick_img_path, -1)
    rythm_img = cv2.imread(rythm_img_path, -1)
    accent_img = cv2.imread(accent_img_path, -1)

    # Instantiate drum objects
    snare = Drum("snare", (210, 300), (400, 480), snare_img, snare_img_path)
    kick = Drum("kick", (0, 0), (0, 0), kick_img, kick_img_path)
    rithm = Drum("rithm", (440, 180), (640, 330), rythm_img, rythm_img_path)
    accent = Drum("accent", (0, 180), (200, 330), accent_img, accent_img_path)

    drums = [snare, rithm, accent]

    cap = cv2.VideoCapture(0)

    # Create the OpenCV window in fullscreen mode
    cv2.namedWindow('web cam', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('web cam', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Initialize variables to store previous circle positions
    prev_green_circles = []

    # Initialize variables for mouse click event
    

    def mouse_callback(event, x, y, flags, param):
        #print (event)
        global mouse_clicked
        if event == cv2.EVENT_RBUTTONDOWN:
            mouse_clicked = True

    cv2.setMouseCallback('web cam', mouse_callback)
    
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
            dy = y - prev_y
            direction = "None"
            if dy > 0:
                direction = "Down"
            elif dy < 0:
                direction = "Up"
            directions.append(direction)

        # Update previous circle positions
        prev_green_circles = green_circles.copy()

        # Check for each drum if there is a green circle currently in it and set hasCircle accordingly
        for drum in drums:
            for circle, velocity, direction in zip(green_circles, velocities, directions):
                (x, y), radius = circle
                if drum.getTopLeft()[0] <= x <= drum.getBottomRight()[0] and \
                    (drum.getTopLeft()[1] <= y + radius or \
                    drum.getTopLeft()[1] <= y - radius):
                    drum.setHasCircle(True)
                    drum.setVelocity(velocity)
                    drum.setDirection(direction)
                    break
                else:
                    drum.setHasCircle(False)

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
            if drum.getName() == "crash" and drum.getState() == 1: 
                drum.playSound()
            elif drum.getState() == 1 and drum.getDirection() == "Down" and drum.getVelocity() > 15:
                drum.playSound()
        
        #print('Mouse click in loop: ', mouse_clicked)

        # Check if mouse is clicked and play bass drum sound
        if mouse_clicked:
            kick.playSound()
            mouse_clicked = False

        if mode_name == 'Transparent mode':
            # Overlay transparent drum images onto the frame
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

        else:
            #Overlay drum images onto the frame after aplying mask
            for drum in drums:
                drum_img = drum.getImage(drum.getBottomRight()[0] - drum.getTopLeft()[0], drum.getBottomRight()[1] - drum.getTopLeft()[1])
                if drum_img is not None:
                    top_left = drum.getTopLeft()
                    bottom_right = drum.getBottomRight()
                    drum_h, drum_w, _ = drum_img.shape

                    # Convert to grayscale
                    gray = cv2.cvtColor(drum_img, cv2.COLOR_BGR2GRAY)

                    # Threshold to extract non-white areas
                    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

                    # Invert mask
                    mask = cv2.bitwise_not(mask)

                    # Apply mask to drum image
                    drum_img = cv2.bitwise_and(drum_img, drum_img, mask=mask)

                    # Get the region of interest on the frame
                    roi = frame[top_left[1]:top_left[1] + drum_h, top_left[0]:top_left[0] + drum_w]

                    # Create an inverse mask
                    mask_inv = cv2.bitwise_not(mask)

                    # Black out the area of the drum in the frame
                    frame_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

                    # Take only the drum region from the drum image
                    drum_fg = cv2.bitwise_and(drum_img, drum_img, mask=mask)

                    # Combine the drum region with the frame region
                    frame[top_left[1]:top_left[1] + drum_h, top_left[0]:top_left[0] + drum_w] = cv2.add(frame_bg, drum_fg)

        cv2.imshow('web cam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
