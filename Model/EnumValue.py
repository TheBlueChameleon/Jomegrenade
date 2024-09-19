from .Base import *
from .ModelNode import ModelNode

# ==================================================================================================================== #

@dataclass
class EnumValue(ModelNode):
    value: None | int = None
    docString: str = None

    KNOWN_KEYS = {
        KEY_PRIMITIVE: FIELD_VALUE,   # todo: fix the EVIL HACK down below
        KEY_NAME: FIELD_NAME,
        KEY_VALUE: FIELD_VALUE,
        KEY_DOCSTRING: FIELD_DOCSTRING
    }
    PRIMITIVE_PAIR = PrimitiveDeclaration(KEY_NAME, KEY_VALUE)

    def get_repr_details(self) -> str:
        return f": {self.value}"

    @classmethod
    def from_list_string(cls, descriptor: str):
        # EVIL HACK
        cls.KNOWN_KEYS[KEY_PRIMITIVE] = FIELD_NAME
        result = cls.from_string(descriptor)
        cls.KNOWN_KEYS[KEY_PRIMITIVE] = FIELD_VALUE
        return result

