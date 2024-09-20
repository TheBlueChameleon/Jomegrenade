__all__ = ["get_model_from_file"]

import json

from Model import *
from Model import ModelNode
from .Base import SK_TYPE
from .Transformer import Transformer


# ==================================================================================================================== #

def get_model_from_file(filename: str) -> ModelNode:
    with open(filename, "r") as fp:
        json_model = json.load(fp, object_pairs_hook=lambda *args, **kwargs:OrderedDict(*args, **kwargs))
        transformer = Transformer(filename, Model)
        traverse(json_model, transformer, transformer)
    return transformer.evaluate()

def traverse(node: OrderedDict, target: Transformer, parent: Transformer, depth: int = 0) -> None:
    for key, value in node.items():
        transformer = get_node_transformer(key, value, target)

        if transformer:
            parent = target
            target = transformer
        else:
            target.add_params(key, value)

        if isinstance(value, OrderedDict):
            traverse(value, target, parent, depth+1)
            target = parent

def get_node_transformer(name: str, content: OrderedDict, parent: Transformer):
    if not isinstance(content, OrderedDict):
        return None

    node_type = get_node_type(name, content, parent)

    if node_type:
        result = Transformer(name, node_type)
        parent.add_child_transformer(result)
        return result
    else:
        return None

def get_node_type(name: str, content: OrderedDict, parent: Transformer):
    special_keys_collection = parent.get_special_keys_collection()
    node_type = special_keys_collection.get_model_class_or_none(name)

    if node_type is None:
        type_name = content.get(SK_TYPE.key, None)
        node_type = REGISTERED_TYPES.get(type_name, None)

    if node_type is None:
        node_type = special_keys_collection.default

    return node_type
