from collections import OrderedDict
from dataclasses import dataclass, field

from sympy.codegen.cnodes import static

from Model.Base import DEFAULT_CONFIG_NAME, KEY_IMPLICIT, FIELD_NAME
from Model.ModelNode import ModelNode
from .Class import Class
from .Config import Config
from .Enum import Enum

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
    }

    def add_namespace(self, namespace: 'Namespace'):
        super().add_with_duplicate_check(namespace, self.namespaces)

    def add_enum(self, enum: Enum):
        super().add_with_duplicate_check(enum, self.enums)

    def add_class(self, cls: 'Class'):
        super().add_with_duplicate_check(cls, self.classes)

    def get_children(self) -> list[ModelNode]:
        return self.namespaces + self.enums + self.classes
