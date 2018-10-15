import naoqi_proxy_python_classes
from configuration import PepperConfiguration
from pynaoqi_mate import Robot

if __name__ == '__main__':
    config = PepperConfiguration("Porter")
    #config = PepperConfiguration("", "localhost", 55830)
    robot = Robot(config)