import json

with open("ModelDescriptors/showcase.json", "r") as fp:
    data = json.load(fp)
    print(data)
    print(data["Project"]["Foo"])