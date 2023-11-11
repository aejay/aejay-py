"""
Module for configuring the application for distribution.
"""
from setuptools import setup

APP = ["main.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": True,
    "plist": {
        "CFBundleName": "Aejay Automations",
        "CFBundleDisplayName": "Aejay Automations",
        "CFBundleGetInfoString": "Aejay Automations",
        "CFBundleIdentifier": "com.aejay.automations",
        "LSUIElement": True,
    },
    "packages": ["keyring"],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
