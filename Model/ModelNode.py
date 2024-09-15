from collections import OrderedDict

from Model import NamedElement, FIELD_NAME
from Model.Base import get_type_name, ModelError, split_descriptor, CtorDictHandler, KEY_NAME


class ModelNode(NamedElement, CtorDictHandler):
    def add_enum_value(self, arg: NamedElement):
        raise self.get_add_error_type(arg)

    def add_enum_value_set(self, arg: NamedElement):
        raise self.get_add_error_type(arg)

    def add_record(self, arg: NamedElement):
        raise self.get_add_error_type(arg)

    def add_record_set(self, arg: NamedElement):
        raise self.get_add_error_type(arg)

    def add_enum(self, arg: NamedElement):
        raise self.get_add_error_type(arg)

    def add_class(self, arg: NamedElement):
        raise self.get_add_error_type(arg)

    def add_namespace(self, arg: NamedElement):
        raise self.get_add_error_type(arg)

    def get_base_add_error_message(self, arg: NamedElement) -> str:
        return f"Cannot add {get_type_name(arg)} '{arg.name}' to {get_type_name(self)} '{self.name}': "

    def get_add_error_type(self, arg: NamedElement) -> ModelError:
        return ModelError(self.get_base_add_error_message(arg) + "types incompatible")

    def add_with_duplicate_check(self, arg: NamedElement, elements: list[NamedElement]):
        if arg.name in map(lambda element: element.name, elements):
            raise ModelError(self.get_base_add_error_message(arg) + "such an element is already present")
        else:
            elements.append(arg)

    def get_structured_repr(self, include_config: bool = False) -> str:
        def get_structured_repr_impl(container : ModelNode, depth: int = 0) -> list[str]:
            result = []
            for node in container.get_children():
                result.append(f"{' ' * depth}{node.name} ({get_type_name(node)}){node.get_repr_details()}")
                lines_ = get_structured_repr_impl(node, depth + 1)
                result.extend(lines_)
            return result

        lines = get_structured_repr_impl(self)
        return "\n".join(lines) if len(lines) > 0 else ["<empty>"]

    def get_children(self) -> list['ModelNode']:
        return []

    def get_repr_details(self) -> str:
        return ""

    @classmethod
    def from_name_and_string(cls, name: str, descriptor: str):
        d = split_descriptor(descriptor)
        d[KEY_NAME] = name
        return cls.from_ordered_dict(d)

    @classmethod
    def from_string(cls, descriptor: str):
        return cls.from_ordered_dict(split_descriptor(descriptor))

    @classmethod
    def from_ordered_dict(cls, descriptor: OrderedDict):
        return cls(**cls.get_ctor_args_from(descriptor))


