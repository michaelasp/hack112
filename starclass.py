
import math

class Star():
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def generatePoints(self):
        pts = []
        numPts = 5
        for num in range(numPts):
            theta = (2*math.pi*num/numPts) + (math.pi/2)
            inTheta = theta + (2*math.pi/numPts*2)
            x = self.x + math.cos(theta)*self.size
            y = self.y - math.sin(theta)*self.size
            inx = self.x + math.cos(inTheta)*self.size
            iny = self.y - math.sin(inTheta)*self.size
            pts += [x,y, inx, iny] 
        return pts

    def draw(self, canvas):
        pts = self.generatePoints()
        print(pts)
        canvas.create_polygon(pts, fill = self.color)