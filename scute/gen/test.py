import json

out = ""

with open("data.json") as file:
    for item in json.load(file):
        out += f'\n{item} = "{item}"'

print(out)
