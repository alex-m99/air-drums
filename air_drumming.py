
import pygame
from moviepy.editor import VideoFileClip
from start_drum_app import start_drum_app
from button import Button

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

# Create buttons
play_button = Button("Start", 100, 200, 300, 100, GREEN, (0, 200, 0), action=start_drum_app) # Change action later
choose_drums_button = Button("Choose Drums", 100, 350, 300, 100, RED, (200, 0, 0), action=None)
choose_mode_button = Button("Mode select", 780, 110, 300, 100, GREEN, (0, 200, 0), image= None)
exit_button = Button("Exit", 100, 500, 300, 100, RED, (200, 0, 0), action=pygame.quit)

# Submenu buttons
snare_button = Button("Snare", 55, 100, 200, 100, GREEN, (0, 200, 0), image=None)
kick_button = Button("Kick", 290, 100, 200, 100, GREEN, (0, 200, 0), image=None)
rythm_cymbal_button = Button("Rythm Cymbal", 710, 100, 200, 100, GREEN, (0, 200, 0), image=None)
accent_cymbal_button = Button("Accent Cymbal", 945, 100, 200, 100, GREEN, (0, 200, 0), image=None)
back_button = Button("Back", 440, 550, 300, 100, RED, (200, 0, 0), action=None, image=None)

# Mode images
mode_pic1 = pygame.image.load("resources/images/transparent_mode.png")
mode_pic2 = pygame.image.load("resources/images/mask_mode.png")

# Drum images
snare_pic1 = pygame.image.load("resources/images/normal_snare.png")
snare_pic2 = pygame.image.load("resources/images/loud_snare.jpg")
snare_pic3 = pygame.image.load("resources/images/electronic_snare2.jpg")


kick_pic1 = pygame.image.load("resources/images/normal_kick.jpg")
kick_pic2 = pygame.image.load("resources/images/loud_kick.png")
kick_pic3 = pygame.image.load("resources/images/electronic_kick.png")

rythm_cymbal_pic1 = pygame.image.load("resources/images/ride.jpg")
rythm_cymbal_pic2 = pygame.image.load("resources/images/hihat.jpg")
rythm_cymbal_pic3 = pygame.image.load("resources/images/electronic_hihat.jpg")

accent_cymbal_pic1 = pygame.image.load("resources/images/crash.jpg")
accent_cymbal_pic2 = pygame.image.load("resources/images/china.jpg")
accent_cymbal_pic3 = pygame.image.load("resources/images/electronic_crash.jpg")



# Change the dimensions of the images
mode_pic1 = pygame.transform.scale(mode_pic1, (300, 180))
mode_pic2 = pygame.transform.scale(mode_pic2, (300, 180))

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

selected_mode = mode_pic1
mode_image = "transparent_mode.png"
mode_name = "Transparent mode"

selected_snare = snare_pic1
snare_image = "normal_snare.png"
snare_name = "Normal snare"

selected_kick = kick_pic1
kick_image = "normal_kick.jpg"
kick_name = "Normal kick"

selected_rythm_cymbal = rythm_cymbal_pic1
rythm_cymbal_image = "ride.jpg"
rythm_cymbal_name = "Ride"

selected_accent_cymbal = accent_cymbal_pic1
accent_cymbal_image = "crash.jpg"
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
        choose_mode_button.draw(screen,mouse_pos)
        exit_button.draw(screen, mouse_pos)

        # Draw mode image
        screen.blit(selected_mode, (780, 210))

        # Add text under mode image
        text_mode = font.render(mode_name, True, (255, 255, 255))
        screen.blit(text_mode, (850, 360))

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
                elif choose_mode_button.is_clicked(mouse_pos):
                    if selected_mode == mode_pic1:
                        mode_name = "Mask mode"
                        mode_image = "mask_mode.png"
                        selected_mode = mode_pic2
                    else:
                        mode_name = "Transparent mode"
                        mode_image = "transparent_mode.png"
                        selected_mode = mode_pic1
            else:
                if snare_button.is_clicked(mouse_pos):
                    if selected_snare == snare_pic1:
                        snare_name = "Loud snare"
                        snare_image = "loud_snare.jpg"
                        selected_snare = snare_pic2
                    elif selected_snare == snare_pic2:
                        snare_name = "Electronic snare"
                        snare_image = "electronic_snare2.jpg"
                        selected_snare = snare_pic3
                    else:
                        snare_name = "Normal snare"
                        snare_image = "normal_snare.png"
                        selected_snare = snare_pic1
                elif kick_button.is_clicked(mouse_pos):
                    if selected_kick == kick_pic1:
                        kick_name = "Loud kick"
                        kick_image = "loud_kick.png"
                        selected_kick = kick_pic2
                    elif selected_kick == kick_pic2:
                        kick_name = "Electronic kick"
                        kick_image = "electronic_kick.png"
                        selected_kick = kick_pic3
                    else:
                        kick_name = "Normal kick"
                        kick_image = "normal_kick.jpg"
                        selected_kick = kick_pic1
                elif rythm_cymbal_button.is_clicked(mouse_pos):
                    if selected_rythm_cymbal == rythm_cymbal_pic1:
                        rythm_cymbal_name = "Hihat"
                        rythm_cymbal_image = "hihat.jpg"
                        selected_rythm_cymbal = rythm_cymbal_pic2
                    elif selected_rythm_cymbal == rythm_cymbal_pic2:
                        rythm_cymbal_name = "Electronic hihat"
                        rythm_cymbal_image = "electronic_hihat.jpg"
                        selected_rythm_cymbal = rythm_cymbal_pic3
                    else:
                        rythm_cymbal_name = "Ride"
                        rythm_cymbal_image = "ride.jpg"
                        selected_rythm_cymbal = rythm_cymbal_pic1
                elif accent_cymbal_button.is_clicked(mouse_pos):
                    if selected_accent_cymbal == accent_cymbal_pic1:
                        accent_cymbal_name = "China cymbal"
                        accent_cymbal_image = "china.jpg"
                        selected_accent_cymbal = accent_cymbal_pic2
                    elif selected_accent_cymbal == accent_cymbal_pic2:
                        accent_cymbal_name = "Electronic crash"
                        accent_cymbal_image = "electronic_crash.jpg"
                        selected_accent_cymbal = accent_cymbal_pic3
                    else:
                        accent_cymbal_name = "Crash cymbal"
                        accent_cymbal_image = "crash.jpg"
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
    action(path+snare_image, path+kick_image, path+rythm_cymbal_image, path+accent_cymbal_image, mode_name)