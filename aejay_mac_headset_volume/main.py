"""
Main module for the module that adjusts the volume of my headset.
"""
import sys


def _main():
    ...


if __name__ == "__main__":
    sys.stdout = sys.stderr = open(
        "/tmp/aejay_mac_headset_volume.log", "a", encoding="utf-8"
    )
    _main()
