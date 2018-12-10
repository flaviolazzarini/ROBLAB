from pynaoqi_mate import Robot
from configuration import PepperConfiguration
from naoqi import ALModule
from time import sleep

import sys
import time
from naoqi import ALProxy
from naoqi import motion

def setPosition(robot):
    session = robot.session
    postureProxy = session.service("ALRobotPosture")
    motionProxy = session.service("ALMotion")

    postureProxy.goToPosture("StandInit", 0.5)

    chainName = "Torso"
    space = 1
    useSensor = False

    current = motionProxy.getPosition(chainName, space, useSensor)
    valueBefore = current
    target = [
        current[0] + 9,
        current[1] + 9,
        current[2] + 9,
        current[3] + 0.5,
        current[4] + 0.5,
        current[5] + 0.5]

    fractionMaxSpeed = 0.5
    axisMask = 63

    motionProxy.setPosition(chainName, space, target, fractionMaxSpeed, axisMask)

    valueAfter = motionProxy.getPosition(chainName, space, useSensor)
    time.sleep(5.0)

def main(robotIP):
    PORT = 9559

    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    # Example showing how to set LArm Position, using a fraction of max speed
    chainName = "LArm"
    space     = motion.FRAME_TORSO
    useSensor = False

    # Get the current position of the chainName in the same space
    current = motionProxy.getPosition(chainName, space, useSensor)

    target  = [
        current[0] + 0.1,
        current[1] + 0.1,
        current[2] + 0.1,
        current[3] + 0.0,
        current[4] + 0.0,
    current[5] + 0.0]

    fractionMaxSpeed = 0.5
    axisMask         = 7 # just control position

    motionProxy.setPosition(chainName, space, target, fractionMaxSpeed, axisMask)

    time.sleep(1.0)

    # Example showing how to set Torso Position, using a fraction of max speed
    chainName        = "Torso"
    space            = 2
    position         = [0.0, 0.0, 0.25, 0.0, 0.0, 0.0] # Absolute Position
    fractionMaxSpeed = 0.2
    axisMask         = 63
    motionProxy.setPosition(chainName, space, position, fractionMaxSpeed, axisMask)


if __name__ == "__main__":
    config = PepperConfiguration("Porter")
    robot = Robot(config)
    setPosition(robot)