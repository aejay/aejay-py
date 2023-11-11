"""
A module for types representing the current remote state.
"""
from enum import Enum
from typing import Type
import re
import json
from pyrsistent import PRecord, field


class ProductivityTask(Enum):
    """
    An enum representing the current task being performed.
    """

    UNKNOWN = ""
    GET_STARTED = "Get Started"
    MAKE_COFFEE = "Make Coffee"
    EXERCISE = "Exercise"
    LEARN_GERMAN = "Learn German"
    OFFICE_WORK = "Office Work"
    PROJECT_WORK = "Project Work"
    HOUSE_WORK = "House Work"
    COOK = "Cook"
    EAT_FOOD = "Eat Food"
    FREE_TIME = "Free Time"
    WIND_DOWN = "Wind Down"
    SLEEP = "Sleep"

    @classmethod
    def from_value(cls: Type["ProductivityTask"], value: str) -> "ProductivityTask":
        """
        Get the enum member with the given value, ignoring whitespace.
        """
        for member in cls:
            if member.value.replace(" ", "") == value.replace(" ", ""):
                return member
        return cls.UNKNOWN


class RemoteState(PRecord):  # pyright: ignore[reportMissingTypeArgument]
    """
    A record representing the remote state of home assistant (or, at least, the value that we care
    about for this utility).
    """

    medication_due = field(type=bool)
    german_due = field(type=bool)
    current_task = field(type=ProductivityTask)
    meeting_joined = field(type=bool)
    microphone_on = field(type=bool)
    camera_on = field(type=bool)
    presenting = field(type=bool)
    others_talking = field(type=bool)
    others_presenting = field(type=bool)

    @classmethod
    def from_json(cls: Type["RemoteState"], json_str: str) -> "RemoteState":
        """
        Deserialize the given JSON string into a RemoteState.
        """

        def to_snake_case(name: str):
            s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
            return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

        data = json.loads(json_str)
        data["CurrentTask"] = ProductivityTask.from_value(data["CurrentTask"])
        data = {to_snake_case(k): v for k, v in data.items()}
        return RemoteState(**data)
