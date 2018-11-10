
import math

class Shield(object):

    def __init__(self, xc, yc, rad, startPosL, degree, color):
        self.xc = xc
        self.yc = yc
        self.rad = rad
        self.color = color
        self.degree = degree
        self.startPosL = startPosL

    def getCoords(self, rad):
        return self.xc - rad, self.yc - rad, self.xc + rad, self.yc + rad

    def draw(self, canvas):
        rect = self.getCoords(self.rad)
        start = self.startPosL
        for startNum in range(len(self.startPosL)):
            canvas.create_arc(rect, start = start[startNum], extent = self.degree, fill = self.color)
        circRect = self.getCoords(self.rad * 0.8)
        canvas.create_oval(circRect, fill = 'LightSkyBlue4', width = 0)






