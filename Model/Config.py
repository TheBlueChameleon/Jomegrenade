from copy import copy
from dataclasses import dataclass
from enum import Enum as PyEnum

from .ModelNode import ModelNode
from .Base import ByReferenceTreatment


# ==================================================================================================================== #

@dataclass
class Config(ModelNode):
    hasGetter: bool = None
    hasSetter: bool = None
    hasResetter: bool = None
    getByReference: ByReferenceTreatment = None
    setByReference: ByReferenceTreatment = None
    visibilityRecord: PyEnum = None
    visibilityGetter: PyEnum = None
    visibilitySetter: PyEnum = None
    visibilityResetter: PyEnum = None
    visibilityInnerTypes: PyEnum = None
    isMonadic: bool = None
    strictEnums: bool = None

    # TODO: KNOWN_KEYS = {...}

    def get_merged_with(self, parent):
        result = copy(self)
        for attribute, value in vars(parent).items():
            if getattr(result, attribute) is None and getattr(parent, attribute) is not None:
                setattr(result, attribute, value)
        return result
