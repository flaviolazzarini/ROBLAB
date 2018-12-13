from urllib2 import urlopen

import requests
import logging

class azureImageWraper():
    def __init__(self, image_data):
        self.image_data = image_data

    def read(self):
        return self.image_data

class AzureHumanDetector():
    def __init__(self, robot):
        self.session = robot.session

        self.subscription_key = '969921d7f8b74d938eedfd1c50887522'
        assert self.subscription_key

        self.vision_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v2.0/"
        self.vision_analyze_url = self.vision_base_url + "analyze"

        self.image_path = "./pictures/Unbenannt3.PNG"

        self._serviceID = "AzureService"
        self.camera = robot.ALPhotoCapture
        self.camera.setResolution(3)
        self.camera.setColorSpace(9)
        self.path = "/home/nao/hs18_hideandseek/"
        self.fileName = "temp2.jpg"

        logging.getLogger().setLevel(logging.WARNING)
        logging.info('AzureHumanDetector initialized')

    def detect_if_people_are_in_sight(self):
        wrapper = self.getPictureFromCamera2()
        image_data = wrapper.read()

        headers    = {'Ocp-Apim-Subscription-Key': self.subscription_key,
                      'Content-Type': 'application/octet-stream'}
        params     = {'visualFeatures': 'Categories, tags'}

        response = requests.post(
            self.vision_analyze_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()

        analysis = response.json()
        print(analysis)
        analysisTags = analysis["tags"]
        for entry in analysisTags:
            if entry["name"] == "person":
                logging.info("Person detected with " + repr(entry["confidence"]) + " Confidence")
                return True
        return False

    def getPictureFromCamera(self):
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
        self.camera.takePicture(self.path, self.fileName)
        return open(self.path + self.fileName, 'rd')


