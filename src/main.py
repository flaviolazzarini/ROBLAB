from configuration import PepperConfiguration
from pynaoqi_mate import Robot

from WaitingAnimation import WaitingAnimation

if __name__ == '__main__':
    config = PepperConfiguration("Amber")
    #config = PepperConfiguration("", "localhost", 53101)
    robot = Robot(config)

    waitingAnimation = WaitingAnimation(robot)
    waitingAnimation.start(robot, 10)