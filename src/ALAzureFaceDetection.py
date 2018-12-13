
from PIL import Image
from io import BytesIO
from configuration import PepperConfiguration
import time

from cognitive_face import CognitiveFaceException
from pynaoqi_mate import Robot

from urllib2 import urlopen

import cognitive_face as CF
import logging


class azureImageWraper():
    def __init__(self, image_data):
        self.image_data = image_data

    def read(self):
        return self.image_data

class ALAzureFaceDetection():
    def __init__(self, myrobot):
        self.robot = myrobot
        self.camera = self.robot.ALPhotoCapture
        self.session = myrobot.session
        self.video_service = self.session.service("ALVideoDevice")
        self._serviceID = "Test"

        # Initialize Azure Face Service Connection
        CF.Key.set('5b1af2b251ee48f99c425e0c216ce013')
        CF.BaseUrl.set('https://westeurope.api.cognitive.microsoft.com/face/v1.0/')
        self.personGroupID = 'hideandseek_01'

        # Initialize Naoqi Camera Service
        self.path = "/home/nao/hs18_hideandseek/"
        self.fileName ="temp.jpg"
        self.camera.setResolution(4)
        self.camera.setColorSpace(11)

        # Initialize Logging
        logging.getLogger().setLevel(logging.INFO)
        logging.info('ALAzureFaceDetection initialized')

        self.subscribe()

    def detectIdentifyAndReturnNameIfPersonKnown(self, threshold):
        # type: (float) -> str
        """
        Uses the Microsoft AZURE Face API to detect a Person in the FOV of the Robot and checkes if
        the Person is already known in the Face Database.

        :param threshold: Minimal confidence required to decide if person is known
        :return: PersistedFaceID as str. None if Person is not known or is no person was detected
        """
        wrapper = self.getPictureFromCamera3()
        faceDetectResult = CF.face.detect(wrapper)

        if len(faceDetectResult) == 0:
            logging.warning("No Face detected")
            return None
        else:
            faceIdentifyResult = self.identifyPerson(faceDetectResult)
            if len(faceIdentifyResult[0]['candidates']) == 0:
                logging.info("No valid candidate was detected")
                return None
            elif faceIdentifyResult[0]['candidates'][0]['confidence'] < float(threshold):
                logging.info("Face was identified but confidence was below set threshold")
                return None
            else:
                persistedPersonID = str(faceIdentifyResult[0]['candidates'][0]['personId'])
                personInfo = CF.person.get(self.personGroupID, persistedPersonID)
                return personInfo['name']




    def detectIfFaceIDIsInSight(self, persistedFaceID):
        """
        Takes a Picture and checks if the given persisted PersonID is in the FOV of the Robot

        :param persistedFaceID: The AZURE persistedFaceID to detect
        :return: bool if face was detected
        """
        # type: (object) -> object

        wrapper = self.getPictureFromCamera3()
        faceDetectResults = CF.face.detect(wrapper)

        if len(faceDetectResults) == 0:
            logging.warning("No Face detected")
            return False

        else:
            faceIdentifyResult = self.identifyPerson(faceDetectResults)
            if len(faceIdentifyResult[0]['candidates']) == 0:
                return False
            else:
                for candidate in faceIdentifyResult[0]['candidates']:
                    if str(candidate['personId']) == str(persistedFaceID):
                        return True
                    else:
                        return False



    def learnFace(self, threshold, displayName):
        """
        Takes a picture from the Camera and detects faces in FOV of Pepper. If the person is already know to the AZURE Face API
        the picture is added to the associated face. If the person is unknown, a new persistedUserID is created.

        :param threshold: Minimal confidence required to decide if person is already known
        :param displayName:
        :return: persistedFaceID of the detected Person
        """
        # type: (float, str) -> str

        wrapper = self.getPictureFromCamera3()
        faceDetectResults = CF.face.detect(wrapper)


        if len(faceDetectResults) == 0:
            logging.warning("learnFace - No Face found to learn")
            return None

        elif len(faceDetectResults) >= 1:
            faceIdentifyResult = self.identifyPerson(faceDetectResults)
            if len(faceIdentifyResult[0]['candidates']) == 0:

                logging.info("The person is unknown to the Azure Service")
                personID = str(CF.person.create(self.personGroupID, displayName)['personId'])
                CF.person.add_face(wrapper, self.personGroupID, personID)
                return personID

            else:
                if faceIdentifyResult[0]['candidates'][0]['confidence'] < float(threshold):
                    personID = str(CF.person.create(self.personGroupID, displayName)['personId'])
                    CF.person.add_face(wrapper, self.personGroupID, personID)
                    return personID

                else:
                    CF.person.add_face(wrapper,
                                       self.personGroupID,
                                       str(faceIdentifyResult[0]['candidates'][0]['personId']),
                                       )
                    return str(faceIdentifyResult[0]['candidates'][0]['personId'])


        else:
            logging.warning("There where " + str(len(faceDetectResults)) +
                                 " detected. The program can't handle this many faces yet."
                                 )
            return None

    def identifyPerson(self, faceDetectResult):
        """
        Identifies the Person and returns a persistedFaceIDContainer if the person is known to the AZURE Service

        :param faceDetectResult:
        :return: Container with the results from AZURE
        """


        logging.info("Create new empty faceID list")
        faceIDs = []

        for face in faceDetectResult:
            logging.info("Added FaceID " + str(face['faceId']) + " Face Rectangle to faceID list")
            faceIDs.append(face['faceId'])

        if faceIDs == 0:
            logging.critical("No Face was found inside of faceDetectedResult")
            result = None
        else:
            logging.info("Send FaceId to Azure Face Service to identify Persons")

            result = CF.face.identify(faceIDs, self.personGroupID)

        return result


    def getPictureFromCamera(self):
        """
        Gets a Picture from a mjpeg camera source

        :return: Wrapper which implements a .read() Method to be able to pass the picture infos to AZURE without saveing it local
        """
        stream = urlopen('http://192.168.1.110:8080/video/mjpeg')
        byt = bytes()
        exit = False
        while not exit:
            byt += stream.read(1024)
            a = byt.find(b'\xff\xd8')
            b = byt.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = byt[a:b + 2]
                byt = byt[b + 2:]
                exit = True

        wrapper = azureImageWraper(jpg)
        return wrapper

    def getPictureFromCamera2(self):
        """
        Gets picture from Pepper Camera by saving it on the robot

        :return: path to the localy safed image
        """
        self.camera.takePicture(self.path, self.fileName)
        return str(self.path + self.fileName)

    def getPictureFromCamera3(self):
        """
        Gets picture from Pepper Camera without saving it to a file


        :return: Wrapper which implements a .read() Method to be able to pass the picture infos to AZURE without saveing it local
        """
        # Get Image from Pepper
        naoImage = self.video_service.getImageRemote(self.video_client)

        #Extract Image Information
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        array = naoImage[6]
        image_string = str(bytearray(array))
        # Create Image from Immage Information
        image = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)



        with BytesIO() as output:
            image.save(output, format="JPEG")
            wrapper = azureImageWraper(output.getvalue())

        return wrapper

    def subscribe(self):
        self.video_client = self.video_service.subscribeCamera(self._serviceID,
                                                          0,
                                                          3,
                                                          11,
                                                          10
                                                          )

    def unregister(self):
        self.video_service.unsubscribe(self.video_client)

    def __createFileLikeFromImageData__(self):
        pass

    def trainPersonGroup(self):
        CF.person_group.train(self.personGroupID)

    def forgetPerson(self, personGroupID, personID):
        """
        Delete a Person from a Person-Group including all the persisted Pictures of that Person.
        If an Error occurs, the Program does log the Error and continues running

        Args:
            :param personGroupID: ID of the Person-Group from which a Person should be deleted
            :param personID: ID of the Person who should be deleted

        Returns:
            No Return
        """

        try:
            CF.person.delete(personGroupID, personID)
            logging.info("Person was deleted successful")
        except CognitiveFaceException:
            pass
            logging.error("Error occured during deletion of Person. Continue Program.")

    def deletePersonGroup(self):
        """
        Delete a Person-Group including all the persisted Persons inside of that Groupe.
        If an CognitiveFaceException occurs, the Program does log the Exception and continues
        running

        Args:
            :param personGroupID: ID of the Person-Group which should be deleted

        Returns:
            No Return
        """

        try:
            CF.person_group.delete(self.personGroupID)
            logging.info("Person was deleted successful")
        except CognitiveFaceException:
            pass
            logging.error("Error occured during deletion of Person. Continue Program.")

    def initPersonGroup(self, personGroupID, personGroupName):
        CF.person_group.create(personGroupID, personGroupName)

    def __initCamera__(self, serviceI_id):
        pass

    def forgetPerson(self):
        pass

if __name__ == "__main__":
    config = PepperConfiguration("Amber", "localhost", 9559)
    robot = Robot(config)
    fd = ALAzureFaceDetection(robot)
    personId = fd.learnFace(0.6, "Flavio")
    fd.trainPersonGroup()
    print "Face learned"
    time.sleep(5)
    print "Face detection started"
    for _ in range(5):
        result = fd.detectIfFaceIDIsInSight(personId)
        print result

