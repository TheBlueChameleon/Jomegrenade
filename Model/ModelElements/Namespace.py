from collections import OrderedDict
from dataclasses import dataclass, field

from Model.Base import DEFAULT_CONFIG_NAME, KEY_IMPLICIT, FIELD_NAME, KEY_TYPE, TYPENAME_NAMESPACE, TYPENAME_CLASS, \
    TYPENAME_ENUM, FIELD_CLASSES, FIELD_ENUMS, FIELD_NAMESPACES
from Model.ModelNode import ModelNode
from .Class import Class
from .Config import Config
from .Enum import Enum
from .. import KEY_NAME, NamedElement
from ..DescriptorHandler import split_descriptor, get_explicit_node_type_or


# ==================================================================================================================== #

@dataclass
class Namespace(ModelNode):
    name: str
    namespaces: list['Namespace'] = field(default_factory=lambda: [])
    enums: list[Enum] = field(default_factory=lambda: [])
    classes: list[Class] = field(default_factory=lambda: [])
    config: Config = field(default_factory=lambda: Config(DEFAULT_CONFIG_NAME))

    KNOWN_KEYS = {
        KEY_TYPE: None,
        KEY_IMPLICIT: FIELD_NAME,
        KEY_NAME: FIELD_NAME
    }

    DELEGATE_RESULT_RECEIVERS = {
        TYPENAME_CLASS: FIELD_CLASSES,
        TYPENAME_ENUM: FIELD_ENUMS,
        TYPENAME_NAMESPACE: FIELD_NAMESPACES
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

    @classmethod
    def get_ctor_args(cls, descriptor: OrderedDict):
        # todo: de-duplicate (direct copy from Model; consider deviation in Class, Enum)
        result = super().get_ctor_args(descriptor)
        unused = cls.get_unknown_args(descriptor)
        for name, element_descriptor in unused.items():
            delegate_descriptor = split_descriptor(element_descriptor)
            delegate_class: ModelNode = get_explicit_node_type_or(delegate_descriptor, Namespace)
            
            target_name = delegate_descriptor.get(KEY_TYPE, TYPENAME_NAMESPACE)
            target = cls.DELEGATE_RESULT_RECEIVERS.get(target_name, None)
            if target is not None:
                instance = delegate_class.from_name_and_string(name, element_descriptor)
                if target not in result.keys():
                    result[target] = []
                result[target].append(instance)

        return result
