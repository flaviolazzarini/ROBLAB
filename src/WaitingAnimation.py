import qi
from naoqi import ALProxy, ALModule


class WaitingAnimation(ALModule):
    def __init__(self, robot):
        super(WaitingAnimation, self)
        session = robot.session
        self.tts = session.service("ALTextToSpeech")

    def start(self, robot, timeout):
        qi.async(self.count_to_zero_from, timeout)
        self.move_hands(robot)

    def count_to_zero_from(self, timeout):
        for x in range(0, timeout, 1):
            self.tts.say(str(timeout - x))

    @staticmethod
    def move_hands(robot):
        names = list()
        times = list()
        keys = list()

        names.append("HeadPitch")
        times.append([0.92, 0.96, 5.96])
        keys.append([[0.445059, [3, -0.32, 0], [3, 0.0133333, 0]], [0.445059, [3, -0.0133333, 0], [3, 1.66667, 0]],
                     [0.445059, [3, -1.66667, 0], [3, 0, 0]]])

        names.append("HeadYaw")
        times.append([0.92])
        keys.append([[-0.0366519, [3, -0.32, 0], [3, 0, 0]]])

        names.append("LElbowRoll")
        times.append([0.96, 5.96])
        keys.append([[-1.47263, [3, -0.333333, 0], [3, 1.66667, 0]], [-1.47263, [3, -1.66667, 0], [3, 0, 0]]])

        names.append("LElbowYaw")
        times.append([0.96, 5.96])
        keys.append([[-0.984828, [3, -0.333333, 0], [3, 1.66667, 0]], [-0.984828, [3, -1.66667, 0], [3, 0, 0]]])

        names.append("LHand")
        times.append([0.96, 5.96])
        keys.append([[0.979237, [3, -0.333333, 0], [3, 1.66667, 0]], [0.979237, [3, -1.66667, 0], [3, 0, 0]]])

        names.append("LShoulderPitch")
        times.append([0.96, 5.96])
        keys.append([[0.110484, [3, -0.333333, 0], [3, 1.66667, 0]], [0.110484, [3, -1.66667, 0], [3, 0, 0]]])

        names.append("LShoulderRoll")
        times.append([0.96, 5.96])
        keys.append([[0.0123425, [3, -0.333333, 0], [3, 1.66667, 0]], [0.0123425, [3, -1.66667, 0], [3, 0, 0]]])

        names.append("LWristYaw")
        times.append([0.96, 5.96])
        keys.append([[-1.81727, [3, -0.333333, 0], [3, 1.66667, 0]], [-1.81727, [3, -1.66667, 0], [3, 0, 0]]])

        names.append("RElbowRoll")
        times.append([0.96, 5.96])
        keys.append([[1.47254, [3, -0.333333, 0], [3, 1.66667, 0]], [1.47254, [3, -1.66667, 0], [3, 0, 0]]])

        names.append("RElbowYaw")
        times.append([0.96, 5.96])
        keys.append([[0.984828, [3, -0.333333, 0], [3, 1.66667, 0]], [0.984828, [3, -1.66667, 0], [3, 0, 0]]])

        names.append("RHand")
        times.append([0.96, 5.96])
        keys.append([[0.979237, [3, -0.333333, 0], [3, 1.66667, 0]], [0.979237, [3, -1.66667, 0], [3, 0, 0]]])

        names.append("RShoulderPitch")
        times.append([0.96, 5.96])
        keys.append([[0.110484, [3, -0.333333, 0], [3, 1.66667, 0]], [0.110484, [3, -1.66667, 0], [3, 0, 0]]])

        names.append("RShoulderRoll")
        times.append([0.96, 5.96])
        keys.append([[-0.0123425, [3, -0.333333, 0], [3, 1.66667, 0]], [-0.0123425, [3, -1.66667, 0], [3, 0, 0]]])

        names.append("RWristYaw")
        times.append([0.96, 5.96])
        keys.append([[1.81727, [3, -0.333333, 0], [3, 1.66667, 0]], [1.81727, [3, -1.66667, 0], [3, 0, 0]]])

        try:
            robot.ALMotion.angleInterpolationBezier(names, times, keys)
        except BaseException, err:
            print err

