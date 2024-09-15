from collections import OrderedDict
from dataclasses import dataclass, field

from .Base import DEFAULT_CONFIG_NAME, FIELD_VALUES
from .Enum import EnumValue
from .ModelNode import ModelNode
from .Config import Config

# ==================================================================================================================== #

@dataclass
class EnumValueSet(ModelNode):
    values: list[EnumValue] = field(default_factory=lambda: [])
    config: Config = field(default_factory=lambda: Config(DEFAULT_CONFIG_NAME))

    @classmethod
    def get_ctor_args_from(cls, descriptor: OrderedDict):
        result = super().get_ctor_args_from(descriptor)
        values = []
        for key, value in descriptor.items():
            values.append(EnumValue.from_name_and_string(key, value))
        result[FIELD_VALUES] = values
        return result
