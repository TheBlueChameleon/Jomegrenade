from dataclasses import dataclass, field

from .Base import VisibilityTypes, SpecialTreatment, DEFAULT_CONFIG_NAME
from .ModelNode import ModelNode
from .Class import Class
from .Config import Config
from .Enum import Enum
from .Namespace import Namespace

# ==================================================================================================================== #

@dataclass
class Model(ModelNode):
    namespaces: list[Namespace] = field(default_factory=lambda: [])
    enums: list[Enum] = field(default_factory=lambda: [])
    classes: list[Class] = field(default_factory=lambda: [])
    config: None = field(default_factory=lambda: Config(
            name=DEFAULT_CONFIG_NAME,
            hasGetter = True,
            hasSetter = True,
            hasResetter = False,
            getByReference = True,
            setByReference = True,
            visibilityRecord = VisibilityTypes.private,
            visibilityGetter = VisibilityTypes.public,
            visibilitySetter = VisibilityTypes.public,
            visibilityResetter = VisibilityTypes.public,
            visibilityInnerTypes = VisibilityTypes.public,
            specialTreatment= SpecialTreatment.none,
            isMonadic = True
    ))

    def add_namespace(self, namespace: 'Namespace'):
        super().add_with_duplicate_check(namespace, self.namespaces)

    def add_enum(self, enum: Enum):
        super().add_with_duplicate_check(enum, self.enums)

    def add_class(self, cls: 'Class'):
        super().add_with_duplicate_check(cls, self.classes)

    def get_children(self) -> list[ModelNode]:
        return self.namespaces + self.enums + self.classes