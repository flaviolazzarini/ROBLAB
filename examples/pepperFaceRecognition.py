import socket

import qi
import time
import sys
from Calendar import Calendar
from VoiceRecognition import VoiceRecognition
from MyStrom import MyStrom

import numpy as np

from naoqi import ALModule, ALBroker

from azureFaceAPI import azureFaceAPI


class pepperFaceRecognition(ALModule):
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
            picture_path = photoCapture.takePicture(record_folder, file_name, overwrite=True)
            self.tts.say("Snap")
            print(picture_path[0])
            responsedetect = afa.detectFaceBinary(picture_path[0])

            if(responsedetect == "fehler keine person erkannt"):
                self.tts.say('Sorry i could not recognize a face')
                time.sleep(2)
                self.isalreadydetecting = False #TODO change with google

            responseidentify = afa.identifyFace(responsedetect)

            if(responseidentify == "person nicht bekannt"):
                self.tts.say("I dont know you yet. Do you want to tell me your name?")
                self.newPerson()
            else:
                self.tts.say("I'm looking for your name")
                personName = afa.getPerson(responseidentify)
                self.tts.say("hello" +personName);

                if personName == "luca":
                    self.tts.say("I'm preparing your work place")
                    mystrom = MyStrom()
                    mystrom.turn_mystrom_on("192.168.1.193")

                self.tts.say("Have a nice day " + personName)

                time.sleep(2)
                self.isalreadydetecting = False #TODO change with google

            time.sleep(5)



    def newPerson(self):
        self.tablet.showInputDialog("text", "What's your name?", "Save", "Cancel", "", 100)
        callbackId = session.service("ALTabletService").onInputText.connect(self.nameCallback)

    def nameCallback(self, button, text):

        if button == 1 and not self.adding_person:
            self.adding_person = True
            print("Hallo " + text)

            afa.addFaceBinary('/data/home/nao/recordings/cameras/luca.jpg',afa.createPerson(text))
            afa.traingroup()
            time.sleep(2)
            afa.trainingStatus()

            self.voice = VoiceRecognition(self.session)
            self.voice.set_callback(self.voiceCallback)
            self.voice.start_recognition()
        elif button == 0 and not self.adding_person:
            print("Bye " + text)
            time.sleep(2)
            self.isalreadydetecting = False #TODO change with google

    def voiceCallback(self, yes):
        self.voice.stop_recognition()
        if yes:

            cal = Calendar(self.session)
            cal.step_1_request_device_code()
            cal.step_2_show_device_code()
            cal.step_3_poll_for_authorization()
            if cal._access_token != "":
                cal.step4_get_calendar()
                cal.step5_get_next_event()
        else:
            pass

        time.sleep(10)
        self.adding_person = False
        self.isalreadydetecting = False




if __name__ == '__main__':
    time.sleep(10)
    connect_ip = '192.168.1.102'
    connection_url = connect_ip+':9559'

    myBroker = ALBroker("myBroker",
                        "0.0.0.0",  # listen to anyone
                        0,  # find a free port and use it
                        connect_ip,  # parent broker IP
                        9559)  # parent broker port
    app = qi.Application(["--qi-url=" + connection_url])  # Connection to robot
    app.run()
    session = app.session
    global FaceRec

    afa = azureFaceAPI()
    photoCapture = session.service("ALPhotoCapture")
    record_folder = "/data/home/nao/recordings/cameras/"
    file_name = "luca.jpg"
    resolution_map = {
        '160 x 120': 0,
        '320 x 240': 1,
        '640 x 480': 2,
        '1280 x 960': 3
    }
    camera_map = {
        'Top': 0,
        'Bottom': 1
    }
    photoCapture.setResolution(resolution_map['1280 x 960'])
    photoCapture.setCameraID(camera_map['Top'])
    photoCapture.setPictureFormat("jpg")

    FaceRec = pepperFaceRecognition('FaceRecognition', session)
    # img = FaceRec.grayscale_img()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)