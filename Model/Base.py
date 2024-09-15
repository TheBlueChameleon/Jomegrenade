from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum as PyEnum

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
KEY_PRIMITIVE = "#primitive"
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
        return {
            cls.KNOWN_KEYS[key] : value
            for key, value in primitive_handled.items()
            if cls.KNOWN_KEYS.get(key, None) is not None
        }

    @classmethod
    def handle_primitive_pair(cls, descriptor: OrderedDict):
        if cls.PRIMITIVE_PAIR is not None:
            key = cls.PRIMITIVE_PAIR[0]
            val = cls.PRIMITIVE_PAIR[1]
            unknown_keys = cls.get_unknown_args_from(descriptor)
            if len(unknown_keys) == 1:
                descriptor[key] = next(iter(unknown_keys.keys()))
                descriptor[val] = next(iter(unknown_keys.values()))
        return descriptor

    @classmethod
    def get_unknown_args_from(cls, descriptor: OrderedDict):
        # todo: warn on any special keys (.startswith(#)
        return {key: value
            for key, value in descriptor.items()
                if key not in cls.KNOWN_KEYS
        }

# ==================================================================================================================== #

def get_type_name(obj) -> str:
    return type(obj).__name__

def split_descriptor(descriptor: str) -> OrderedDict:
    # identify cases:
    #   primitive: "int", "zero", "3"
    #       return {"#primitive": descriptor}
    #   structured: "key1:value1; key2 : value2    ; ..."
    #       return { key1: value1, key2: value2, ...}
    #   (partially) malformed: "key1; key2:value;; seg1:seg2:seg3; ..."
    #       return dict of valid portions, warn on split residue

    categories = descriptor.split(";")
    paired: map[str] = map(lambda c: c.split("="), categories)
    stripped = list(
        tuple(element.strip() for element in pair)
        for pair in paired
    )

    if len(stripped) == 1 and len(stripped[0]) == 1:
        return OrderedDict([(KEY_PRIMITIVE, descriptor.strip())])

    valid = filter(
        lambda pair: len(pair) == 2,
        stripped
    )

    # todo: warn malformed

    return OrderedDict(valid)
