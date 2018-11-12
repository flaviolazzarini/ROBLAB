import sys
import time

from naoqi import ALModule

from FaceRecognition import FaceRecognition
from PepperTabletDialogHandler import PepperTabletDialogHandler
from FaceLearning import FaceLearning


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

        # Speech Service
        self.tts = self.session.service("ALTextToSpeech")

        #start robot
        self.motion = self.session.service("ALMotion")
        self.motion.wakeUp()

    def run(self):
        print "Starting HideNSeek"
        known_face, person_name = self.faceRecognition.search_face_blocking()
        self.faceRecognition = None
        if known_face:
            self.tts.say("Hello " + person_name)
        else:
            self.tts.say("I don't know you yet, what is your name?")
            person_name = self.tablet.show_input_text_dialog_blocking("What's your name?")
            print person_name
            self.tts.say("Look me in the eyes. I'm learning your face")
            time.sleep(1)
            face_learned = self.learnFace.learn_face_blocking(person_name)
            if face_learned:
                self.tts.say("I learned your face")
            else:
                self.tts.say("I was not able to learn your face")
                # TODO: save logic

