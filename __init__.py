# Basic Animation Framework
from Tkinter import *
from bullet import *
from collision import *
import math
import defender
from starclass import *
import handFinder
from shield import *

####################################
# customize these functions
####################################

def init(data):
    data.star1 = Star(data.width/2, data.height/2, 60, 10, 'cyan2')
    data.rotation = 0
    #data.shield = Shield(data.width/2 - 70, data.height/2 -70, data.width/2 + 70, data.height/2 + 70)
    # load data.xyz as appropriate
    data.shields = (-45, 135)
    data.mode = 'play'
    #data.shield = Shield(data.width/2 - 70, data.height/2 -70, data.width/2 + 70, data.height/2 + 70)
    data.shield1 = Shield(data.width/2, data.height/2,  90, data.shields, 90, 'blue')
    data.timerDelay = 10 # 100 millisecond == 0.1 seconds
    data.timerCalls = 0
    data.pause = True
    handFinder.init(data)
    defender.init(data)
    
def drawEnd(canvas):
    canvas.create_rectangle(0,0, 50, 50, fill = 'red')


def mousePressed(event, data):
    # use event. x and event.y
    if data.mode == 'play':
        if data.star1.die() == True:
            data.mode = 'end'
        else: 
            data.star1.hit()

def keyPressed(event, data):
    pass
    # use event.char and event.keysym
def rgbString(red, green, blue):    
    return "#%02x%02x%02x" % (red, green, blue)


def redrawAll(canvas, data):
    # draw in canvas
    if data.mode == 'play':
        color = rgbString(255, data.rotation%255, 0)
        data.star1.draw(canvas)
        data.shield1.draw(canvas)
        data.star1.draw(canvas)
        defender.redrawAll(canvas, data)
        #data.shield.draw(canvas)
    if data.mode == 'end':
        drawEnd(canvas) 
    
def timerFired(data):
        if data.mode == 'play':
            handFinder.timerFired(data)
            frame = data.frame
            if data.pause != True:
                data.rotation = math.degrees(frame.hands[0].palm_normal.roll)
                
                data.shield1.startPosL = tuple(map(lambda x: x+data.rotation, data.shields))
                #print data.shields
                #data.rectOffsetX = frame.hands[0].palm_position[0]
                #data.rectOffsetY = frame.hands[0].palm_position[2]
                #data.rectOffset = frame.hands[0].palmPosition
                data.timerCalls += 1
                defender.timerFired(data)
            if data.star1.die() == True:
                data.mode = 'end'
            

             
    

    

    #data.shield.draw(canvas)
    

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='LightSkyBlue4', width=0)

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
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
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
run(800, 800)