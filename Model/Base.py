from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum as PyEnum
from typing import Iterator

# ==================================================================================================================== #

SpecialTreatment = PyEnum("SpecialTreatment", ["none", "optional", "vector"])
VisibilityTypes = PyEnum("VisibilityType", ["private", "protected", "public"])

DEFAULT_CONFIG_NAME = "#config"

KEY_BASECLASS = "#baseclass"
KEY_NAME = "#name"
KEY_DEFAULT = "#default"
KEY_DOCSTRING = "#docString"
KEY_DOCSTRING_GETTER = "#docStringGetter"
KEY_DOCSTRING_SETTER = "#docStringSetter"
KEY_DOCSTRING_RESETTER = "#docStringResetter"
KEY_PRIMITIVE = type("Primitive", tuple(), dict())()        # instance of run time class Primitive
KEY_TYPE = "#type"
KEY_VALUE = "#value"

FIELD_BASECLASS = "baseclass"
FIELD_DEFAULT = "default"
FIELD_DOCSTRING = "docString"
FIELD_DOCSTRING_GETTER = "docStringGetter"
FIELD_DOCSTRING_SETTER = "docStringSetter"
FIELD_DOCSTRING_RESETTER = "docStringResetter"
FIELD_NAME = "name"
FIELD_RECORDS = "records"
FIELD_TYPE = "type"
FIELD_VALUE = "value"
FIELD_VALUES = "values"

# ==================================================================================================================== #

class ModelError(Exception): pass

# ==================================================================================================================== #

@dataclass
class NamedElement:
    name:str

# ==================================================================================================================== #

class CtorDictHandler:
    PRIMITIVE_PAIR: tuple | None = None
    KNOWN_KEYS = dict()

    @classmethod
    def get_ctor_args_from(cls, descriptor: OrderedDict):
        primitive_handled = cls.handle_primitive_pair(descriptor)
        return OrderedDict(
            (cls.KNOWN_KEYS[key], value)
            for key, value in primitive_handled.items()
            if cls.KNOWN_KEYS.get(key, None) is not None
        )

    @classmethod
    def handle_primitive_pair(cls, descriptor: OrderedDict):
        if cls.PRIMITIVE_PAIR is not None:
            primitive_key = cls.PRIMITIVE_PAIR[0]
            primitive_val = cls.PRIMITIVE_PAIR[1]
            unknown_keys = cls.get_unknown_args_from(descriptor)
            if len(unknown_keys) == 1:
                descriptor[primitive_key] = next(iter(unknown_keys.keys()))
                descriptor[primitive_val] = next(iter(unknown_keys.values()))
        return descriptor

    @classmethod
    def get_unknown_args_from(cls, descriptor: OrderedDict):
        # todo: warn on any special keys (.startswith(#))
        return OrderedDict(
            (key, value)
            for key, value in descriptor.items()
            if key not in cls.KNOWN_KEYS
        )

    @classmethod
    def get_delegate_nodes(cls, delegate_class: type['ModelNode'], descriptor: OrderedDict):
        unused = cls.get_unknown_args_from(descriptor)
        forward_nodes = []
        for key, value in unused.items():
            if isinstance(value, str):
                forward_nodes.append(delegate_class.from_name_and_string(key, value))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        forward_nodes.append(delegate_class.from_list_string(item))
                    else:
                        # TODO proper log and warning handling
                        print("warning message: unknown JSON element:", item)
            else:
                # TODO proper log and warning handling
                print("warning message: unknown JSON element:", value)
        return forward_nodes

    @classmethod
    def from_string(cls, descriptor: str):
        return cls.from_ordered_dict(split_descriptor(descriptor))

    @classmethod
    def from_list_string(cls, descriptor: str):
        return cls.from_string(descriptor)

    @classmethod
    def from_name_and_string(cls, name: str, descriptor: str):
        d = split_descriptor(descriptor)
        d[KEY_NAME] = name
        return cls.from_ordered_dict(d)

    @classmethod
    def from_ordered_dict(cls, descriptor: OrderedDict):
        ctor_args = cls.get_ctor_args_from(descriptor)
        return cls(**ctor_args)

# ==================================================================================================================== #

def get_type_name(obj) -> str:
    return type(obj).__name__

def split_descriptor(descriptor: str) -> OrderedDict:
    units: list[str] = descriptor.split(";")
    unit_pairs: Iterator[list[str]] = map(lambda c: c.split("="), units)
    stripped_pairs: list[tuple] = list(
        tuple(element.strip() for element in pair)
        for pair in unit_pairs
    )

    valid_pairs: list[tuple] = []
    malformed_pairs: list[tuple] = []
    singles: list[tuple] = []
    for pair in stripped_pairs:
        if len(pair) == 1: singles.append(pair[0])
        elif len(pair) == 2: valid_pairs.append(pair)
        else: malformed_pairs.append(pair)

    result = OrderedDict(valid_pairs)

    if len(singles) == 1:
        result[KEY_PRIMITIVE] = singles[0]
    elif len(singles) > 1:
        print("malformed:", descriptor)
        print("  ", singles)

    # todo: warn malformed

    return result
