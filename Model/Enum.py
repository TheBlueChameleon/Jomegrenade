from dataclasses import field

from .Base import *
from .ModelNode import ModelNode, NamedElement
from .Config import Config
from .EnumValue import EnumValue
from .EnumValueSet import EnumValueSet

# ==================================================================================================================== #

@dataclass
class Enum(ModelNode):
    name: str
    baseclass: str = None
    docString: str = None
    values: list[EnumValue] = field(default_factory=lambda: [])
    config: Config = field(default_factory=lambda: Config(DEFAULT_CONFIG_NAME))

    KNOWN_KEYS = {
        KEY_PRIMITIVE: FIELD_NAME,
        KEY_NAME: FIELD_NAME,
        KEY_BASECLASS : FIELD_BASECLASS,
        KEY_TYPE: None
    }

    def add_enum_value(self, value: EnumValue):
        super().add_with_duplicate_check(value, self.values)

    def add_enum_value_set(self, arg: EnumValueSet):
        for value in arg.values:
            self.add_enum_value(value)

    def get_children(self) -> list[EnumValue]:
        return self.values

    @classmethod
    def get_ctor_args(cls, descriptor: OrderedDict):
        result = super().get_ctor_args(descriptor)
        result[FIELD_VALUES] = cls.get_delegate_nodes(EnumValue, descriptor)
        return result