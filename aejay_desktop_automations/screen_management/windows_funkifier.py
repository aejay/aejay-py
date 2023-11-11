"""
Module for funkifying the screen on windows machines.
"""
import ctypes
import time
import threading
from typing import Callable, Dict, cast
from .funkifier import Funkifier
from .funky_state import FunkyState

# Define a type for the MAGCOLOREFFECT structure
MagColorEffectType = ctypes.c_float * 25

# Load the Magnification.dll library
magnification = cast(ctypes.CDLL, ctypes.WinDLL("Magnification.dll"))  # type: ignore

# Get a reference to the MagSetFullscreenColorEffect function
mag_set_fullscreen_color_effect: Callable[
    [MagColorEffectType], bool
] = magnification.MagSetFullscreenColorEffect
mag_initialize = magnification.MagInitialize
mag_uninitialize = magnification.MagUninitialize

# Set up argument types and return type
mag_set_fullscreen_color_effect.argtypes = [MagColorEffectType]
mag_set_fullscreen_color_effect.restype = ctypes.c_bool
mag_initialize.restype = ctypes.c_bool
mag_uninitialize.restype = ctypes.c_bool

funky_effect_map: Dict[FunkyState, MagColorEffectType] = {
    FunkyState.NORMAL: MagColorEffectType(
        +1.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +1.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +1.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +1.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +1.0,
    ),
    FunkyState.STEP_AWAY: MagColorEffectType(
        -0.1,
        -0.1,
        -0.1,
        +0.0,
        +0.0,
        -0.1,
        -0.1,
        -0.1,
        +0.0,
        +0.0,
        -0.1,
        -0.1,
        -0.1,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +1.0,
        +0.0,
        +0.2,
        +0.2,
        +0.2,
        +0.0,
        +1.0,
    ),
    FunkyState.MEDICATION_DUE: MagColorEffectType(
        +1.0,
        +0.5,
        +0.5,
        +0.0,
        +0.0,
        +0.5,
        +0.5,
        +0.5,
        +0.0,
        +0.0,
        +0.5,
        +0.5,
        +0.5,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +1.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +1.0,
    ),
    FunkyState.GERMAN_DUE: MagColorEffectType(
        +0.5,
        +0.5,
        +0.5,
        +0.0,
        +0.0,
        +0.5,
        +1.0,
        +0.5,
        +0.0,
        +0.0,
        +0.5,
        +0.5,
        +0.5,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +1.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +0.0,
        +1.0,
    ),
}


class WindowsFunkifier(Funkifier):
    def __init__(self):
        self._ending: bool = False
        self._last_state: FunkyState = FunkyState.NORMAL
        self._desired_state: FunkyState = FunkyState.NORMAL
        self._thread = threading.Thread(target=self._init_worker)

    def funkify_screen(self, state: FunkyState):
        self._desired_state = state

    def start(self):
        if not self._thread.is_alive():
            self._thread.start()

    def stop(self):
        self._ending = True
        self._thread.join(5)
        if self._thread.is_alive():
            raise RuntimeError("Failed to end child thread!")

    def _init_worker(self):
        print("Initializing magnifier...")
        if not mag_initialize():
            raise RuntimeError("Failed to initialize Magnification API!")

        while not self._ending:
            if self._desired_state != self._last_state:
                print(f"Setting screen mode to {self._desired_state}")
                self._last_state = self._desired_state
                effect = funky_effect_map[self._desired_state]
                if not mag_set_fullscreen_color_effect(effect):
                    print(f"Failed to set color effect for {self._desired_state.name}")
            time.sleep(1)

        print("Uninitializing magnifier...")
        if not mag_uninitialize():
            print("Failed to uninitialize Magnification API!")
