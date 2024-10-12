from Model.Base import *
from Model.DescriptorHandler import split_descriptor
from Model.ModelNode import ModelNode

# ==================================================================================================================== #

@dataclass
class EnumValue(ModelNode):
    value: None | int = None
    docString: str = None

    KNOWN_KEYS = {
        KEY_IMPLICIT: FIELD_VALUE,   # todo: fix the EVIL HACK down below
        KEY_NAME: FIELD_NAME,
        KEY_VALUE: FIELD_VALUE,
        KEY_DOCSTRING: FIELD_DOCSTRING
    }
    IMPLICIT_PAIR = ImplicitDeclaration(KEY_NAME, KEY_VALUE)

    def get_repr_details(self) -> str:
        return f": {self.value}"

    @classmethod
    def from_list_string(cls, descriptor: str):
        # EVIL HACK
        cls.KNOWN_KEYS[KEY_IMPLICIT] = FIELD_NAME
        result = cls.from_string(descriptor)
        cls.KNOWN_KEYS[KEY_IMPLICIT] = FIELD_VALUE
        return result

    @classmethod
    def from_name_and_string(cls, name: str, descriptor: str):
        od = split_descriptor(descriptor)
        if name is KEY_IMPLICIT:
            name = od.pop(KEY_IMPLICIT)
        od[KEY_NAME] = name
        return super().from_ordered_dict(od)