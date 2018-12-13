import concurrent
from pynaoqi_mate import Robot
from configuration import PepperConfiguration
from naoqi import ALModule


class ObstacleAvoidance(ALModule):

    def __init__(self, pepper):
        session = pepper.session
        self.motion = session.service("ALMotion")
        self.posture = session.service("ALRobotPosture")
        self.__set_external_collision_protection()
        self._found = False
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def set_found(self, found):
        self._found = found

    def __set_external_collision_protection(self):
        self.motion.setExternalCollisionProtectionEnabled("All", True)

    def move_to_concurrently(self):
        self._executor.submit(self.__move_to)

    def __move_to(self, distance=10, theta=0):
        while not self._found:
            self.motion.moveTo(distance, 0, theta)
            if self.posture.getPostureFamily() == "Standing":
                self.motion.moveTo(-.1, 0, 0)
                self.motion.moveTo(0, 0, -0.4)
