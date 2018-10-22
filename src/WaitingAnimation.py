from time import sleep

import qi
from naoqi import ALModule


class WaitingAnimation(ALModule):
    def __init__(self, robot):
        super(WaitingAnimation, self)
        session = robot.session
        self.tts = session.service("ALTextToSpeech")

    def start(self, robot, timeout):
        qi.async(self.move_hands, robot)
        self.count_to_zero_from(timeout)

    def count_to_zero_from(self, timeout):
        for x in range(0, timeout, 1):
            self.tts.say(str(timeout - x))
            sleep(.2)
        self.tts.say('ready or not, here I come');

    @staticmethod
    def move_hands(robot):
        names = list()
        times = list()
        keys = list()

        names.append("HeadPitch")
        times.append([0.92, 0.96, 9.16, 11.12])
        keys.append([[0.445059, [3, -0.32, 0], [3, 0.0133333, 0]], [0.445059, [3, -0.0133333, 0], [3, 2.73333, 0]],
                     [0.445059, [3, -2.73333, 0], [3, 0.653333, 0]], [-0.377458, [3, -0.653333, 0], [3, 0, 0]]])

        names.append("HeadYaw")
        times.append([0.92, 11.12])
        keys.append([[-0.0366519, [3, -0.32, 0], [3, 3.4, 0]], [0.0183193, [3, -3.4, 0], [3, 0, 0]]])

        names.append("LElbowRoll")
        times.append([0.96, 9.16, 11.12])
        keys.append([[-1.47263, [3, -0.333333, 0], [3, 2.73333, 0]], [-1.47263, [3, -2.73333, 0], [3, 0.653333, 0]],
                     [-0.109855, [3, -0.653333, 0], [3, 0, 0]]])

        names.append("LElbowYaw")
        times.append([0.96, 9.16, 11.12])
        keys.append([[-0.984828, [3, -0.333333, 0], [3, 2.73333, 0]], [-0.984828, [3, -2.73333, 0], [3, 0.653333, 0]],
                     [-1.71671, [3, -0.653333, 0], [3, 0, 0]]])

        names.append("LHand")
        times.append([0.96, 9.16, 11.12])
        keys.append([[0.979237, [3, -0.333333, 0], [3, 2.73333, 0]], [0.979237, [3, -2.73333, 0], [3, 0.653333, 0]],
                     [0.6942, [3, -0.653333, 0], [3, 0, 0]]])

        names.append("LShoulderPitch")
        times.append([0.96, 9.16, 11.12])
        keys.append([[0.110484, [3, -0.333333, 0], [3, 2.73333, 0]], [0.110484, [3, -2.73333, 0], [3, 0.653333, 0]],
                     [1.77102, [3, -0.653333, 0], [3, 0, 0]]])

        names.append("LShoulderRoll")
        times.append([0.96, 9.16, 11.12])
        keys.append([[0.0123425, [3, -0.333333, 0], [3, 2.73333, 0]], [0.0123425, [3, -2.73333, 0], [3, 0.653333, 0]],
                     [0.103043, [3, -0.653333, 0], [3, 0, 0]]])

        names.append("LWristYaw")
        times.append([0.96, 9.16, 11.12])
        keys.append([[-1.81727, [3, -0.333333, 0], [3, 2.73333, 0]], [-1.81727, [3, -2.73333, 0], [3, 0.653333, 0]],
                     [0.0346901, [3, -0.653333, 0], [3, 0, 0]]])

        names.append("RElbowRoll")
        times.append([0.96, 9.16, 11.12])
        keys.append([[1.47254, [3, -0.333333, 0], [3, 2.73333, 0]], [1.47254, [3, -2.73333, 0], [3, 0.653333, 0]],
                     [0.0985442, [3, -0.653333, 0], [3, 0, 0]]])

        names.append("RElbowYaw")
        times.append([0.96, 9.16, 11.12])
        keys.append([[0.984828, [3, -0.333333, 0], [3, 2.73333, 0]], [0.984828, [3, -2.73333, 0], [3, 0.653333, 0]],
                     [1.68655, [3, -0.653333, 0], [3, 0, 0]]])

        names.append("RHand")
        times.append([0.96, 9.16, 11.12])
        keys.append([[0.979237, [3, -0.333333, 0], [3, 2.73333, 0]], [0.979237, [3, -2.73333, 0], [3, 0.653333, 0]],
                     [0.688049, [3, -0.653333, 0], [3, 0, 0]]])

        names.append("RShoulderPitch")
        times.append([0.96, 9.16, 11.12])
        keys.append([[0.110484, [3, -0.333333, 0], [3, 2.73333, 0]], [0.110484, [3, -2.73333, 0], [3, 0.653333, 0]],
                     [1.74858, [3, -0.653333, 0], [3, 0, 0]]])

        names.append("RShoulderRoll")
        times.append([0.96, 9.16, 11.12])
        keys.append([[-0.0123425, [3, -0.333333, 0], [3, 2.73333, 0]], [-0.0123425, [3, -2.73333, 0], [3, 0.653333, 0]],
                     [-0.104964, [3, -0.653333, 0], [3, 0, 0]]])

        names.append("RWristYaw")
        times.append([0.96, 9.16, 11.12])
        keys.append([[1.81727, [3, -0.333333, 0], [3, 2.73333, 0]], [1.81727, [3, -2.73333, 0], [3, 0.653333, 0]],
                     [-0.0374315, [3, -0.653333, 0], [3, 0, 0]]])

        try:
            robot.ALMotion.angleInterpolationBezier(names, times, keys)
        except BaseException, err:
            print err

