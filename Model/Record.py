from dataclasses import field

from .Base import *
from .ModelNode import ModelNode
from .Config import Config

# ==================================================================================================================== #

@dataclass
class Record(ModelNode):
    type: str
    default: str = None
    docStringGetter: str = None
    docStringSetter: str = None
    docStringResetter: str = None
    config: Config = field(default_factory=lambda: Config(DEFAULT_CONFIG_NAME))

    PRIMITIVE_PAIR = (KEY_NAME, KEY_TYPE)
    KNOWN_KEYS = {
        KEY_PRIMITIVE: FIELD_TYPE,
        KEY_TYPE: FIELD_TYPE,
        KEY_NAME: FIELD_NAME,
        KEY_DEFAULT: FIELD_DEFAULT,
        KEY_DOCSTRING_GETTER: FIELD_DOCSTRING_GETTER,
        KEY_DOCSTRING_SETTER: FIELD_DOCSTRING_SETTER,
        KEY_DOCSTRING_RESETTER: FIELD_DOCSTRING_RESETTER,
    }

    def get_repr_details(self) -> str:
        return f": {self.type} {f'= {self.default}' if self.default is not None else ''}"