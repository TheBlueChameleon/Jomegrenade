from .Base import *
from .ModelNode import ModelNode

# ==================================================================================================================== #

@dataclass
class EnumValue(ModelNode):
    value: None | int = None
    docString: str = None

    KNOWN_KEYS = {
        KEY_PRIMITIVE: FIELD_VALUE,
        KEY_NAME: FIELD_NAME,
        KEY_VALUE: FIELD_VALUE,
        KEY_DOCSTRING: FIELD_DOCSTRING
    }
    PRIMITIVE_PAIR = (KEY_NAME, KEY_VALUE)

    def get_repr_details(self) -> str:
        return f": {self.value}"