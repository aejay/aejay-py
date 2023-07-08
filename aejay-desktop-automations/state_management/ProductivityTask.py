from enum import Enum
from typing import Type

class ProductivityTask(Enum):
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
        for member in cls:
            if member.value.replace(" ", "") == value.replace(" ", ""):
                return member
        return cls.UNKNOWN
