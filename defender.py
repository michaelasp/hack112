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
        start_new_thread(sounds.play, ('hack112\\bigExplosion.wav',))
        collided = False
    
def init(data):
    data.timer = 0
    data.level = 1
    data.seconds = 0
    data.spawner = BulletSpawner(0,0)
    data.bullets = []
    data.collisions = []
    data.bomb = []
    
    
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    pass

def timerFired(data):
    data.timer += 1
    if data.timer % 100 == 0:
        data.seconds += 1
        
    if data.timer % 500 == 0:
        data.level += 1
        start_new_thread(sounds.play, ('hack112\\level.wav',))
        
    if data.timer % int(100 * (4./5)**data.level) == 0:
    
        data.bullets.append(data.spawner.makeBullet(data.width,data.height, data.level))
        
    for bullet in data.bullets:
        removed = False
        bullet.moveBullet()
        
        if bullet.isOffscreen(data.width, data.height):
            data.bullets.remove(bullet)
        
        r1 = bullet.r
        r2 = 60
        shieldSize = 90
        x = bullet.cx
        y = bullet.cy
       
        # In range of shield
        if math.sqrt((x*1.- data.width/2)**2 + (y*1. - data.height/2)**2) <= r1 + shieldSize:
            x1, y1 = bullet.cx, bullet.cy
            x2, y2 = data.width/2, data.height/2
            r1, r3 = bullet.r, shieldSize
            ang1, ang2 = data.shield1.startPosL
            bulletAngle = math.degrees(math.atan((-(y1 - data.height/2)*1.)/(x1 - data.width/2 )))
            if (ang1 % 360 > 0 and ang1 % 360 < 90) or (ang1 % 360 > 180 and ang1 % 360 < 270):
                smaller = min(ang1 % 360, ang2 % 360)
                larger  = max(ang1 % 360, ang2 % 360)
                if (bulletAngle % 360 <= larger+90 and bulletAngle % 360 >= larger)  or (bulletAngle%360 <= smaller + 90  and bulletAngle % 360 >= smaller):
                    pcollision = ((x1*r3+x2*r1*1.)/(r1+r3),(y1*r3+y2*r1*1.)/(r1+r3))
                    data.collisions.append(Collision(pcollision[0],pcollision[1], 2, bullet.r))
                    data.bullets.remove(bullet)
                    removed = True
                    collided = True
                    collideSound(collided)
            else:
                if ang1%360 <= 90 or ang1%360 >=270:
                    right = ang1
                else:
                    right = ang2 
                if bulletAngle % 360 >= 270:
                    if bulletAngle % 360 >= ang1 % 360:
                        pcollision = ((x1*r2+x2*r1*1.)/(r1+r2),(y1*r2+y2*r1*1.)/(r1+r2))
                        data.collisions.append(Collision(pcollision[0],pcollision[1], 2, bullet.r))
                        data.bullets.remove(bullet)
                        removed = True
                        collided = True
                        collideSound(collided)
                else:
                    if bulletAngle % 360 <= (ang1 +90) % 360:
                        pcollision = ((x1*r2+x2*r1*1.)/(r1+r2),(y1*r2+y2*r1*1.)/(r1+r2))
                        data.collisions.append(Collision(pcollision[0],pcollision[1], 2, bullet.r))
                        data.bullets.remove(bullet)
                        removed = True
                        collided = True
                        collideSound(collided)

                


        #Hits Pentagon
        if math.sqrt((x*1.- data.width/2)**2 + (y*1. - data.height/2)**2) <= r1 + r2 and removed == False:
        # the 300 is just data.width and data.height
            start_new_thread(sounds.play, ('hack112\\ouch.wav',))
            x1, y1 = bullet.cx, bullet.cy
            x2, y2 = data.width/2, data.height/2
            # the 10 is just the radius of the sample ship i used
            r1, r2 = bullet.r, 60

            
            # https://stackoverflow.com/questions/1736734/circle-circle-collision
            pcollision = ((x1*r2+x2*r1*1.)/(r1+r2),(y1*r2+y2*r1*1.)/(r1+r2))
            
            data.collisions.append(Collision(pcollision[0],pcollision[1], 2, bullet.r))
            data.bullets.remove(bullet)
            data.star1.hit()
    
    
    for collision in data.collisions:
       
        if collision.power < 10:
            collision.power = 10
        elif collision.power > 20:
            collision.power = 20
            
        if collision.r <= collision.power:
            data.collisions.append(Collision(collision.cx, collision.cy, collision.r + 2,collision.power))
    
    for bomb in data.bomb:
        if bomb.r <= bomb.power:
            data.bomb.append(Collision(bomb.cx, bomb.cy, bomb.r + 20, bomb.power))
        

def redrawAll(canvas, data):
    
    for collision in data.collisions:
        collision.draw(canvas)
        data.collisions.remove(collision)
        

        
    for bullet in data.bullets:
        bullet.draw(canvas)
    
    canvas.create_text(0,0, anchor = NW, text = "Health: %d" % data.star1.health, font = "Arial 14")
    canvas.create_text(data.width,0, anchor = NE, text = "Level: %d" % data.level, font = 'Arial 14')
        

# start_new_thread(run, (600, 600))
# start_new_thread(sounds.play, ('backgroundMusic.wav',))