from naoqi import ALBroker, ALModule
import time

class PepperFaceRecognition(ALModule):
    # naoqi sessions
    tts = None
    memory = None
    subscriber = None
    video_service = None

    # search options
    scanning = False
    searched_person = None
    adding_person = False

    isalreadydetecting = False

    def __init__(self, name, session):
        ALModule.__init__(self, name)
        self.session = session
        self.tts = session.service("ALTextToSpeech")
        self.face_recon = session.service("ALFaceDetection")
        self.video_service = session.service("ALVideoDevice")
        self.tablet = session.service("ALTabletService")

        self.memory = session.service("ALMemory")
        self.subscriber = self.memory.subscriber("FaceDetected")
        self.face_recon.subscribe(name)
        isalreadydetecting = 0
        self.subscriber.signal.connect(self.faceCallback)

    def faceCallback(self, *_args):
        """Callback method for faceDetected"""

        if not self.isalreadydetecting:
            self.isalreadydetecting = True
            self.tts.say('hello, im taking a picture')
            time.sleep(1)
            self.tts.say("Snap")
            responsedetect = afa.detectFaceBinary(picture_path[0])

            if (responsedetect == "fehler keine person erkannt"):
                self.tts.say('Sorry i could not recognize a face')
                time.sleep(2)
                self.isalreadydetecting = False  # TODO change with google

            responseidentify = afa.identifyFace(responsedetect)

            if (responseidentify == "person nicht bekannt"):
                self.tts.say("I dont know you yet. Do you want to tell me your name?")
                self.newPerson()
            else:
                self.tts.say("I'm looking for your name")
                personName = afa.getPerson(responseidentify)
                self.tts.say("hello" + personName);
                self.tts.say("Have a nice day " + personName)

                time.sleep(2)
                self.isalreadydetecting = False  # TODO change with google

            time.sleep(5)

