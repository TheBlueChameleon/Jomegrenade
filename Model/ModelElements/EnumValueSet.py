from collections import OrderedDict
from dataclasses import dataclass, field

from Model.Base import DEFAULT_CONFIG_NAME, FIELD_VALUES, NamedElement
from .Enum import EnumValue
from Model.ModelNode import ModelNode
from .Config import Config

# ==================================================================================================================== #

@dataclass
class EnumValueSet(ModelNode):
    values: list[EnumValue] = field(default_factory=lambda: [])
    config: Config = field(default_factory=lambda: Config(DEFAULT_CONFIG_NAME))

    def add(self, item: NamedElement):
        if isinstance(item, EnumValue):
            super().add_with_duplicate_check(item, self.values)

    @classmethod
    def get_ctor_args(cls, descriptor: OrderedDict):
        result = super().get_ctor_args(descriptor)
        result[FIELD_VALUES] = cls.get_delegate_nodes(EnumValue, descriptor)
        return result
