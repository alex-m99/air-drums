# drum states:
# - 0: the circle is out of the rectangle (sound shouldn't play)
# - 1: the circle just entered the rectangle (the sound should play)
# - 2: the circle is in the rectangle (sound shouldn't play)  

import pygame
import cv2


class Drum:
    def __init__(self, name, topLeft, bottomRight, image, imagePath):
        self.__name = name
        self.__topLeft = topLeft
        self.__bottomRight = bottomRight
        self.__image = image
        self.__imagePath = imagePath
        self.__hasCircle = False
        self.__state = 0
        self.__velocity = 0.0
        self.__direction = "None"
        self.__soundPath = self.chooseSoundPath(imagePath)

        pygame.mixer.init()
        self.__sound = pygame.mixer.Sound(self.__soundPath) if self.__soundPath else None

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
        
    def setImagePath(self, imagePath):
        self.__imagePath = imagePath
    
    def getImagePath(self):
        return self.__imagePath
    
    def playSound(self, volume):
        self.__sound.set_volume(volume)
        self.__sound.play()

    def chooseSoundPath(self, imagePath):
        path = "resources/sounds/"
        match imagePath:
            case "resources/images/normal_snare.png":
                return path + "snare1.mp3"
            case "resources/images/loud_snare.jpg":
                return path + "snare2.wav"
            case "resources/images/electronic_snare2.jpg":
                return path + "snare3.wav"
            case "resources/images/normal_kick.jpg":
                return path + "kick1.mp3"
            case "resources/images/loud_kick.png":
                return path + "kick2.mp3"
            case "resources/images/electronic_kick.png":
                return path + "kick3.mp3"
            case "resources/images/ride.jpg":
                return path + "ride1.wav"
            case "resources/images/hihat.jpg":
                return path + "hihat.mp3"
            case "resources/images/electronic_hihat.jpg":
                return path + "ride3.wav"
            case "resources/images/crash.jpg":
                return path + "crash.mp3"
            case "resources/images/china.jpg":
                return path + "china.mp3"
            case "resources/images/electronic_crash.jpg":
                return path + "electronic_cymbal.wav"
            case _:
                return None