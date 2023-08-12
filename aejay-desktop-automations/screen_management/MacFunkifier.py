import subprocess
import shutil
from .Funkifier import Funkifier
from .FunkyState import FunkyState

class MacFunkifier(Funkifier):
    def __init__(self):
        self._brightness_path = shutil.which('brightness') or shutil.which('/usr/local/bin/brightness')

    def start(self):
       pass

    def stop(self):
       pass

    def funkify_screen(self, state: FunkyState):
        if state == FunkyState.STEP_AWAY:
          applescript = """
          tell application "System Events"
              tell appearance preferences
                  set dark mode to false
              end tell
          end tell
          """

          subprocess.run(['osascript', '-e', applescript], stdout=subprocess.DEVNULL)
          if self._brightness_path is not None:
            # This thing is pretty chatty about not being able to update the non-internal display
            subprocess.run([self._brightness_path, '-v', '0.05'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
          applescript = """
          tell application "System Events"
              tell appearance preferences
                  set dark mode to true
              end tell
          end tell
          """

          subprocess.run(['osascript', '-e', applescript], stdout=subprocess.DEVNULL)
          if self._brightness_path is not None:
            # This thing is pretty chatty about not being able to update the non-internal display
            subprocess.run([self._brightness_path, '-v', '0.8'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
