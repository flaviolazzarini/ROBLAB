import concurrent
from time import sleep


class FaceLearning(object):
    def __init__(self, robot):
        """
        Initialisation of qi framework and event detection.
        """
        # Get the service ALMemory.
        self.session = robot.session
        self._app = robot.app
        self.memory = self.session.service("ALMemory")
        self.subscriber = None
        self._success = None
        self.face_detection = None
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._name = None
        self._face_learned = False

    def learn_face_blocking(self, name, timeout=None):
        future = self.learn_face_concurrently(name)
        return future.result(timeout)

    def learn_face_concurrently(self, name):
        future = self._executor.submit(self.__learn_face_logic, name)
        return future

    def __learn_face_logic(self, name):
        try:
            self._name = name
            self.subscribe()
            self.face_detection.forgetPerson(self._name)
            #self._app.run()
            while not self._face_learned:
                sleep(0)
        except Exception, e:
            print "Error: ", e

        return self.__get_result_and_reset()

    def __get_result_and_reset(self):
        return self._success

    def on_human_tracked(self, value):
        """
        Callback for event FaceDetected.
        """
        print "Callback"
        # Unsubscribe from to prevent multiple triggers
        self.unsubscribe()

        if value != []:  # empty value when the face disappears
            self._success = self.face_detection.learnFace(self._name)
            print("learning face")

        else:
            self.subscribe()
        self._face_learned = True
        #self._app.stop()

    def subscribe(self):
        print("Subscribed")
        self.subscriber = self.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.on_human_tracked)
        self.face_detection = self.session.service("ALFaceDetection")
        self.face_detection.setRecognitionConfidenceThreshold(0.3)
        self.face_detection.subscribe("FaceRecognition")

    def unsubscribe(self):
        self.subscriber = None
        self.face_detection.unsubscribe("FaceRecognition")