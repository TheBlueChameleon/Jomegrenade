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

SK_TYPE = SpecialKey('#type', str)
SK_CONFIG = SpecialKey('#config', Config)
SK_RECORDS = SpecialKey('#elements', RecordSet)
SK_ENUM_VALUES = SpecialKey('#elements', EnumValueSet)

SPECIAL_KEYS_DICT = {
    Class : SpecialKeysCollection(
        {SK_CONFIG, SK_RECORDS},
        Record
    ),
    Config : SpecialKeysCollection(
        {SK_CONFIG},
        None
    ),
    Enum : SpecialKeysCollection(
        {SK_CONFIG, SK_ENUM_VALUES},
        EnumValue
    ),
    EnumValue : SpecialKeysCollection(
        {SK_CONFIG},
        None
    ),
    EnumValueSet : SpecialKeysCollection(
        {SK_CONFIG},
        EnumValue
    ),
    Model : SpecialKeysCollection(
        {SK_CONFIG},
        Namespace
    ),
    Namespace : SpecialKeysCollection(
        {SK_CONFIG},
        Namespace
    ),
    Record : SpecialKeysCollection(
        {SK_CONFIG},
        None
    ),
    RecordSet : SpecialKeysCollection(
        {SK_CONFIG},
        Record
    )
}