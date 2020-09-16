import os

def files(folder):
    ret = []
    for path, subdirs, files in os.walk(folder):
        for name in files:
            ret.append(os.path.join(path, name))
    return ret

f = files("./src")
for fileName in f:
    with open(fileName, "r") as file:
        data = file.read()
        if "item" in data:
            index = data.index("item")
            end_index = data.index(")", index)
            sub = data[(index + 4):(index + (end_index - (index)))]
            item_params = sub.split(", ")
            if len(item_params) == 3: print(item_params[len(item_params) - 1])
        file.close()
