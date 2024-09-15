from collections import OrderedDict
from dataclasses import dataclass, field

from .Base import DEFAULT_CONFIG_NAME, FIELD_RECORDS
from .Record import Record
from .ModelNode import ModelNode
from .Config import Config

# ==================================================================================================================== #

@dataclass
class RecordSet(ModelNode):
    records: list[Record] = field(default_factory=lambda: [])
    config: Config = field(default_factory=lambda: Config(DEFAULT_CONFIG_NAME))

    def add_record(self, record: Record):
        super().add_with_duplicate_check(record, self.records)

    def from_ordered_dict(cls, descriptor: OrderedDict):
        return super().from_ordered_dict(descriptor)

    @classmethod
    def get_ctor_args_from(cls, descriptor: OrderedDict):
        result = super().get_ctor_args_from(descriptor)
        records = []
        for key, value in descriptor.items():
            records.append(Record.from_name_and_string(key, value))
        result[FIELD_RECORDS] = records
        return result