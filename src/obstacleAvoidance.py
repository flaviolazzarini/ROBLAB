from pynaoqi_mate import Robot
from configuration import PepperConfiguration
from naoqi import ALModule
from time import sleep


class ObstacleAvoidance(ALModule):

    def __init__(self, myrobot):
        super(ObstacleAvoidance, self)

        myrobot.ALMotion.setExternalCollisionProtectionEnabled("Move", True)
        myrobot.ALMotion.moveTo(5.0, 5.0, 10)


if __name__ == "__main__":

    #config = PepperConfiguration("Amber")
    config = PepperConfiguration("", "localhost", 52038)
    robot = Robot(config)

    obstacleAvoidance = ObstacleAvoidance(robot)
