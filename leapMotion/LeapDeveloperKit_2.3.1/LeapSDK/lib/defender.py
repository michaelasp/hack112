# https://developer.leapmotion.com/sdk/v2

#import Leap, sys, thread, time 
# import os, sys, inspect, thread, time
# sys.path.insert(0, "C:\Users\Joshua Moavenzadeh\Desktop\LeapDeveloperKit_3.2.0+45899_win\LeapSDK\lib/x86")

# import Leap
# from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import bullet
import random
import math
from Tkinter import *

####################################
# customize these functions
####################################
class Bullet(object):
    # Model
    def __init__(self, cx, cy, angle, speed):
        # A bullet has a position, a size, a direction, and a speed
        self.cx = cx
        self.cy = cy
        self.r = 5
        self.angle = angle
        self.speed = speed
        
    # View
    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, 
                           self.cx + self.r, self.cy + self.r,
                           fill="red", outline=None)

    # Controller
    def moveBullet(self):
        # Move according to the original trajectory
        self.cx += math.cos(math.radians(self.angle))*self.speed
        self.cy -= math.sin(math.radians(self.angle))*self.speed 
        
    def isOffscreen(self, width, height):
        # Check if the bullet has moved fully offscreen
        return (self.cx + self.r <= 0 or self.cx - self.r >= width) and \
               (self.cy + self.r <= 0 or self.cy - self.r >= height)

    
class BulletSpawner(object):
    import random
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def makeBullet(self, screenWidth, screenHeight):
       
        side = random.choice(["topbot"]) #,"leftright"])
        if side == "topbot":
            x = random.randint(0,screenWidth)
            y = 0 #random.choice([0,screenHeight])
        elif side == "leftright":
            x = random.choice([0,screenWidth])
            y = random.randint(0,screenHeight)
        
        speed = random.randint(10,40)
        
        if y == 0:
            angle = math.degrees(math.atan((y *1. - screenHeight/2)/(screenWidth/2 - x)))
        else:
            angle = 45
        
        print("(%d,%d)" % (x,y), "(300,300)", angle)
        
        return Bullet(x, y, angle, speed)
        
def init(data):
    data.timer = 0
    data.spawner = BulletSpawner(0,0)
    data.bullets = []
    
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    data.timer += 1
    if data.timer % 10 == 0:
        data.bullets.append(data.spawner.makeBullet(data.width,data.height))
        
    for bullet in data.bullets:
        bullet.moveBullet()
        if bullet.isOffscreen(data.width, data.height):
            data.bullets.remove(bullet)


def redrawAll(canvas, data):
    x,y = data.width/2, data.height/2
    canvas.create_oval(x - 10, y - 10, x+10,y+10)
    for bullet in data.bullets:
        bullet.draw(canvas)
        

####################################
# use the run function as-is
####################################


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 20 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)
