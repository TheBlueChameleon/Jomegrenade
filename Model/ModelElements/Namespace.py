from dataclasses import dataclass, field

from Model.Base import DEFAULT_CONFIG_NAME, KEY_IMPLICIT, FIELD_NAME
from Model.ModelNode import ModelNode
from .Class import Class
from .Config import Config
from .Enum import Enum
from .. import KEY_NAME, NamedElement


# ==================================================================================================================== #

@dataclass
class Namespace(ModelNode):
    name: str
    namespaces: list['Namespace'] = field(default_factory=lambda: [])
    enums: list[Enum] = field(default_factory=lambda: [])
    classes: list[Class] = field(default_factory=lambda: [])
    config: Config = field(default_factory=lambda: Config(DEFAULT_CONFIG_NAME))

    KNOWN_KEYS = {
        KEY_IMPLICIT: FIELD_NAME,
        KEY_NAME: FIELD_NAME
    }

    def add(self, item: NamedElement):
        if isinstance(item, type(self)):
            super().add_with_duplicate_check(item, self.namespaces)
        elif isinstance(item, Enum):
            super().add_with_duplicate_check(item, self.enums)
        elif isinstance(item, Class):
            super().add_with_duplicate_check(item, self.classes)

    def get_children(self) -> list[ModelNode]:
        return self.namespaces + self.enums + self.classes
