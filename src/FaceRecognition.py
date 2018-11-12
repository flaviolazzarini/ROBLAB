import sys

from naoqi import ALBroker, ALModule
import time
import concurrent.futures


class FaceRecognition(object):

    def __init__(self, robot):
        """
        Initialisation of qi framework and event detection.
        """
        # Get the service ALMemory.
        self.session = robot.session
        self._app = robot.app
        self.memory = self.session.service("ALMemory")
        self.subscriber = None
        self.face_detection = None
        self._knownFace = None
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._name = None

    def deleteExtractor(self):
        self._executor = None

    def search_face_blocking(self, timeout=None):
        future = self.search_face_concurrently()
        return future.result(timeout)

    def search_face_concurrently(self):
        future = self._executor.submit(self.__search_face_logic)
        return future

    def __search_face_logic(self):
        try:
            self.subscribe()
            self._app.run()
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

        else:
            self.subscribe()

        self._app.stop()

    def subscribe(self):
        self.subscriber = self.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.on_human_tracked)
        self.face_detection = self.session.service("ALFaceDetection")
        self.face_detection.setRecognitionConfidenceThreshold(0.3)
        self.face_detection.subscribe("FaceRecognition")

    def unsubscribe(self):
        self.subscriber = None
        self.face_detection.unsubscribe("FaceRecognition")
