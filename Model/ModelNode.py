from .Base import get_type_name, ModelError, NamedElement, REGISTERED_TYPES
from .CtorDictHandler import CtorDictHandler

# ==================================================================================================================== #

class RegisterModelTypeMeta(type['ModelNode']):
    def __new__(cls, *args, **kwargs):
        new_class = super().__new__(cls, *args, **kwargs)
        key = args[0].lower()
        if key != "modelnode":
            REGISTERED_TYPES[key] = new_class
        return new_class

# ==================================================================================================================== #

class ModelNode(NamedElement, CtorDictHandler, metaclass=RegisterModelTypeMeta):
    def add(self, arg: NamedElement):
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
        def get_structured_repr_impl(container : ModelNode, depth: int = 1) -> list[str]:
            result = []
            for node in container.get_children():
                result.append(f"{' ' * depth}{node.name} ({get_type_name(node)}){node.get_repr_details()}")
                lines_ = get_structured_repr_impl(node, depth + 1)
                result.extend(lines_)
            return result

        lines = [self.name] + get_structured_repr_impl(self)
        return "\n".join(lines)

    def get_children(self) -> list['ModelNode']:
        return []

    def get_repr_details(self) -> str:
        return ""