from dataclasses import field

from .Base import *
from .ModelNode import ModelNode
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
    def get_ctor_args_from(cls, descriptor: OrderedDict):
        result = super().get_ctor_args_from(descriptor)
        unused = cls.get_unknown_args_from(descriptor)
        records = []
        for key, value in unused.items():
            if isinstance(value, str):
                records.append(Record.from_name_and_string(key, value))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        records.append(Record.from_name_and_string(key, item))
                    else:
                        # TODO proper log and warning handling
                        print("warning message: unknown JSON element:", item)
            else:
                # TODO proper log and warning handling
                print("warning message: unknown JSON element:", value)
        result[FIELD_RECORDS] = records
        return result