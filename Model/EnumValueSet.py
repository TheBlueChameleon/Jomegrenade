from collections import OrderedDict
from dataclasses import dataclass, field

from .Base import DEFAULT_CONFIG_NAME, FIELD_VALUES, PrimitiveHandlingPolicy
from .Enum import EnumValue
from .ModelNode import ModelNode
from .Config import Config

# ==================================================================================================================== #

@dataclass
class EnumValueSet(ModelNode):
    values: list[EnumValue] = field(default_factory=lambda: [])
    config: Config = field(default_factory=lambda: Config(DEFAULT_CONFIG_NAME))

    def add_enum_value(self, value: EnumValue):
        super().add_with_duplicate_check(value, self.values)

    @classmethod
    def get_ctor_args_from(
            cls,
            descriptor: OrderedDict,
            primitive_handling_policy: PrimitiveHandlingPolicy = PrimitiveHandlingPolicy.default
    ):
        result = super().get_ctor_args_from(descriptor, primitive_handling_policy)
        result[FIELD_VALUES] = cls.get_delegate_nodes(EnumValue, descriptor)
        return result
