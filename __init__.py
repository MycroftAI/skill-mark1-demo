from mycroft.skills.core import MycroftSkill


class Mark1DemoSkill(MycroftSkill):
    def __init__(self):
        super(Mark1DemoSkill, self).__init__("Mark1DemoSkill")

    def initialize(self):
        self.emitter.on("mycroft.mark1.demo", self.demo)

    def demo(self, message):
        self.name()
        self.change_eyes()

    def change_eyes(self):
        self.enclosure.eyes_narrow()

    def name(self):
        self.enclosure.mouth_text("Hello, My name is Mark One")

    def stop(self):
        pass


def create_skill():
    return Mark1DemoSkill()
