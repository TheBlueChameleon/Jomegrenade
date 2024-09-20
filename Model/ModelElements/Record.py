from dataclasses import field

from Model.Base import *
from Model.ModelNode import ModelNode
from .Config import Config

# ==================================================================================================================== #

@dataclass
class Record(ModelNode):
    type: str
    default: str = None
    docStringGetter: str = None
    docStringSetter: str = None
    docStringResetter: str = None
    special: PyEnum = SpecialTreatment.none
    config: Config = field(default_factory=lambda: Config(DEFAULT_CONFIG_NAME))

    IMPLICIT_PAIR = ImplicitDeclaration(KEY_NAME, KEY_TYPE)
    KNOWN_KEYS = {
        KEY_IMPLICIT: FIELD_TYPE,
        KEY_TYPE: FIELD_TYPE,
        KEY_NAME: FIELD_NAME,
        KEY_DEFAULT: FIELD_DEFAULT,
        KEY_DOCSTRING_GETTER: FIELD_DOCSTRING_GETTER,
        KEY_DOCSTRING_SETTER: FIELD_DOCSTRING_SETTER,
        KEY_DOCSTRING_RESETTER: FIELD_DOCSTRING_RESETTER,
        KEY_SPECIAL: FIELD_SPECIAL
    }

    def get_repr_details(self) -> str:
        return f": {self.type} {f'= {self.default}' if self.default is not None else ''}"