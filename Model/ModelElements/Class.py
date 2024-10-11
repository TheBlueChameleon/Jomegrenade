from collections import OrderedDict
from dataclasses import field

from Model.Base import *
from Model.ModelNode import ModelNode
from .Config import Config
from .Enum import Enum
from .Record import Record
from .RecordSet import RecordSet


# ==================================================================================================================== #

@dataclass
class Class(ModelNode):
    name: str
    baseclass: str = None
    docString: str = None
    enums: list[Enum] = field(default_factory=lambda: [])
    classes: list['Class'] = field(default_factory=lambda: [])
    records: list[Record] = field(default_factory=lambda: [])
    config: Config = field(default_factory=lambda: Config(DEFAULT_CONFIG_NAME))

    KNOWN_KEYS = {
        KEY_IMPLICIT: FIELD_NAME,
        KEY_NAME: FIELD_NAME,
        KEY_BASECLASS : FIELD_BASECLASS,
        KEY_DOCSTRING : FIELD_DOCSTRING,
        KEY_TYPE : None
    }

    def add(self, item: ModelNode):
        if isinstance(item, Enum):
            super().add_with_duplicate_check(item, self.enums)
        elif isinstance(item, type(self)):
            super().add_with_duplicate_check(item, self.classes)
        elif isinstance(item, Record):
            super().add_with_duplicate_check(item, self.records)
        elif isinstance(item, RecordSet):
            for record in item.records:
                self.add(record)

    def get_children(self) -> list[ModelNode]:
        return self.enums + self.classes + self.records

    @classmethod
    def get_ctor_args(cls, descriptor: OrderedDict):
        result = super().get_ctor_args(descriptor)
        result[FIELD_RECORDS] = cls.get_delegate_nodes(Record, descriptor)
        return result