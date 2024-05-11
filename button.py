
import pygame

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
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)

        if self.image:
            screen.blit(self.image, (self.x, self.y))

    def is_clicked(self, mouse):
        return self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y