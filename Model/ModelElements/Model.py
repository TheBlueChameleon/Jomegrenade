from collections import OrderedDict
from dataclasses import field

from Model.Base import *
from Model.ModelNode import ModelNode
from .Class import Class
from .Config import Config
from .Enum import Enum
from .Namespace import Namespace
from ..DescriptorHandler import split_descriptor, get_explicit_node_type_or


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
            getByReference = ByReferenceTreatment.auto,
            setByReference = ByReferenceTreatment.auto,
            visibilityRecord = VisibilityTypes.private,
            visibilityGetter = VisibilityTypes.public,
            visibilitySetter = VisibilityTypes.public,
            visibilityResetter = VisibilityTypes.public,
            visibilityInnerTypes = VisibilityTypes.public,
            isMonadic = True,
            strictEnums = True
    ))

    def add_namespace(self, namespace: 'Namespace'):
        super().add_with_duplicate_check(namespace, self.namespaces)

    def add_enum(self, enum: Enum):
        super().add_with_duplicate_check(enum, self.enums)

    def add_class(self, cls: 'Class'):
        super().add_with_duplicate_check(cls, self.classes)

    def get_children(self) -> list[ModelNode]:
        return self.namespaces + self.enums + self.classes

    @classmethod
    def get_ctor_args(cls, descriptor: OrderedDict):
        result = super().get_ctor_args(descriptor)
        for key, value in descriptor.items():
            vd = split_descriptor(value)
            print(key, vd, get_explicit_node_type_or(vd, Namespace).__name__)
        result[FIELD_CLASSES] = cls.get_delegate_nodes(Class, descriptor)
        return result