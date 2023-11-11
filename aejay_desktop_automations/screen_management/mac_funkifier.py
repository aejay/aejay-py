"""
Module for funkifying the screen on mac machines.
"""
import subprocess
import shutil
from .funkifier import Funkifier
from .funky_state import FunkyState


class MacFunkifier(Funkifier):
    """
    A type that can funkify the screen on mac machines.
    """

    def __init__(self):
        self._brightness_path = shutil.which("brightness") or shutil.which(
            "/usr/local/bin/brightness"
        )

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

            subprocess.run(
                ["osascript", "-e", applescript], stdout=subprocess.DEVNULL, check=False
            )
            if self._brightness_path is not None:
                # This thing is pretty chatty about not being able to update the non-internal display
                subprocess.run(
                    [self._brightness_path, "-v", "0.05"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
        else:
            applescript = """
          tell application "System Events"
              tell appearance preferences
                  set dark mode to true
              end tell
          end tell
          """

            subprocess.run(
                ["osascript", "-e", applescript], stdout=subprocess.DEVNULL, check=False
            )
            if self._brightness_path is not None:
                # This thing is pretty chatty about not being able to update the non-internal display
                subprocess.run(
                    [self._brightness_path, "-v", "0.8"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
