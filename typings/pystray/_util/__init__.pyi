"""
This type stub file was generated by pyright.
"""

import contextlib
import os
import tempfile

@contextlib.contextmanager
def serialized_image(image, format, extension=...):  # -> Generator[Unknown, Any, None]:
    """Creates an image file from a :class:`PIL.Image.Image`.

    This function is a context manager that yields a temporary file name. The
    file is removed when the block is exited.

    :param PIL.Image.Image image: The in-memory image.

    :param str format: The format of the image. This format must be handled by
        *Pillow*.

    :param extension: The file extension. This defaults to ``format``
        lowercased.
    :type extensions: str or None
    """
    ...