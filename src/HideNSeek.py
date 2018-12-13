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
from MapSearcher import start_random_search
import MapSearcher
from InitAnimation import InitAnimation
from ALAzureFaceDetection import ALAzureFaceDetection
from azureHumanDetector import AzureHumanDetector
from HeadInitAnimation import HeadInitAnimation
import logging


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
        #self.tracker.stop_face_tracking
        #self.tracker.start_face_tracking()
        self._person_to_search = None
        self.fd = ALAzureFaceDetection(self.robot)
        self.hd = AzureHumanDetector(self.robot)

        # Speech Service
        self.tts = self.session.service("ALTextToSpeech")

        #Basic Awareness
        self.basicAware = self.robot.ALBasicAwareness
        self.basicAware.startAwareness()
        self.basicAware.setEngagementMode("FullyEngaged")
        self.basicAware.setStimulusDetectionEnabled("People", True)
        self.basicAware.setStimulusDetectionEnabled("Sound", True)
        self.basicAware.setTrackingMode("Head")

        # start robot
        self.motion = self.session.service("ALMotion")
        self.motion.wakeUp()
        self.initAnimation = InitAnimation()
        self.initAnimation.start(self.robot)
        logging.getLogger().setLevel(logging.WARNING)

    def run(self):
        print "Starting HideNSeek"
        face_learned = False
        while not face_learned:
            while not self.hd.detect_if_people_are_in_sight():
                pass

            personKnown = self.fd.detectIdentifyAndReturnNameIfPersonKnown(0.5)

            # known_face, person_name = self.faceRecognition.search_face_blocking()
            print("after search face")
            if personKnown is None:
                self.tts.say("I don't know you yet, what is your name?")
                person_name = self.tablet.show_input_text_dialog_blocking("What's your name?")
                print person_name
                self.tts.say("Look me in the eyes. I'm learning your face")
                time.sleep(1)
                personId = self.fd.learnFace(0.7, person_name)
                if personId is not None:
                    self.fd.trainPersonGroup()
                    face_learned = True
                # if not face_learned:
                #  self.tts.say("I was to stupid to learn your face")
                #  self.tts.say("Let's try again")
                #  face_learned = False
                #  person_name = ""
            else:
                person_name = personKnown
                self.tts.say("I know you already " + personKnown)
                self.tts.say("Look me in the eyes. I am improving my face recognition")

                time.sleep(1)
                personId = self.fd.learnFace(0.7, personKnown)

                if personId is not None:
                    self.fd.trainPersonGroup()
                    face_learned = True


        self.tts.say("I learned your face")
        self._person_to_search = person_name
        self.tts.say("Hello " + self._person_to_search + ". Let's play")
        self.basicAware.setEngagementMode("Unengaged")

        animation = WaitingAnimation()
        animation.start(self.robot, 10)
        self.initAnimation.start(self.robot)
        exploration = Exploration(self.robot)
        qi.async(MapSearcher.start_random_search, exploration)

        map = exploration.get_current_map()
        motion = self.session.service("ALMotion")
        #qi.async(start_search, exploration, map, delay=0)
        qi.async(start_random_search, exploration,motion)
        # obstacleAvoidance = ObstacleAvoidance(self.robot)
        # obstacleAvoidance.move_to_concurrently()

        print "Start with found Methode"
        found = False
        while not found:
            #known_face, person_name = self.faceRecognition.search_face_blocking()
            #self.tracker.start_face_tracking())
            found = self.fd.detectIfFaceIDIsInSight(personId)
            #self.tracker.stop_face_tracking()

        MapSearcher.IS_FINISHED = True
        self.fd.unregister()
        # self.tracker.move_to_target()
        # obstacleAvoidance.set_found(True)
        self.tts.say("Found you " + person_name)
        time.sleep(0)
        # self.tracker.stop_face_tracking()

