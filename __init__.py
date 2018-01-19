# Copyright 2017, Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
from threading import Thread

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill


#######################################################################
# Helpers for building the animation frames

def animation(t, often, func, *args):
    '''
    Args:
        t (int) : seconds from now to begin the frame (secs)
        often (int/string): (int) how often to repeat the frame (secs)
                            (str) when to trigger, relative to the clock,
                                  for synchronized repetitions
        func: the function to invoke
        *args: arguments to pass to func
    '''
    return {
        "time": time.time() + t,
        "often": often,
        "func": func,
        "args": args
    }


def __get_time(often, t):
    return often - t % often

#######################################################################


class Mark1DemoSkill(MycroftSkill):
    def __init__(self):
        super(Mark1DemoSkill, self).__init__("Mark1DemoSkill")
        self.animations = []
        self.playing = False
        self.thread = None

    def initialize(self):
        # Listen for the message send by the DEMO menu item on a Mark 1
        self.add_event("mycroft.mark1.demo", self.demo, False)

    def run(self):
        while self.playing:
            for animation in self.animations:
                if animation["time"] <= time.time():
                    # Execute animation action
                    animation["func"](*animation["args"])

                    # Adjust time for next loop
                    if type(animation["often"]) is int:
                        animation["time"] = time.time() + animation["often"]
                    else:
                        often = int(animation["often"])
                        t = animation["time"]
                        animation["time"] = time.time() + __get_time(
                            often, t)
            time.sleep(0.1)

        self.thread = None

    def demo(self, message):
        if not self.thread:
            self.playing = True

            # Build the list of animation actions to run
            self.animations = [
                # Change the eyes every 2 seconds, looping at 8 seconds
                animate(0, 8, self.enclosure.eyes_look, "r"),
                animate(2, 8, self.enclosure.eyes_look, "l"),
                animate(4, 8, self.enclosure.eyes_look, "d"),
                animate(6, 8, self.enclosure.eyes_look, "u"),

                # Every 120 seconds, sing a song.  This is synchronized
                # based on the clock, so multiple units can sing in abs
                # chorus.
                #
                # skill-singing handles the mycroft.sing message
                animate(__get_time(120, time.time()), "120",
                        self.emitter.emit, Message("mycroft.sing"))
            ]

            self.thread = Thread(None, self.run)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        if self.playing:
            self.playing = False  # the thread will kill itself
            self.enclosure.eyes_reset()
            return True
        else:
            return False


def create_skill():
    return Mark1DemoSkill()
