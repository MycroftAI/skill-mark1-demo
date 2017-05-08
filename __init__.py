from threading import Timer

import time
from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill


class Mark1DemoSkill(MycroftSkill):
    def __init__(self):
        super(Mark1DemoSkill, self).__init__("Mark1DemoSkill")
        self.thread = None
        self.kill = False

    def initialize(self):
        self.emitter.on("mycroft.mark1.demo", self.demo)

    def sleep(self, t):
        if self.kill:
            raise Exception
        time.sleep(t)

    def mark1(self):
        self.enclosure.mouth_text("Hello, My name is Mark One")
        self.emitter.emit(Message("mycroft.sing"))
        for i in range(0, 10):
            self.enclosure.eyes_look("l")
            self.sleep(1)
            self.enclosure.eyes_look("u")
            self.sleep(1)
            self.enclosure.eyes_look("d")
            self.sleep(1)
            self.enclosure.eyes_look("r")
            self.sleep(1)
        self.enclosure.eyes_reset()
        self.sleep(1)
        self.speak("It is my first time in the world")
        self.sleep(3)
        self.enclosure.eyes_narrow()
        self.enclosure.mouth_text("Talk with me")
        for i in range(1, 50):
            self.enclosure.eyes_brightness(i)
            self.sleep(0.1)
        self.enclosure.eyes_reset()

    def demo(self, message):
        try:
            self.kill = False
            self.mark1()
        except:
            self.enclosure.eyes_reset()

    def stop(self):
        self.kill = True
        self.enclosure.eyes_reset()


def create_skill():
    return Mark1DemoSkill()
