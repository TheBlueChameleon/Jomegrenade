from .Base import *
from .ModelElements import *
from .ModelBuilder.Base import SpecialKey, SpecialKeysCollection

# ==================================================================================================================== #

TYPENAME_TO_TYPE = {
    TYPENAME_CLASS: Class,
    TYPENAME_ENUM: Enum,
    TYPENAME_NAMESPACE: Namespace
}

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