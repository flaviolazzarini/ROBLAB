from pynaoqi_mate import Robot
from configuration import PepperConfiguration
from naoqi import ALModule

class ObstacleAvoidance(ALModule):

    def __init__(self, pepper):
        session = pepper.session
        self.motion = session.service("ALMotion")
        self.posture = session.service("ALRobotPosture")
        self.setExternalCollisionProtection()

    def setExternalCollisionProtection(self):
        self.motion.setExternalCollisionProtectionEnabled("All", True)

    def moveTo(self, distance, theta):
        self.motion.moveTo(distance, 0, theta)
        if self.posture.getPostureFamily() == "Standing":
            self.motion.moveTo(-.1, 0, 0)
            self.motion.moveTo(0, 0, -0.4)