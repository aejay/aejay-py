from enum import Enum
from typing import Type

class FunkyState(Enum):
    NORMAL = "Normal"
    STEP_AWAY = "Step Away"
    MEDICATION_DUE = "Medication Due"
    GERMAN_DUE = "German Due"

    @classmethod
    def from_value(cls: Type["FunkyState"], value: str):
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"No enum member with value '{value}' found")
