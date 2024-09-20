from Model import *
from Model.DescriptorHandler import split_descriptor

# ==================================================================================================================== #

x = get_model_from_file("./test/ModelDescriptors/showcase.json").get_structured_repr()
print()
print(x)
print("---")
print(Record.from_string("foo=int"))
print(EnumValue.from_string("foo=5"))

# ==================================================================================================================== #

def keepForTest():
    ca = Config(DEFAULT_CONFIG_NAME, hasGetter=True)
    cb = Config(DEFAULT_CONFIG_NAME, hasSetter=False)

    print(ca.get_merged_with(cb))
    print(ca)
    print(cb)

    e = Enum("name")
    e.add_enum_value(EnumValue("five", value=5))
    e.add_record(Record("name", "val"))
    e.add_enum_value(EnumValue("five", 6))

    print()
    print(split_descriptor("foobar"))
    print(split_descriptor("foo:bar; FOO : BAR"))
    print(split_descriptor("foo; FOO : BAR : BAZ; valid: part"))

    print()
    print(EnumValue.from_string("foo"))
    print(EnumValue.from_string("foo:2"))
    print(EnumValue.from_string("foo:2; docString: bar"))

    print()
    #print(Record.from_string("foo"))
    print(Record.from_string("foo:int"))
    print(Record.from_string("foo:int; #default:2; #docStringGetter: bar"))
