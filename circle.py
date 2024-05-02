class Circle:
    def __init__(self, center, radius):
        self.__center = center
        self.__radius = radius
        self.__isInRideRectangle = False
        self.__playedRideRectangle = False

    def setCenter(self, value):
        self.__center = value
    
    def getCenter(self):
        return self.__center
    
    def setRadius(self, value):
        self.__radius = value
    
    def getRadius(self):
        return self.__radius

    def setIsInRideRectangle(self, value):
        self.__isInRideRectangle = value
    
    def getIsInRideRectangle(self):
        return self.__isInRideRectangle
    
    def setPlayedRideRectangle(self, value):
        self.__playedRideRectangle = value
    
    def getPlayedRideRectangle(self):
        return self.__playedRideRectangle