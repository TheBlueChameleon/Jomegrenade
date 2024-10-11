from collections import namedtuple
from dataclasses import dataclass
from enum import Enum as PyEnum

from Model.MetaCode import Singleton


# ==================================================================================================================== #
# base types

class ModelError(Exception): pass

@dataclass
class NamedElement:
    name:str

SpecialTreatment = PyEnum("SpecialTreatment", ["none", "optional", "vector"])
ByReferenceTreatment = PyEnum("ByReferenceTreatment", ["true", "false", "auto"])
VisibilityTypes = PyEnum("VisibilityType", ["private", "protected", "public"])

ImplicitDeclaration = namedtuple("ImplicitDeclaration", ["field_key", "field_value"])

class ImplicitKey(metaclass=Singleton):
    def __repr__(self):
        return "<IMPLICIT KEY OBJECT>"

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
KEY_IMPLICIT = ImplicitKey()
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
FIELD_ENUMS = "enums"
FIELD_NAME = "name"
FIELD_NAMESPACES = "namespaces"
FIELD_RECORDS = "records"
FIELD_SPECIAL = "special"
FIELD_TYPE = "type"
FIELD_VALUE = "value"
FIELD_VALUES = "values"

TYPENAME_CLASS = "class"
TYPENAME_ENUM = "enum"
TYPENAME_NAMESPACE = "namespace"

REGISTERED_TYPES = dict()
    # types are registered on definition in ModelElements submodule

# ==================================================================================================================== #
# public util funcs

def get_type_name(obj) -> str:
    return type(obj).__name__

