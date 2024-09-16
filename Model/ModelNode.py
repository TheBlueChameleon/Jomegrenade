from collections import OrderedDict

from Model import NamedElement
from Model.Base import get_type_name, ModelError, split_descriptor, CtorDictHandler, KEY_NAME, PrimitiveHandlingPolicy


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
    def from_string(
            cls, descriptor: str,
            primitive_handling_policy: PrimitiveHandlingPolicy = PrimitiveHandlingPolicy.default
    ):
        return cls.from_ordered_dict(split_descriptor(descriptor), primitive_handling_policy)

    @classmethod
    def from_name_and_string(cls, name: str, descriptor: str):
        d = split_descriptor(descriptor)
        d[KEY_NAME] = name
        return cls.from_ordered_dict(d)

    @classmethod
    def from_ordered_dict(
            cls,
            descriptor: OrderedDict,
            primitive_handling_policy: PrimitiveHandlingPolicy = PrimitiveHandlingPolicy.default
    ):
        td = cls.get_ctor_args_from(descriptor, primitive_handling_policy)
        return cls(**td)

    @classmethod
    def get_delegate_nodes(cls, delegate_class: type['ModelNode'], descriptor: OrderedDict):
        unused = cls.get_unknown_args_from(descriptor)
        forward_nodes = []
        for key, value in unused.items():
            if isinstance(value, str):
                forward_nodes.append(delegate_class.from_name_and_string(key, value))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        forward_nodes.append(delegate_class.from_string(item, PrimitiveHandlingPolicy.from_list))
                    else:
                        # TODO proper log and warning handling
                        print("warning message: unknown JSON element:", item)
            else:
                # TODO proper log and warning handling
                print("warning message: unknown JSON element:", value)
        return forward_nodes
