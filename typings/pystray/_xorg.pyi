"""
This type stub file was generated by pyright.
"""

import contextlib
from . import _base

display = ...

class XError(Exception):
    """An error that is thrown at the end of a code block managed by a
    :func:`display_manager` if an *X* error occurred.
    """

    ...

@contextlib.contextmanager
def display_manager(display):  # -> Generator[None, Any, None]:
    """Traps *X* errors and raises an :class:`XError` at the end if any
    error occurred.

    This handler also ensures that the :class:`Xlib.display.Display` being
    managed is sync'd.

    :param Xlib.display.Display display: The *X* display.
    """
    ...

class Icon(_base.Icon):
    _XEMBED_VERSION = ...
    _XEMBED_MAPPED = ...
    _SYSTEM_TRAY_REQUEST_DOCK = ...
    HAS_MENU = ...
    HAS_MENU_RADIO = ...
    HAS_NOTIFICATION = ...
    def __init__(self, *args, **kwargs) -> None: ...
    def __del__(self):  # -> None:
        ...
