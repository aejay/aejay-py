import subprocess
import shutil
from .Funkifier import Funkifier
from .FunkyState import FunkyState

class MacFunkifier(Funkifier):
    def __init__(self):
        self._has_brightness = not shutil.which('brightness') is None

    def start(self):
       pass

    def stop(self):
       pass

    def funkify_screen(self, state: FunkyState):
        if state == FunkyState.NORMAL:
          applescript = """
          tell application "System Events"
              tell appearance preferences
                  set dark mode to true
              end tell
          end tell
          """

          subprocess.run(['osascript', '-e', applescript])
          if self._has_brightness:
            subprocess.run(['brightness', '-m', '0.8'])
        else:
          applescript = """
          tell application "System Events"
              tell appearance preferences
                  set dark mode to false
              end tell
          end tell
          """

          subprocess.run(['osascript', '-e', applescript])
          if self._has_brightness:
            subprocess.run(['brightness', '-m', '0.05'])
