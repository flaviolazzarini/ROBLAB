import naoqi_proxy_python_classes
import qi
from configuration import PepperConfiguration
from pynaoqi_mate import Robot

from WaitingAnimation import WaitingAnimation

from FaceRecognition import FaceRecognition
from HideNSeek import HideNSeek

if __name__ == '__main__':
    config = PepperConfiguration("Porter")
    #config = PepperConfiguration("", "localhost", 53101)
    robot = Robot(config)
    hideNseek = HideNSeek(robot)
    hideNseek.run()
