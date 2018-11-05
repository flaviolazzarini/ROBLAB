from pynaoqi_mate import Robot
from configuration import PepperConfiguration
from naoqi import ALModule

class ObstacleAvoidance():


    def __init__(self, pepper, motion):
        # super(ObstacleAvoidance, self)
        session = pepper.session
        self.motion = motion
        self.posture = session.service("ALRobotPosture")
        self.setExternalCollisionProtection()
        self.found = False

    def set_found(self, found):
        self.found = found

    def setExternalCollisionProtection(self):
        self.motion.setExternalCollisionProtectionEnabled("All", True)

    def moveTo(self, distance=1.0, theta=0.1):
        while not self.found:
            self.motion.moveTo(distance, 0, theta)
            if self.posture.getPostureFamily() == "Standing":
                self.motion.moveTo(-.1, 0, 0)
                self.motion.moveTo(0, 0, -0.4)
