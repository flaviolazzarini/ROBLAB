from pynaoqi_mate import Robot
from configuration import PepperConfiguration
from naoqi import ALModule
from time import sleep


class SoundLocalizer(ALModule):

    def __init__(self, myrobot):
        super(SoundLocalizer, self)

        session = myrobot.session
        self.memory = session.service("ALMemory")

        self.tts = session.service("ALTextToSpeech")
        self.sound_localization = session.service("ALSoundLocalization")
        self.sound_localization.setParameter("Sensitivity", 0.8)
        self.sound_localization.subscribe("SoundLocalizationModule")

        self.subscriber = self.memory.subscriber("ALSoundLocalization/SoundLocated")
        self.subscriber.signal.connect(self.on_sound_located)

    def on_sound_located(self, value):

        # Unsubscribe from to prevent multiple triggers
        self.subscriber = None

        sleep(0.1)

        if value[1][0] < -1.74 or value[1][0] > 1.74:
            self.tts.say("Hey back there")

        if value[1][0] >= -1.74 and value[1][0] < -0.26:
            self.tts.say("I guess there is someone right of me")

        if value[1][0] > 0.26 and value[1][0] <= 1.74:
            self.tts.say("I guess there is someone left of me")

        if value[1][0] >= -0.26 and value[1][0] <= 0.26:
            self.tts.say("Oohhh ")
            sleep(0.1)
            self.tts.say("Hi there")


        print"\nPosition of sound relativ to Head (Rad)"
        print(value[1][0])
        print(value[1][1])

        sleep(0.2)

        # Subscribe to enable trigger
        self.subscriber = self.memory.subscriber("ALSoundLocalization/SoundLocated")
        self.subscriber.signal.connect(self.on_sound_located)

    def run(self):
        sleep(60)



if __name__ == "__main__":

    config = PepperConfiguration("Porter")
    robot = Robot(config)

    slm = SoundLocalizer(robot)
    slm.run()
