# https://developer.leapmotion.com/sdk/v2

#import Leap, sys, thread, time 
import os, sys, inspect, thread, time
sys.path.insert(0, "C:\Users/aspin\Downloads\Leap_Motion_SDK_Windows_2.3.1\LeapDeveloperKit_2.3.1+31549_win\LeapSDK\lib/x64")

# import Leap
# from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

from bullet import *
from collision import *
import random
import math
from Tkinter import *

# threading for collision sounds
import thread
from thread import start_new_thread
import sounds

####################################
# customize these functions
####################################

collided = False

def collideSound(collided):
    # plays sound when collided
    if collided == True:
        start_new_thread(sounds.play, ('smallExplosion.wav',))
        collided = False
    
def init(data):
    data.timer = 0
    data.level = 1
    data.seconds = 0
    data.spawner = BulletSpawner(0,0)
    data.bullets = []
    data.collisions = []
    
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    data.timer += 1
    if data.timer % 100 == 0:
        data.seconds += 1
        
    if data.timer % 1000 == 0:
        data.level += 1
        
    if data.timer % int(100 * (4./5)**data.level) == 0:
    
        data.bullets.append(data.spawner.makeBullet(data.width,data.height, data.level))
        
    for bullet in data.bullets:
        bullet.moveBullet()
        
        if bullet.isOffscreen(data.width, data.height):
            data.bullets.remove(bullet)
        
        r1 = bullet.r
        r2 = 10
        x = bullet.cx
        y = bullet.cy
       
        # the 300 is just data.width and data.height
        
        if math.sqrt((x - 300)**2 + (y - 300)**2) <= r1 + r2:
            #collision  happens

            collided = True
            collideSound(collided)
            
            x1, y1 = bullet.cx, bullet.cy
            x2, y2 = data.width/2, data.height/2
            
            # the 10 is just the radius of the sample ship i used
            r1, r2 = bullet.r, 10
            
            # https://stackoverflow.com/questions/1736734/circle-circle-collision
            pcollision = ((x1*r2+x2*r1*1.)/(r1+r2),(y1*r2+y2*r1*1.)/(r1+r2))
            
            data.collisions.append(Collision(pcollision[0],pcollision[1], 2, bullet.r))
            data.bullets.remove(bullet)
    
    
    for collision in data.collisions:
        
        # if the collision is too small or too big, fix it
        if collision.power < 10:
            collision.power = 10
        if collision.power > 20:
            collision.power = 20
        if collision.r <= collision.power:
            data.collisions.append(Collision(collision.cx, collision.cy, collision.r + 2,collision.power))
        

def redrawAll(canvas, data):
    x,y = data.width/2, data.height/2
    canvas.create_rectangle(0,0,data.width,data.height,fill = "lightskyblue4")
    
    for collision in data.collisions:
        collision.draw(canvas)
        data.collisions.remove(collision)
        
    canvas.create_oval(x - 10, y - 10, x+10,y+10, fill = "blue")
    
        
    for bullet in data.bullets:
        bullet.draw(canvas)
    
    canvas.create_text(0,0, anchor = NW, text = "Time: %d" % data.seconds)
    canvas.create_text(data.width,0, anchor = NE, text = "Level: %d" % data.level)
   

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
    data.timerDelay = 10 # milliseconds
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

start_new_thread(run, (600, 600))
start_new_thread(sounds.play, ('backgroundMusic.wav',))
