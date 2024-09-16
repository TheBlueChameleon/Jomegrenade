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
    PRIMITIVE_PAIR = (KEY_NAME, KEY_VALUE)

    def get_repr_details(self) -> str:
        return f": {self.value}"

    @classmethod
    def get_ctor_args_from(
            cls,
            descriptor: OrderedDict,
            primitive_handling_policy: PrimitiveHandlingPolicy = PrimitiveHandlingPolicy.default
    ):
        # todo: remove this EVIL HACK
        if primitive_handling_policy == PrimitiveHandlingPolicy.from_list:
            cls.KNOWN_KEYS[KEY_PRIMITIVE] = FIELD_NAME
        result = super().get_ctor_args_from(descriptor, primitive_handling_policy)
        if primitive_handling_policy == PrimitiveHandlingPolicy.from_list:
            cls.KNOWN_KEYS[KEY_PRIMITIVE] = FIELD_VALUE
        return result