import requests
import matplotlib.pyplot as plt
from io import BytesIO

subscription_key = '969921d7f8b74d938eedfd1c50887522'
assert subscription_key

vision_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v2.0/"
vision_analyze_url = vision_base_url + "analyze"

image_path = "./pictures/Unbenannt3.PNG"

for i in range(3):
    image_data = open(image_path, "rb").read()

    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                  'Content-Type': 'application/octet-stream'}
    params     = {'visualFeatures': 'Categories, tags'}



    response = requests.post(
        vision_analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    analysis = response.json()
    print(analysis)
    analysisTags = analysis["tags"]
    for entry in analysisTags:
        if entry["name"] == "person":
            image_caption = "Person detected with " + repr(entry["confidence"]) + " Confidence"


    print image_caption


#image = Image.open(BytesIO(image_data))
#plt.imshow(image)
#plt.axis("off")
#_ = plt.title(image_caption, size="x-large", y=-0.1)