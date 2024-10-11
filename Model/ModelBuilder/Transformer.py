from collections import OrderedDict
from dataclasses import field
from typing import Any

from Model import *
from Model.CtorDictHandler import CtorDictHandler
from Model.ModelNode import ModelNode
from .Base import KeyMappingSet, REGISTERED_KEY_MAPPING_SETS


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
            self.node.add(child.evaluate())
        return self.node

    def add_child_transformer(self, transformer: 'Transformer'):
        self.children.append(transformer)

    def add_params(self, key: str, value: OrderedDict | str):
        self.params[key] = value

    def get_key_mapping_set(self) -> KeyMappingSet:
        return REGISTERED_KEY_MAPPING_SETS[self.nodeType]

    def get_node_type_name(self) -> str:
        return self.nodeType.__name__
