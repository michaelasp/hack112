import os, sys, inspect, thread, time
sys.path.insert(0, "C:\Users/aspin\Downloads\Leap_Motion_SDK_Windows_2.3.1\LeapDeveloperKit_2.3.1+31549_win\LeapSDK\lib/x64")
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

def init(data):
    data.controller = Leap.Controller()
    data.frame = data.controller.frame()
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.boneNames = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

def timerFired(data):
    updateLeapMotionData(data)
    #printLeapMotionData(data)

def updateLeapMotionData(data):
    data.frame = data.controller.frame()
    frame = data.frame
    if len(frame.hands) > 0:
        data.pause = False
    else:
        data.pause = True
def printLeapMotionData(data):
    frame = data.frame

    print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
          frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))
    
    # Get hands
    
    for hand in frame.hands:

        handType = "Left hand" if hand.is_left else "Right hand"

        print "  %s, id %d, position: %s" % (
            handType, hand.id, hand.palm_position)

        # Get the hand's normal vector and direction
        normal = hand.palm_normal
        direction = hand.direction

        # Calculate the hand's pitch, roll, and yaw angles
        print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
            direction.pitch * Leap.RAD_TO_DEG,
            normal.roll * Leap.RAD_TO_DEG,
            direction.yaw * Leap.RAD_TO_DEG)