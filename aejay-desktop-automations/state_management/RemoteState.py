from typing import Type
from pyrsistent import PRecord, field
import re
import json
from .ProductivityTask import ProductivityTask

class RemoteState(PRecord):
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
        def to_snake_case(name):
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        
        data = json.loads(json_str)
        data['CurrentTask'] = ProductivityTask.from_value(data['CurrentTask'])
        data = {to_snake_case(k): v for k, v in data.items()}
        return RemoteState(**data)