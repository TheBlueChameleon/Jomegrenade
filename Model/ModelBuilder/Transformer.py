from collections import OrderedDict
from dataclasses import field
from typing import Any

from .Base import KeyMappingSet, REGISTERED_KEY_MAPPING_SETS

from Model import *
from Model.ModelNode import ModelNode
from Model.CtorDictHandler import CtorDictHandler


# ==================================================================================================================== #

def from_name_and_ordered_dict(cls: type[CtorDictHandler, NamedElement, Any], name:str, descriptor: OrderedDict):
    return cls(name, **cls.get_ctor_args(descriptor))

# ==================================================================================================================== #

@dataclass
class Transformer:
    name: str
    nodeType: type[ModelNode]
    node: ModelNode = None
    children: list['Transformer'] = field(default_factory=lambda: [])
    params: OrderedDict = field(default_factory=lambda: OrderedDict())

    def evaluate(self) -> ModelNode:
        self.node = from_name_and_ordered_dict(self.nodeType, self.name, self.params)
        for child in self.children:
            self.add(child.evaluate())
        return self.node

    def add_child_transformer(self, transformer: 'Transformer'):
        self.children.append(transformer)

    def add_params(self, key: str, value: OrderedDict | str):
        self.params[key] = value

    def add(self, arg: NamedElement):
        if isinstance(arg, Class):
            self.node.add_class(arg)
        elif isinstance(arg, Enum):
            self.node.add_enum(arg)
        elif isinstance(arg, EnumValue):
            self.node.add_enum_value(arg)
        elif isinstance(arg, EnumValueSet):
            self.node.add_enum_value_set(arg)
        elif isinstance(arg, Namespace):
            self.node.add_namespace(arg)
        elif isinstance(arg, Record):
            self.node.add_record(arg)
        elif isinstance(arg, RecordSet):
            self.node.add_record_set(arg)

    def get_key_mapping_set(self) -> KeyMappingSet:
        return REGISTERED_KEY_MAPPING_SETS[self.nodeType]

    def get_node_type_name(self) -> str:
        return self.nodeType.__name__
