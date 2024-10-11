from collections import OrderedDict
from dataclasses import field

from Model.Base import *
from Model.ModelNode import ModelNode, NamedElement
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
        KEY_IMPLICIT: FIELD_NAME,
        KEY_NAME: FIELD_NAME,
        KEY_BASECLASS : FIELD_BASECLASS,
        KEY_TYPE: None
    }

    def add(self, item: NamedElement):
        if isinstance(item, EnumValue):
            super().add_with_duplicate_check(item, self.values)
        elif isinstance(item, EnumValueSet):
            for value in item.values:
                self.add(value)

    def get_children(self) -> list[EnumValue]:
        return self.values

    @classmethod
    def get_ctor_args(cls, descriptor: OrderedDict):
        result = super().get_ctor_args(descriptor)
        result[FIELD_VALUES] = cls.get_delegate_nodes(EnumValue, descriptor)
        return result