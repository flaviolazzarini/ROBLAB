from io import BytesIO

import cv2
import urllib
from urllib2 import urlopen

from PIL import Image

for _ in range(10):
    stream = urlopen('http://192.168.1.110:8080/video/mjpeg')
    byt = bytes()
    exit = False
    while not exit:
        byt += stream.read(1024)
        a = byt.find(b'\xff\xd8')
        b = byt.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = byt[a:b+2]
            byt = byt[b+2:]
            exit = True

    image = Image.open(BytesIO(jpg))
    image.save("/home/nao/hs18_hideandseek/test.jpg")

    print "Test"

class azureImageWraper():
    def __main__(self, image_data):
        self.image_data = image_data

    def read(self):
        return self.image_data
