"""
Module for manipulating the state of the screen the utility is running on.
"""
import platform

from .funky_state import FunkyState

os_type: str = platform.system()

if os_type == "Windows":
    from .windows_funkifier import WindowsFunkifier as Funkifier
elif os_type == "Darwin":
    from .mac_funkifier import MacFunkifier as Funkifier
else:
    raise NotImplementedError(f"OS {os_type} not supported.")

__all__ = ["FunkyState", "Funkifier"]
