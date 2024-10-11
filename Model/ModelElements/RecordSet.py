from collections import OrderedDict
from dataclasses import dataclass, field

from Model.Base import DEFAULT_CONFIG_NAME, FIELD_RECORDS
from .Record import Record
from Model.ModelNode import ModelNode
from .Config import Config
from .. import NamedElement


# ==================================================================================================================== #

@dataclass
class RecordSet(ModelNode):
    records: list[Record] = field(default_factory=lambda: [])
    config: Config = field(default_factory=lambda: Config(DEFAULT_CONFIG_NAME))

    def add(self, item: NamedElement):
        if isinstance(item, Record):
            super().add_with_duplicate_check(item, self.records)

    @classmethod
    def get_ctor_args(cls, descriptor: OrderedDict):
        result = super().get_ctor_args(descriptor)
        result[FIELD_RECORDS] = result[FIELD_RECORDS] = cls.get_delegate_nodes(Record, descriptor)
        return result