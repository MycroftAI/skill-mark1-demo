from mycroft.skills.core import MycroftSkill


class Mark1DemoSkill(MycroftSkill):
    def __init__(self):
        super(Mark1DemoSkill, self).__init__("Mark1DemoSkill")

    def initialize(self):
        pass

    def stop(self):
        pass


def create_skill():
    return Mark1DemoSkill()
