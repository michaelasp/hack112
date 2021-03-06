
import math

class Star():
    def __init__(self, x, y, rad, health, color):
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        self.health = health

    def getBounds(self):
        pass
        #fill in distance formula and bullet class


    def generatePoints(self):
        pts = []
        numPts = 5
        for num in range(numPts):
            theta = (2*math.pi*num/numPts) + (math.pi/2)
            inTheta = theta + (2*math.pi/numPts*2)
            x = self.x + math.cos(theta)*self.rad
            y = self.y - math.sin(theta)*self.rad
            inx = self.x + math.cos(inTheta)*self.rad
            iny = self.y - math.sin(inTheta)*self.rad
            pts += [x,y, inx, iny] 
        return pts

    def draw(self, canvas):
        pts = self.generatePoints()
        canvas.create_polygon(pts, fill = self.color)

    #tells you if the star is dead or not
    def hit(self):
        self.health -= 1
        if self.health <= 2:
            self.color = 'red'
        
    def die(self):
        if self.health <= 0:
            self.color = 'cyan2'
            return True
        return False






