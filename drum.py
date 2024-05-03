# drum states:
# - 0: the circle is out of the rectangle (sound shouldn't play)
# - 1: the circle just entered the rectangle (the sound should play)
# - 2: the circle is in the rectangle (sound shouldn't play)  

import pygame
import cv2


class Drum:
    def __init__(self, name, topLeft, bottomRight, soundPath, image):
        self.__name = name
        self.__topLeft = topLeft
        self.__bottomRight = bottomRight
        self.__soundPath = soundPath
        self.__hasCircle = False
        self.__hasHit = False
        self.__state = 0
        self.__velocity = 0.0
        self.__direction = "None"
        self.__image = image

        pygame.mixer.init()
        self.__sound = pygame.mixer.Sound(soundPath)

    def setName(self, name):
        self.__name = name
    
    def getName(self):
        return self.__name
    
    def setTopLeft(self, topLeft):
        self.__topLeft = topLeft

    def getTopLeft(self):
        return self.__topLeft
    
    def setBottomRight(self, bottomRight):
        self.__bottomRight = bottomRight

    def getBottomRight(self):
        return self.__bottomRight
    
    def setSoundPath(self, soundPath):
        self.__soundPath = soundPath

    def getSoundPath(self):
        return self.__soundPath
    
    def setHasCircle(self, hasCircle):
        self.__hasCircle = hasCircle
    
    def getHasCircle(self):
        return self.__hasCircle
    
    def setHasHit(self, hasHit):
        self.__hasHit = hasHit

    def getHasHit(self):
        return self.__hasHit

    def setState(self, state):
        self.__state = state
    
    def getState(self):
        return self.__state
    
    def setVelocity(self, velocity):
        self.__velocity = velocity
    
    def getVelocity(self):
        return self.__velocity
    
    def setDirection(self, direction):
        self.__direction = direction
    
    def getDirection(self):
        return self.__direction
    
    def setImage(self, image):
        self.__image = image
    
    def getImage(self, width, height):
        if self.__image is not None:
            return cv2.resize(self.__image, (width, height))
        else:
            return None
    
    def playSound(self):
        self.__sound.play()
    