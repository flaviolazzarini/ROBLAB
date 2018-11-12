import naoqi_proxy_python_classes
import qi
from configuration import PepperConfiguration
from pynaoqi_mate import Robot

from WaitingAnimation import WaitingAnimation

from FaceRecognition import FaceRecognition

if __name__ == '__main__':
    config = PepperConfiguration("Amber")
    #config = PepperConfiguration("", "localhost", 53101)
    robot = Robot(config)
    faceRec = FaceRecognition(robot)
    faceRec.run()
