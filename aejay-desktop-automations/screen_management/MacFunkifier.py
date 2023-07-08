import subprocess
import shutil
from .Funkifier import Funkifier
from .FunkyState import FunkyState

class MacFunkifier(Funkifier):
    def __init__(self):
        self._has_brightness = not shutil.which('brightness') is None

    def funkify_screen(self, state: FunkyState):
        if state == FunkyState.NORMAL:
          applescript = """
          tell application "System Events"
              tell appearance preferences
                  set high contrast to false
                  set dark mode to true
              end tell
          end tell
          """

          subprocess.run(['osascript', '-e', applescript])
          if self._has_brightness:
            subprocess.run(['brightness', '1.0', applescript])
        else:
          applescript = """
          tell application "System Events"
              tell appearance preferences
                  set dark mode to false
                  set high contrast to true
              end tell
          end tell
          """

          subprocess.run(['osascript', '-e', applescript])
          if self._has_brightness:
            subprocess.run(['brightness', '0.2', applescript])
