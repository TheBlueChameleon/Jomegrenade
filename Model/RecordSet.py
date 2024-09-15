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

    @classmethod
    def get_ctor_args_from(cls, descriptor: OrderedDict):
        result = super().get_ctor_args_from(descriptor)
        result[FIELD_RECORDS] = result[FIELD_RECORDS] = cls.get_delegate_nodes(Record, descriptor)
        return result