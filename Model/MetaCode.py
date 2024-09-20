from Model import REGISTERED_TYPES

class RegisterModelTypeMeta(type['ModelNode']):
    def __new__(cls, *args, **kwargs):
        new_class = super().__new__(cls, *args, **kwargs)
        key = args[0].lower()
        if key != "modelnode":
            REGISTERED_TYPES[key] = new_class
        return new_class
