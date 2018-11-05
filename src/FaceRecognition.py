import sys

import qi
from naoqi import ALBroker, ALModule
import time
from WaitingAnimation import WaitingAnimation
from PepperTabletDialogHandler import PepperTabletDialogHandler
from obstacleAvoidance import ObstacleAvoidance

class FaceRecognition(ALModule):

    def __init__(self, robot):
        """
        Initialisation of qi framework and event detection.
        """
        super(FaceRecognition, self)
        self.robot = robot;
        self.session = robot.session
        # Get the service ALMemory.
        self.memory = self.session.service("ALMemory")

        # Connect the event callback.
        self.subscriber = self.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.on_human_tracked)
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = self.session.service("ALTextToSpeech")
        self.face_detection = self.session.service("ALFaceDetection")
        self.face_detection.subscribe("FaceRecognition")
        self.face_detection.setRecognitionConfidenceThreshold(0.3)
        self.speech_recognition = self.session.service("ALSpeechRecognition")
        self.motion = self.session.service("ALMotion")
        self.tracker = self.session.service("ALTracker")
        self.basicAwareness = self.session.service("ALBasicAwareness")
        self.motion.wakeUp()
        self.basicAwareness.setEnabled(False)
        self.name = ""
        self.obstacleAvoidance = None

        # If the speech recognition subscriber still keeps reacting
        for subscriber, period, prec in self.speech_recognition.getSubscribersInfo():
            self.speech_recognition.unsubscribe(subscriber)

        self.speech_recognition.setLanguage("English")
        self.tts.setLanguage("English")
        voci = ["yes", "no"]
        self.speech_recognition.setVocabulary(voci, False)
        self.subscriberSpeech = self.memory.subscriber("WordRecognized")
        self.subscriberSpeech.signal.connect(self.on_word_recognized)
        self.play = None

    def on_word_recognized(self, value):
        print value
        if value[0] == "yes":
            self.play = True
        else:
            if not self.play or self.play is None:
                self.play = False

        self.speech_recognition.unsubscribe("LetsPlay")
        self.subscriberSpeech = None

    def on_human_tracked(self, value):
        """
        Callback for event FaceDetected.
        """

        # Unsubscribe from to prevent multiple triggers
        self.subscriber = None
        self.face_detection.unsubscribe("FaceRecognition")
        self.play = None
        if not self.play or self.play is None:
            if value == []:  # empty value when the face disappears
                print "No face detected"
            else:
                print "I saw a face!"
                self.tts.say("Hello, do you wan't to play?")
                self.speech_recognition.subscribe("LetsPlay")
                while self.play is None:
                    time.sleep(2)

                if self.play:
                    # First Field = TimeStamp.
                    timeStamp = value[0]
                    print "TimeStamp is: " + str(timeStamp)

                    # Second Field = array of face_Info's.
                    faceInfoArray = value[1]

                    for j in range(len(faceInfoArray) - 1):
                        faceInfo = faceInfoArray[j]

                        # First Field = Shape info.
                        faceShapeInfo = faceInfo[0]

                        # Second Field = Extra info (empty for now).
                        faceExtraInfo = faceInfo[1]

                        if faceExtraInfo[2] == "":
                            self.tts.say("I don't know you yet, what is your name?")
                            tablet = PepperTabletDialogHandler(self.robot)
                            self.name = tablet.show_input_text_dialog_blocking("What's your name?");
                            print(self.name)
                            success = self.face_detection.learnFace(self.name)
                            print success
                            # if not success:
                            #     self.subscriber = self.memory.subscriber("FaceDetected")
                            #     self.subscriber.signal.connect(self.on_human_tracked)
                            #     self.face_detection.subscribe("FaceRecognition")
                            #     self.play = None
                            #     print success
                            #     return
                        else:
                            print faceExtraInfo[2]
                            self.name = faceExtraInfo[2]

                        self.tts.say("Hello " + self.name + ". Let's play!")
                        time.sleep(1)
                        animation = WaitingAnimation()
                        animation.start(self.robot, 10)


                        self.subscriber = self.memory.subscriber("FaceDetected")
                        self.subscriber.signal.connect(self.on_human_tracked2)
                        self.face_detection.subscribe("FaceRecognition")
                        self.obstacleAvoidance = ObstacleAvoidance(self.robot, self.motion)
                        qi.async(self.obstacleAvoidance.moveTo())

                        print "Face Infos :  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
                        print "Face Infos :  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])
                        print "Face Extra Infos :" + str(faceExtraInfo)
                else:
                    self.tts.say("Ok, we will play next time")
        print "test"
        self.subscriber = self.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.on_human_tracked)
        self.face_detection.subscribe("FaceRecognition")

    def on_human_tracked2(self, value):
        if value == []:  # empty value when the face disappears
            print "No face detected"
        else:
            self.subscriber = None
            self.face_detection.unsubscribe("FaceRecognition")
            faceInfoArray = value[1]

            for j in range(len(faceInfoArray) - 1):
                faceInfo = faceInfoArray[j]

                # First Field = Shape info.
                faceShapeInfo = faceInfo[0]

                # Second Field = Extra info (empty for now).
                faceExtraInfo = faceInfo[1]
                if faceExtraInfo[2] == self.name:
                    self.basicAwareness.startAwareness()
                    self.obstacleAvoidance.set_found(True)
                    self.tts.say("Gotcha! " + self.name)
                else:
                    self.subscriber = self.memory.subscriber("FaceDetected")
                    self.subscriber.signal.connect(self.on_human_tracked2)
                    self.face_detection.subscribe("FaceRecognition")

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting HumanGreeter"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping HumanGreeter"
            self.face_detection.unsubscribe("HumanGreeter")
            self.basicAwareness.setEnabled(False)
            # stop
            sys.exit(0)
