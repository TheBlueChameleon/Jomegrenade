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
        KEY_PRIMITIVE: FIELD_NAME,
        KEY_NAME: FIELD_NAME,
        KEY_BASECLASS : FIELD_BASECLASS,
        KEY_DOCSTRING : FIELD_DOCSTRING,
        KEY_TYPE : None
    }

    def add_enum(self, enum: Enum):
        super().add_with_duplicate_check(enum, self.enums)

    def add_class(self, cls: 'Class'):
        super().add_with_duplicate_check(cls, self.classes)

    def add_record(self, record: Record):
        super().add_with_duplicate_check(record, self.records)

    def add_record_set(self, arg: RecordSet):
        for record in arg.records:
            self.add_record(record)

    def get_children(self) -> list[ModelNode]:
        return self.enums + self.classes + self.records

    @classmethod
    def get_ctor_args(cls, descriptor: OrderedDict):
        result = super().get_ctor_args(descriptor)
        result[FIELD_RECORDS] = cls.get_delegate_nodes(Record, descriptor)
        return result