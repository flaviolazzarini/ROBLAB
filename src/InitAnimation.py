from time import sleep
import qi


class InitAnimation():

    def start(self, robot):
        qi.async(self.move_hands, robot)

    @staticmethod
    def move_hands(robot):
        names = list()
        times = list()
        keys = list()

        names.append("HeadPitch")
        times.append([0.96])
        keys.append([-0.18101])

        names.append("HeadYaw")
        times.append([0.96])
        keys.append([0.0184078])

        names.append("HipPitch")
        times.append([0.96])
        keys.append([-0.0720971])

        names.append("HipRoll")
        times.append([0.96])
        keys.append([-0.00613594])

        names.append("KneePitch")
        times.append([0.96])
        keys.append([0.0122719])

        names.append("LElbowRoll")
        times.append([0.96])
        keys.append([-0.119651])

        names.append("LElbowYaw")
        times.append([0.96])
        keys.append([-1.71959])

        names.append("LHand")
        times.append([0.96])
        keys.append([0.689807])

        names.append("LShoulderPitch")
        times.append([0.96])
        keys.append([1.76254])

        names.append("LShoulderRoll")
        times.append([0.96])
        keys.append([0.111981])

        names.append("LWristYaw")
        times.append([0.96])
        keys.append([0.00149202])

        names.append("RElbowRoll")
        times.append([0.96])
        keys.append([0.102777])

        names.append("RElbowYaw")
        times.append([0.96])
        keys.append([1.68431])

        names.append("RHand")
        times.append([0.96])
        keys.append([0.692443])

        names.append("RShoulderPitch")
        times.append([0.96])
        keys.append([1.75027])

        names.append("RShoulderRoll")
        times.append([0.96])
        keys.append([-0.110447])

        names.append("RWristYaw")
        times.append([0.96])
        keys.append([-0.021518])

        try:
            robot.ALMotion.angleInterpolationBezier(names, times, keys)
        except BaseException, err:
            print err
