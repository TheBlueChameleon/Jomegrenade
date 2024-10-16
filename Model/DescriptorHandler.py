from collections import OrderedDict
from typing import Iterator

from Model import KEY_IMPLICIT, KEY_TYPE, REGISTERED_TYPES, ModelNode


# ==================================================================================================================== #

def split_descriptor(descriptor: str) -> OrderedDict:
    units: list[str] = descriptor.split(";")
    unit_pairs: Iterator[list[str]] = map(lambda c: c.split("="), units)
    stripped_pairs: list[tuple[str, ...]] = list(
        tuple(element.strip() for element in pair)
        for pair in unit_pairs
    )

    valid_pairs: list[tuple[str, ...]] = []
    malformed_pairs: list[tuple] = []
    singles: list[str] = []
    for pair in stripped_pairs:
        if len(pair) == 1: singles.append(pair[0])
        elif len(pair) == 2: valid_pairs.append(pair)
        else: malformed_pairs.append(pair)

    result = OrderedDict(valid_pairs)

    if len(singles) == 1:
        result[KEY_IMPLICIT] = singles[0]
    elif len(singles) > 1:
        result[KEY_IMPLICIT] = singles

    # todo: warn malformed

    return result

def get_explicit_node_type_or(descriptor: OrderedDict, fallback: type[ModelNode]) -> type[ModelNode] | None:
    typename = descriptor.get(KEY_TYPE, None)
    if typename is None:
        return fallback
    else:
        # todo: warn on malformed
        return REGISTERED_TYPES.get(typename, fallback)