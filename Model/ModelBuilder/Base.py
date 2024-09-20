from dataclasses import dataclass

from Model import *

# ==================================================================================================================== #
# base types

@dataclass(frozen=True)
class KeyMapping:
    key: str
    content_class: type

@dataclass
class KeyMappingSet:
    keys: set[KeyMapping]
    default: type | None

    def get_model_class_or_none(self, key):
        return next(
            (sk.content_class for sk in self.keys if sk.key == key),
            None                                            # default
        )

    def get_key_set(self):
        return self.keys

# ==================================================================================================================== #

KM_TYPE = KeyMapping('#type', str)
KM_CONFIG = KeyMapping('#config', Config)
KM_RECORDS = KeyMapping('#elements', RecordSet)
KM_ENUM_VALUES = KeyMapping('#elements', EnumValueSet)

REGISTERED_KEY_MAPPING_SETS = {
    Class : KeyMappingSet(
        {KM_CONFIG, KM_RECORDS},
        Record
    ),
    Config : KeyMappingSet(
        {KM_CONFIG},
        None
    ),
    Enum : KeyMappingSet(
        {KM_CONFIG, KM_ENUM_VALUES},
        EnumValue
    ),
    EnumValue : KeyMappingSet(
        {KM_CONFIG},
        None
    ),
    EnumValueSet : KeyMappingSet(
        {KM_CONFIG},
        EnumValue
    ),
    Model : KeyMappingSet(
        {KM_CONFIG},
        Namespace
    ),
    Namespace : KeyMappingSet(
        {KM_CONFIG},
        Namespace
    ),
    Record : KeyMappingSet(
        {KM_CONFIG},
        None
    ),
    RecordSet : KeyMappingSet(
        {KM_CONFIG},
        Record
    )
}