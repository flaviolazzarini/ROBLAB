import qi


class HeadInitAnimation():

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


        try:
            robot.ALMotion.angleInterpolationBezier(names, times, keys)
        except BaseException, err:
            print err
