import time

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill


class Mark1DemoSkill(MycroftSkill):
    def __init__(self):
        super(Mark1DemoSkill, self).__init__("Mark1DemoSkill")
        self.stop = False

    def initialize(self):
        self.emitter.on("mycroft.mark1.demo", self.demo)

    def demo(self, message):
        self.enclosure.mouth_text("Hello, My name is Mark One")
        self.emitter.emit(Message("mycroft.sing"))
        for i in range(0, 10):
            if self.stop:
                break
            self.enclosure.eyes_look("l")
            time.sleep(1)
            self.enclosure.eyes_look("u")
            time.sleep(1)
            self.enclosure.eyes_look("d")
            time.sleep(1)
            self.enclosure.eyes_look("r")
            time.sleep(1)
        self.enclosure.eyes_reset()
        time.sleep(1)
        self.speak("It is my first time in the world")
        time.sleep(3)
        self.enclosure.eyes_narrow()
        self.enclosure.mouth_text("Talk with me")
        for i in range(1, 50):
            self.enclosure.eyes_brightness(i)
            time.sleep(0.1)

    def stop(self):
        self.enclosure.eyes_reset()
        self.stop = True


def create_skill():
    return Mark1DemoSkill()
