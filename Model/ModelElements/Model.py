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

    DELEGATE_RESULT_RECEIVERS = {
        TYPENAME_CLASS: FIELD_CLASSES,
        TYPENAME_ENUM: FIELD_ENUMS,
        TYPENAME_NAMESPACE: FIELD_NAMESPACES
    }

    def add(self, item: NamedElement):
        if isinstance(item, type(self)):
            super().add_with_duplicate_check(item, self.namespaces)
        if isinstance(item, Enum):
            super().add_with_duplicate_check(item, self.enums)
        if isinstance(item, Class):
            super().add_with_duplicate_check(item, self.classes)
        if isinstance(item, Namespace):
            super().add_with_duplicate_check(item, self.namespaces)

    def get_children(self) -> list[ModelNode]:
        return self.namespaces + self.enums + self.classes

    @classmethod
    def get_ctor_args(cls, descriptor: OrderedDict):
        result = super().get_ctor_args(descriptor)
        unused = cls.get_unknown_args(descriptor)
        for name, element_descriptor in unused.items():
            delegate_descriptor = split_descriptor(element_descriptor)
            delegate_class = get_explicit_node_type_or(delegate_descriptor, Namespace)

            delegate_descriptor[KEY_NAME] = name
            if KEY_TYPE in delegate_descriptor.keys():
                target_name = delegate_descriptor.pop(KEY_TYPE)
            else:
                target_name = TYPENAME_NAMESPACE

            target = cls.DELEGATE_RESULT_RECEIVERS.get(target_name, None)
            if target is not None:
                instance = delegate_class.from_ordered_dict(delegate_descriptor)
                if target not in result.keys():
                    result[target] = []
                result[target].append(instance)

        return result