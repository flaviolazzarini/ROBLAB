import time

import numpy as np
import qi

from naoqi import ALModule

from FaceRecognition import FaceRecognition
from PepperTabletDialogHandler import PepperTabletDialogHandler
from FaceLearning import FaceLearning
from WaitingAnimation import WaitingAnimation
from obstacleAvoidance import ObstacleAvoidance
from FaceTracker import FaceTracker
from Exploration import Exploration
from MapSearcher import start_search


class HideNSeek(ALModule):
    def __init__(self, robot):
        super(HideNSeek, self)
        self.robot = robot
        self.session = robot.session
        self.memory = self.session.service("ALMemory")
        # Face Recognition
        self.faceRecognition = FaceRecognition(robot)
        self.learnFace = FaceLearning(robot)
        self.tablet = PepperTabletDialogHandler(self.robot)
        self.tracker = FaceTracker(self.robot)
        self.tracker.stop_face_tracking()
        self._person_to_search = None

        # Speech Service
        self.tts = self.session.service("ALTextToSpeech")

        #start robot
        self.motion = self.session.service("ALMotion")
        self.motion.wakeUp()

    def run(self):
        print "Starting HideNSeek"
        face_learned = False
        while not face_learned:
            known_face, person_name = self.faceRecognition.search_face_blocking()
            if not known_face:
                self.tts.say("I don't know you yet, what is your name?")
                person_name = self.tablet.show_input_text_dialog_blocking("What's your name?")
                print person_name
                self.tts.say("Look me in the eyes. I'm learning your face")
                time.sleep(1)
                face_learned = self.learnFace.learn_face_blocking(person_name)
                print face_learned
                if not face_learned:
                    self.tts.say("I was to stupid to learn your face")
                    self.tts.say("Let's try again")
                    face_learned = False
                    person_name = ""
                    # TODO: Reset facereco, tablet, ...

        self.tts.say("I learned your face")
        self._person_to_search = person_name
        person_name = None
        self.tts.say("Hello " + self._person_to_search + ". Let's play")

        animation = WaitingAnimation()
        animation.start(self.robot, 10)
        exploration = Exploration(self.robot)
        exploration.relocate_in_map([0, 0])
        map = exploration.get_current_map()
        learn_layer = np.zeros(np.array(map).shape)
        qi.async(start_search, exploration, map, learn_layer, delay=0)
        # obstacleAvoidance = ObstacleAvoidance(self.robot)
        # obstacleAvoidance.move_to_concurrently()

        while person_name != self._person_to_search:
            print "searching()"
            known_face, person_name = self.faceRecognition.search_face_blocking()
            self.tracker.start_face_tracking()
        self.tracker.move_to_target()
        # obstacleAvoidance.set_found(True)
        self.tts.say("Found you " + person_name)
        time.sleep(0)
        self.tracker.stop_face_tracking()

