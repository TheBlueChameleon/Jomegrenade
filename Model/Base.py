from collections import OrderedDict, namedtuple
from dataclasses import dataclass
from enum import Enum as PyEnum
from typing import Iterator

# ==================================================================================================================== #
# base types

class ModelError(Exception): pass

@dataclass
class NamedElement:
    name:str

SpecialTreatment = PyEnum("SpecialTreatment", ["none", "optional", "vector"])
ByReferenceTreatment = PyEnum("ByReferenceTreatment", ["true", "false", "auto"])
VisibilityTypes = PyEnum("VisibilityType", ["private", "protected", "public"])

PrimitiveDeclaration = namedtuple("PrimitiveDeclaration", ["field_key", "field_value"])

# ==================================================================================================================== #
# constants

DEFAULT_CONFIG_NAME = "#config"

KEY_BASECLASS = "#baseclass"
KEY_NAME = "#name"
KEY_DEFAULT = "#default"
KEY_DOCSTRING = "#docString"
KEY_DOCSTRING_GETTER = "#docStringGetter"
KEY_DOCSTRING_SETTER = "#docStringSetter"
KEY_DOCSTRING_RESETTER = "#docStringResetter"
KEY_PRIMITIVE = type("Primitive", tuple(), dict())()        # instance of run time class Primitive
KEY_SPECIAL = "#special"
KEY_TYPE = "#type"
KEY_VALUE = "#value"

FIELD_BASECLASS = "baseclass"
FIELD_CLASSES = "classes"
FIELD_DEFAULT = "default"
FIELD_DOCSTRING = "docString"
FIELD_DOCSTRING_GETTER = "docStringGetter"
FIELD_DOCSTRING_SETTER = "docStringSetter"
FIELD_DOCSTRING_RESETTER = "docStringResetter"
FIELD_NAME = "name"
FIELD_RECORDS = "records"
FIELD_SPECIAL = "special"
FIELD_TYPE = "type"
FIELD_VALUE = "value"
FIELD_VALUES = "values"

# ==================================================================================================================== #
# public util funcs

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
