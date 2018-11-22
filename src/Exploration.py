import numpy
import array as arr

from MapHelper import array_to_bw_bitmap


class Exploration:
    def __init__(self, robot):
        session = robot.session
        self.navigation = session.service("ALNavigation")

    def explore(self, radius):
        error_code = self.navigation.explore(radius)
        if error_code != 0:
            print "Exploration failed."
            return

        path = self.navigation.saveExploration()
        print "Exploration saved at path: \"" + path + "\""

        self.navigation.startLocalization()
        self.move_to_origin()
        return path

    def move_to_in_map(self, position):
        errorcode = self.navigation.navigateToInMap(position)
        if(errorcode != 0):
            raise EnvironmentError("could not navigate to position " + position)

    def navigate_to(self, x, y):
        successfull = self.navigation.navigateTo(x, y)
        if successfull == False:
            raise EnvironmentError("could not navigate to position (" + str(x) + " / " + str(y) + ")")

    def move_to_origin(self):
        self.move_to_in_map([0., 0., 0.])

    def get_current_position_in_map_array(self):
        result_map = self.navigation.getMetricalMap()
        map_meters_per_pixel = result_map[0]
        map_width = result_map[1]
        map_height = result_map[2]

        width_offset = int(map_width/2)
        height_offset = int(map_height/2)

        position = self.get_current_position()

        x_offset_in_pixels = (position[0] / map_meters_per_pixel)
        y_offset_in_pixels = (position[1] / map_meters_per_pixel)
        return [int(width_offset + x_offset_in_pixels), int(height_offset + y_offset_in_pixels)]

    def get_current_position(self):
        pose = self.navigation.getRobotPositionInMap()
        xy_position = arr.array('f', [pose[0][0], pose[0][1]])
        return xy_position

    def save_current_map_as_bw_image(self, path):
        result_map = self.navigation.getMetricalMap()
        map_width = result_map[1]
        map_height = result_map[2]
        img = numpy.array(result_map[4]).reshape(map_width, map_height)
        img = (100 - img) * 2.55  # from 0..100 to 255..0
        array_to_bw_bitmap(img, path)

    def get_current_map(self):
        result_map = self.navigation.getMetricalMap()
        map_width = result_map[1]
        map_height = result_map[2]
        map = numpy.array(result_map[4]).reshape(map_width, map_height)
        return map

    def get_current_map_meters_per_pixel(self):
        return self.navigation.getMetricalMap()[0]

    def load_map(self, path):
        self.navigation.stopLocalization()
        self.navigation.stopExploration()
        self.navigation.loadExploration(path)
        guess = [0., 0.] # assuming the robot is not far from the place where he started the loaded exploration.
        self.navigation.relocalizeInMap(guess)
        self.navigation.startLocalization()

    def relocate_in_map(self, guess):
        self.navigation.relocalizeInMap(guess)
