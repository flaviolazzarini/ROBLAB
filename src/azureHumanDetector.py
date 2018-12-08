import requests
from PIL import Image
from naoqi import ALModule
import logging

class AzureHumanDetector(ALModule):
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
        self.fileName = "temp.jpg"

        logging.getLogger().setLevel(logging.WARNING)
        logging.info('AzureHumanDetector initialized')

    def detect_if_people_are_in_sight(self):
        # images = self.getPictureFromCamera()
        # images[0].save("./pictures/_temp.png", "PNG")


        image_data = open("./pictures/_temp.png", "rb").read()

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
        self.camera.takePicture(self.path, self.fileName)
        return str(self.path + self.fileName)
