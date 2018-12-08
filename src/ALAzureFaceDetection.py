from PIL import Image
from io import BytesIO
from configuration import PepperConfiguration
import time

from cognitive_face import CognitiveFaceException
from pynaoqi_mate import Robot

import cognitive_face as CF
import logging


class ALAzureFaceDetection():
    def __init__(self, myrobot):
        self.robot = myrobot
        self.camera = self.robot.ALPhotoCapture
        self.session = myrobot.session

        # Initialize Azure Face Service Connection
        CF.Key.set('5b1af2b251ee48f99c425e0c216ce013')
        CF.BaseUrl.set('https://westeurope.api.cognitive.microsoft.com/face/v1.0/')
        self.personGroupID = 'hideandseek_01'

        # Initialize Naoqi Camera Service
        self.path = "/home/nao/hs18_hideandseek/"
        self.fileName ="temp.jpg"
        self.camera.setResolution(3)
        self.camera.setColorSpace(9)

        # Initialize Logging
        logging.getLogger().setLevel(logging.WARNING)
        logging.info('ALAzureFaceDetection initialized')


    def detectIfFaceIDIsInSight(self, persistedFaceID):

        imagePath = self.getPictureFromCamera()
        faceDetectResults = CF.face.detect(imagePath)

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

        filePath = self.getPictureFromCamera()
        faceDetectResults = CF.face.detect(filePath)

        image = open(self.path+self.fileName, "rb")

        if len(faceDetectResults) == 0:
            logging.warning("learnFace - No Face found to learn")
            return None

        elif len(faceDetectResults) >= 1:
            faceIdentifyResult = self.identifyPerson(faceDetectResults)
            if len(faceIdentifyResult[0]['candidates']) == 0:

                logging.info("The person is unknown to the Azure Service")
                personID = str(CF.person.create(self.personGroupID, displayName)['personId'])
                CF.person.add_face(filePath, self.personGroupID, personID)
                return personID

            else:
                if faceIdentifyResult[0]['candidates'][0]['confidence'] < float(threshold):
                    personID = str(CF.person.create(self.personGroupID, displayName)['personId'])
                    CF.person.add_face(image, self.personGroupID, personID)
                    return personID

                else:
                    CF.person.add_face(filePath,
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

            result = CF.face.identify(faceIDs, self.personGroupID, )

        return result

    def getPictureFromCamera(self):
        self.camera.takePicture(self.path, self.fileName)
        return str(self.path + self.fileName)

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

