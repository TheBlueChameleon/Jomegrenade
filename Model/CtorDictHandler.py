from collections import OrderedDict
from typing import Any

from . import ModelNode
from .Base import *
from .DescriptorHandler import split_descriptor


# ==================================================================================================================== #

class CtorDictHandler:
    IMPLICIT_PAIR: ImplicitDeclaration | None = None
    KNOWN_KEYS = dict()

    @classmethod
    def get_ctor_args(cls, descriptor: OrderedDict) -> OrderedDict[str, Any]:
        cls.handle_implicit_pair(descriptor)
        return OrderedDict(
            (cls.KNOWN_KEYS[key], value)
            for key, value in descriptor.items()
            if cls.KNOWN_KEYS.get(key, None) is not None
        )

    @classmethod
    def handle_implicit_pair(cls, descriptor: OrderedDict):
        def get_first_key(od: OrderedDict):
            return next(iter(od.keys()))
        def get_first_value(od: OrderedDict):
            return next(iter(od.values()))

        if cls.IMPLICIT_PAIR is not None:
            unknown_keys = cls.get_unknown_args(descriptor)
            if len(unknown_keys) == 1:
                descriptor[cls.IMPLICIT_PAIR.field_key] = get_first_key(unknown_keys)
                descriptor[cls.IMPLICIT_PAIR.field_value] = get_first_value(unknown_keys)

    @classmethod
    def get_config_args(cls, descriptor: OrderedDict):
        # todo
        pass

    @classmethod
    def get_unknown_args(cls, descriptor: OrderedDict):
        # todo: warn on any special keys (.startswith(#))
        return OrderedDict(
            (key, value)
            for key, value in descriptor.items()
            if key not in cls.KNOWN_KEYS
        )

    @classmethod
    def get_delegate_nodes(cls, delegate_class: type[ModelNode], descriptor: OrderedDict):
        unused = cls.get_unknown_args(descriptor)
        impl = descriptor.get(KEY_IMPLICIT, None)
        if impl is not None:
            unused[KEY_IMPLICIT] = descriptor[KEY_IMPLICIT]

        forward_nodes = []
        for key, value in unused.items():
            if isinstance(value, str):
                forward_nodes.append(delegate_class.from_name_and_string(key, value))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        forward_nodes.append(delegate_class.from_list_string(item))
                    else:
                        # TODO proper log and warning handling
                        print("warning message: unknown JSON element:", item)
            else:
                # TODO proper log and warning handling
                print("warning message: unknown JSON element:", value)
        return forward_nodes

    @classmethod
    def from_string(cls, descriptor: str):
        return cls.from_ordered_dict(split_descriptor(descriptor))

    @classmethod
    def from_list_string(cls, descriptor: str):
        return cls.from_string(descriptor)

    @classmethod
    def from_name_and_string(cls, name: str, descriptor: str):
        od = split_descriptor(descriptor)
        od[KEY_NAME] = name
        return cls.from_ordered_dict(od)

    @classmethod
    def from_ordered_dict(cls: type['CtorDictHandler', Any], descriptor: OrderedDict):
        ctor_args = cls.get_ctor_args(descriptor)
        return cls(**ctor_args)
