from PIL import Image
from configuration import PepperConfiguration
from io import BytesIO

from cognitive_face import CognitiveFaceException
from pynaoqi_mate import Robot

from naoqi import ALModule
import cognitive_face as CF
import logging

#bla
class ALAzureFaceDetection(ALModule):
    def __init__(self, myrobot):
        self.session = myrobot.session

        # Initialize Azure Face Service Connection
        CF.Key.set('5b1af2b251ee48f99c425e0c216ce013')
        CF.BaseUrl.set('https://westeurope.api.cognitive.microsoft.com/face/v1.0/')
        self.personGroupID = 'hideandseek_01'

        # Initialize Naoqi Camera Service
        self._serviceID = "AzureService"
        self._AL_kTopCamera = 0
        self._AL_kQVGA = 1  # 320x240
        self._AL_kBGRColorSpace = 11
        self._AL_fps = 2
        self.video_service = self.session.service("ALVideoDevice")

        # Initialize Logging
        logging.info('ALAzureFaceDetection initialized')

    def detectIfFaceIDIsInSight(self, persistedFaceID):

        images = self.getPicturesFromCamera(1)

        images[0].save("./pictures/_temp.png", "PNG")
        faceDetectResults = CF.face.detect('./pictures/_temp.png')

        if len(faceDetectResults) == 0:
            logging.warning("No Face found to learn")
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

        images = self.getPicturesFromCamera(1)

        images[0].save("./pictures/_temp.png", "PNG")
        image = images[0]

        faceDetectResults = CF.face.detect('./pictures/_temp.png')


        if len(faceDetectResults) == 0:
            logging.warning("learnFace - No Face found to learn")
            return None

        elif len(faceDetectResults) >= 1:
            faceIdentifyResult = self.identifyPerson(faceDetectResults)
            if len(faceIdentifyResult[0]['candidates']) == 0:
                #self.logging.info("The person is unknown to the Azure Service")
                personID = str(CF.person.create(self.personGroupID, displayName)['personId'])
                CF.person.add_face('./pictures/_temp.png', self.personGroupID, personID)
                return personID

            else:
                if faceIdentifyResult[0]['candidates'][0]['confidence'] < float(threshold):
                    personID = str(CF.person.create(self.personGroupID, displayName)['personId'])
                    CF.person.add_face(image, self.personGroupID, personID)
                    return personID

                else:
                    CF.person.add_face('./pictures/_temp.png',
                                       self.personGroupID,
                                       str(faceIdentifyResult[0]['candidates'][0]['personId']),
                                       )
                    return str(faceIdentifyResult[0]['candidates'][0]['personId'])


        else:
            #self.logging.warning("There where " + str(len(faceDetectResults)) +
            #                     " detected. The program can't handle this many faces yet."
            #                     )
            return None

    def identifyPerson(self, faceDetectResult):

        #self.logging.info("Create new empty faceID list")
        faceIDs = []

        for face in faceDetectResult:
            #self.logging.info("Added FaceID " + str(face['faceId']) + " Face Rectangle to faceID list")
            faceIDs.append(face['faceId'])

        if faceIDs == 0:
            #self.logging.critical("No Face was found inside of faceDetectedResult")
            result = None
        else:
            #self.logging.info("Send FaceId to Azure Face Service to identify Persons")

            result = CF.face.identify(faceIDs, self.personGroupID, )

        return result


    def getPicturesFromCamera(self, numberOfImagesToTake=1):
        video_client = self.video_service.subscribeCamera(self._serviceID,
                                                          self._AL_kTopCamera,
                                                          self._AL_kQVGA,
                                                          self._AL_kBGRColorSpace,
                                                          self._AL_fps
                                                          )

        images = []
        for _ in range(numberOfImagesToTake):

            # Get Image from Pepper
            naoImage = self.video_service.getImageRemote(video_client)

            #Extract Image Information
            imageWidth = naoImage[0]
            imageHeight = naoImage[1]
            array = naoImage[6]
            image_string = str(bytearray(array))

            # Create Image from Immage Information
            image = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)
            images.append(image)

        # Unsubscribe from Pepper
        self.video_service.unsubscribe(video_client)

        return images

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
            #self.logging.info("Person was deleted successful")
        except CognitiveFaceException:
            pass
            #self.logging.error("Error occured during deletion of Person. Continue Program.")

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
            #self.logging.info("Person was deleted successful")
        except CognitiveFaceException:
            pass
            #self.logging.error("Error occured during deletion of Person. Continue Program.")

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
    personId = fd.learnFace(0.5, "Bushi")
    fd.trainPersonGroup()

    for _ in range(5):
        result = fd.detectIfFaceIDIsInSight(personId)
        print result

