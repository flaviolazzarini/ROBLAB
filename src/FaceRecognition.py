
import qi
from time import sleep
import concurrent.futures


class FaceRecognition(object):

    def __init__(self, robot):
        """
        Initialisation of qi framework and event detection.
        """
        # Get the service ALMemory.
        self.session = robot.session
        #self._app.session.registerService("FaceRec", FaceRecognition())
        self.memory = self.session.service("ALMemory")
        self.subscriber = None
        self.face_detection = None
        self._knownFace = None
        self._name = None
        self._person_seen = False
        self._subscribed = False

    def search_face_blocking(self, timeout=None):
        return self.__search_face_logic()
        # future = self.search_face_concurrently()
        # return future.wait()

    def __search_face_logic(self):
        try:
            self.subscribe()
            print("search_face_logic")
            while not self._person_seen:
                sleep(0.1)
            self._person_seen = False
        except Exception, e:
            print "Error: ", e

        return self.__get_result_and_reset()

    def __get_result_and_reset(self):

        return self._knownFace, self._name

    def on_human_tracked(self, value):
        """
        Callback for event FaceDetected.
        """
        # Unsubscribe from to prevent multiple triggers
        self.unsubscribe()

        if value != []:  # empty value when the face disappears

            # Second Field = array of face_Info's.
            faceInfoArray = value[1]

            for j in range(len(faceInfoArray) - 1):
                faceInfo = faceInfoArray[j]

                # First Field = Shape info.
                faceShapeInfo = faceInfo[0]

                # Second Field = Extra info (empty for now).
                faceExtraInfo = faceInfo[1]

                if faceExtraInfo[2] == "":
                    self._knownFace = False

                else:
                    self._knownFace = True
                    self._name = faceExtraInfo[2]
            self._person_seen = True
        else:
            if not self._subscribed:
                self.subscribe()

    def subscribe(self):
        if not self._subscribed:
            self.subscriber = self.memory.subscriber("FaceDetected")
            self.subscriber.signal.connect(self.on_human_tracked)
            self.face_detection = self.session.service("ALFaceDetection")
            self.face_detection.setRecognitionConfidenceThreshold(0.3)
            self.face_detection.subscribe("FaceRecognition")
            self._subscribed = True
            print("subscribe face_rec")
            sleep(0.1)

    def unsubscribe(self):
        if self._subscribed:
            self.subscriber = None
            self.face_detection.unsubscribe("FaceRecognition")
            self._subscribed = False
            print("unsubscribe face_rec")
