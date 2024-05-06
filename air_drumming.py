import cv2
import numpy as np
import pygame
from drum import Drum
import ctypes
from moviepy.editor import VideoFileClip

mouse_clicked = False

# Define the drum app function
def start_drum_app(snare_img_path, kick_img_path, rythm_img_path, accent_img_path):
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
            elif drum.getState() == 1 and drum.getDirection() == "Down":
                drum.playSound()
        
        #print('Mouse click in loop: ', mouse_clicked)

        # Check if mouse is clicked and play bass drum sound
        if mouse_clicked:
            kick.playSound()
            mouse_clicked = False

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

# Initialize Pygame
pygame.init()

# Constants for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the screen
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")


# Load music
pygame.mixer.music.load("resources/sounds/background_music.mp3")  # Change "background_music.mp3" to your music file
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
pygame.mixer.music.set_pos(9.5)


# Load GIF using moviepy
gif_clip = VideoFileClip("resources/images/background.gif")
gif_clip = gif_clip.resize((screen_width, screen_height))
frames = [pygame.image.fromstring(frame.tostring(), gif_clip.size, "RGB") for frame in gif_clip.iter_frames()]

# Button class
class Button:
    def __init__(self, text, x, y, width, height, inactive_color, active_color, action=None, image=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.action = action
        self.image = image
        self.clicked = False

    def draw(self, screen, mouse):
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.inactive_color, (self.x, self.y, self.width, self.height))
        
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)

        if self.image:
            screen.blit(self.image, (self.x, self.y))

    def is_clicked(self, mouse):
        return self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y


# Create buttons
play_button = Button("Play", 100, 200, 300, 100, GREEN, (0, 200, 0), action=start_drum_app) # Change action later
choose_drums_button = Button("Choose Drums", 100, 350, 300, 100, RED, (200, 0, 0), action=None)
exit_button = Button("Exit", 100, 500, 300, 100, RED, (200, 0, 0), action=pygame.quit)

# Submenu buttons
snare_button = Button("Snare", 55, 100, 200, 100, GREEN, (0, 200, 0), image=None)
kick_button = Button("Kick", 290, 100, 200, 100, GREEN, (0, 200, 0), image=None)
rythm_cymbal_button = Button("Rythm Cymbal", 710, 100, 200, 100, GREEN, (0, 200, 0), image=None)
accent_cymbal_button = Button("Accent Cymbal", 945, 100, 200, 100, GREEN, (0, 200, 0), image=None)
back_button = Button("Back", 440, 550, 300, 100, RED, (200, 0, 0), action=None, image=None)

# Drum images
snare_pic1 = pygame.image.load("resources/images/snare1.png")
snare_pic2 = pygame.image.load("resources/images/snare2.png")
snare_pic3 = pygame.image.load("resources/images/snare3.png")


kick_pic1 = pygame.image.load("resources/images/kick1.png")
kick_pic2 = pygame.image.load("resources/images/kick2.png")
kick_pic3 = pygame.image.load("resources/images/kick3.png")

rythm_cymbal_pic1 = pygame.image.load("resources/images/ride1.png")
rythm_cymbal_pic2 = pygame.image.load("resources/images/ride2.png")
rythm_cymbal_pic3 = pygame.image.load("resources/images/ride3.png")

accent_cymbal_pic1 = pygame.image.load("resources/images/crash1.png")
accent_cymbal_pic2 = pygame.image.load("resources/images/crash2.png")
accent_cymbal_pic3 = pygame.image.load("resources/images/crash3.png")



# Change the dimensions of the images
snare_pic1 = pygame.transform.scale(snare_pic1, (200, 200)) #width, height
snare_pic2 = pygame.transform.scale(snare_pic2, (200, 200))
snare_pic3 = pygame.transform.scale(snare_pic3, (200, 200))

kick_pic1 = pygame.transform.scale(kick_pic1, (200, 200)) #width, height
kick_pic2 = pygame.transform.scale(kick_pic2, (200, 200))
kick_pic3 = pygame.transform.scale(kick_pic3, (200, 200))

rythm_cymbal_pic1 = pygame.transform.scale(rythm_cymbal_pic1, (200, 200))
rythm_cymbal_pic2 = pygame.transform.scale(rythm_cymbal_pic2, (200, 200))
rythm_cymbal_pic3 = pygame.transform.scale(rythm_cymbal_pic3, (200, 200))

accent_cymbal_pic1 = pygame.transform.scale(accent_cymbal_pic1, (200, 200))
accent_cymbal_pic2 = pygame.transform.scale(accent_cymbal_pic2, (200, 200))
accent_cymbal_pic3 = pygame.transform.scale(accent_cymbal_pic3, (200, 200))


# Initialize the font
font = pygame.font.Font(None, 36)

# Main menu loop
running = True
action = None
submenu = False

selected_snare = snare_pic1
snare_image = "snare1.png"
snare_name = "Normal snare"

selected_kick = kick_pic1
kick_image = "kick1.png"
kick_name = "Normal kick"

selected_rythm_cymbal = rythm_cymbal_pic1
rythm_cymbal_image = "ride1.png"
rythm_cymbal_name = "Ride"

selected_accent_cymbal = accent_cymbal_pic1
accent_cymbal_image = "crash1.png"
accent_cymbal_name = "Crash"

frame_index = 0
clock = pygame.time.Clock()

while running:
    screen.blit(frames[frame_index], (0, 0))
    frame_index = (frame_index + 1) % len(frames)  # Loop through frames

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    if not submenu:
        # Draw main menu buttons
        play_button.draw(screen, mouse_pos)
        choose_drums_button.draw(screen, mouse_pos)
        exit_button.draw(screen, mouse_pos)

       # screen.blit(selected_snare, (800, 200))
        #screen.blit(selected_kick, (800, 400))

    else:
        # Draw submenu buttons
        snare_button.draw(screen, mouse_pos)
        kick_button.draw(screen, mouse_pos)
        rythm_cymbal_button.draw(screen, mouse_pos)
        accent_cymbal_button.draw(screen, mouse_pos)
        back_button.draw(screen, mouse_pos)

        # Draw drum images
        screen.blit(selected_snare, (55, 230))
        screen.blit(selected_kick, (290, 230))
        screen.blit(selected_rythm_cymbal, (710, 230))
        screen.blit(selected_accent_cymbal, (945, 230))

         # Add text under drum images
        text_snare = font.render(snare_name, True, (255, 255, 255))
        text_kick = font.render(kick_name, True, (255, 255, 255))
        text_rythm_cymbal = font.render(rythm_cymbal_name, True, (255, 255, 255))
        text_accent_cymbal = font.render(accent_cymbal_name, True, (255, 255, 255))
        screen.blit(text_snare, (55 + selected_snare.get_width() // 2 - text_snare.get_width() // 2, 450))
        screen.blit(text_kick, (290 + selected_kick.get_width() // 2 - text_kick.get_width() // 2, 450))
        screen.blit(text_rythm_cymbal, (710 + selected_rythm_cymbal.get_width() // 2 - text_rythm_cymbal.get_width() // 2, 450))
        screen.blit(text_accent_cymbal, (945 + selected_accent_cymbal.get_width() // 2 - text_accent_cymbal.get_width() // 2, 450))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not submenu:
                if play_button.is_clicked(mouse_pos):
                    action = play_button.action
                    running = False
                elif choose_drums_button.is_clicked(mouse_pos):
                    submenu = True
                elif exit_button.is_clicked(mouse_pos):
                    running = False
            else:
                if snare_button.is_clicked(mouse_pos):
                    if selected_snare == snare_pic1:
                        snare_name = "Loud snare"
                        snare_image = "snare2.png"
                        selected_snare = snare_pic2
                    elif selected_snare == snare_pic2:
                        snare_name = "Electric snare"
                        snare_image = "snare3.png"
                        selected_snare = snare_pic3
                    else:
                        snare_name = "Normal snare"
                        snare_image = "snare1.png"
                        selected_snare = snare_pic1
                elif kick_button.is_clicked(mouse_pos):
                    if selected_kick == kick_pic1:
                        kick_name = "Loud kick"
                        kick_image = "kick2.png"
                        selected_kick = kick_pic2
                    elif selected_kick == kick_pic2:
                        kick_name = "Electric kick"
                        kick_image = "kick3.png"
                        selected_kick = kick_pic3
                    else:
                        kick_name = "Normal kick"
                        kick_image = "kick1.png"
                        selected_kick = kick_pic1
                elif rythm_cymbal_button.is_clicked(mouse_pos):
                    if selected_rythm_cymbal == rythm_cymbal_pic1:
                        rythm_cymbal_name = "Hihat"
                        rythm_cymbal_image = "ride2.png"
                        selected_rythm_cymbal = rythm_cymbal_pic2
                    elif selected_rythm_cymbal == rythm_cymbal_pic2:
                        rythm_cymbal_name = "Electric hihat"
                        rythm_cymbal_image = "ride3.png"
                        selected_rythm_cymbal = rythm_cymbal_pic3
                    else:
                        rythm_cymbal_name = "Ride"
                        rythm_cymbal_image = "ride1.png"
                        selected_rythm_cymbal = rythm_cymbal_pic1
                elif accent_cymbal_button.is_clicked(mouse_pos):
                    if selected_accent_cymbal == accent_cymbal_pic1:
                        accent_cymbal_name = "China cymbal"
                        accent_cymbal_image = "crash2.png"
                        selected_accent_cymbal = accent_cymbal_pic2
                    elif selected_accent_cymbal == accent_cymbal_pic2:
                        accent_cymbal_name = "Electric crash"
                        accent_cymbal_image = "crash3.png"
                        selected_accent_cymbal = accent_cymbal_pic3
                    else:
                        accent_cymbal_name = "Crash cymbal"
                        accent_cymbal_image = "crash1.png"
                        selected_accent_cymbal = accent_cymbal_pic1
                
                elif back_button.is_clicked(mouse_pos):
                    submenu = False

    


    # Display images under drum buttons
    # drum1_button.image = selected_drum1
    # drum2_button.image = selected_drum2
    # drum3_button.image = selected_drum3


    pygame.display.update()
    clock.tick(10)  # Adjust frame rate as needed

print("Selected_drum1: ", selected_snare)
print("Selected_drum2: ", selected_kick)
print("Selected_drum3: ", selected_rythm_cymbal)
print("Selected_drum4: ", selected_accent_cymbal)

# Quit Pygame when you want to close the app
pygame.quit()

path = "resources/images/"

print(path+snare_image)
print(path+kick_image)
print(path+rythm_cymbal_image)
print(path+accent_cymbal_image)



if action:
    action(path+snare_image, path+kick_image, path+rythm_cymbal_image, path+accent_cymbal_image)