import numpy
from PIL import Image
import array as arr

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
        self.navigation.navigateToInMap(position)

    def move_to_origin(self):
        self.move_to_in_map([0., 0., 0.])

    def get_current_map_as_array(self):
        result_map = self.navigation.getMetricalMap()
        map_width = result_map[1]
        map_height = result_map[2]
        img = numpy.array(result_map[4]).reshape(map_width, map_height)
        return img

    def get_current_pixel(self):
        result_map = self.navigation.getMetricalMap()
        map_width = result_map[1]
        map_height = result_map[2]

        width_offset = int(map_width/2)
        height_offset = int(map_height/2)

        position = self.get_current_position()

        return [width_offset + position[0], height_offset + position[1]]

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
        img = numpy.array(img, numpy.uint8)
        result = Image.frombuffer('L', (map_width, map_height), img, 'raw', 'L', 0, 1)
        result.save(path)

    def load_map(self, path):
        self.navigation.stopLocalization()
        self.navigation.stopExploration()
        self.navigation.loadExploration(path)
        guess = [0., 0.] # assuming the robot is not far from the place where he started the loaded exploration.
        self.navigation.relocalizeInMap(guess)
        self.navigation.startLocalization()
