from Tkinter import *
class Collision(object):
    def __init__(self, cx, cy, r, power):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.power = power
    
    def draw(self, canvas):
        r = self.r
        canvas.create_oval(self.cx-r,self.cy-r,self.cx+r,self.cy+r,outline = "orange")