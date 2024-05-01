class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.isInRideRectangle = False

    def setIsInRideRectangle(self, value):
        self.isInRideRectangle = value
    
    def getIsInRideRectangle(self):
        return self.isInRideRectangle