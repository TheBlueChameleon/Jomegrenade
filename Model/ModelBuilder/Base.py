from dataclasses import dataclass

from Model import *

# ==================================================================================================================== #
# base types

@dataclass(frozen=True)
class SpecialKey:
    key: str
    content_class: type

@dataclass
class SpecialKeysCollection:
    keys: set[SpecialKey]
    default: type | None

    def get_model_class_or_none(self, key):
        return next(
            (sk.content_class for sk in self.keys if sk.key == key),
            None                                            # default
        )

    def get_key_set(self):
        return self.keys

# ==================================================================================================================== #
