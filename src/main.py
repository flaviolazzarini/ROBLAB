from configuration import PepperConfiguration
from pynaoqi_mate import Robot
import logging

from HideNSeek import HideNSeek

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    config = PepperConfiguration("Amber")
    #config = PepperConfiguration("", "localhost", 53101)
    robot = Robot(config)
    hideNseek = HideNSeek(robot)
    hideNseek.run()
