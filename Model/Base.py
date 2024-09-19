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
KEY_PRIMITIVE = type("Primitive", tuple(), dict())()        # disallow an explicit primitive key in the JSON model
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

TYPENAME_CLASS = "class"
TYPENAME_ENUM = "enum"
TYPENAME_NAMESPACE = "namespace"

# ==================================================================================================================== #
# public util funcs

def get_type_name(obj) -> str:
    return type(obj).__name__

