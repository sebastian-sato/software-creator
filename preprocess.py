with open("./main.py", "r") as f:
    raw_txt = f.read()

lines = raw_txt.split('\n')
build = "# THIS FILE WAS AUTOMATICALLY GENERATED, CHANGES TO IT WILL NOT BE SAVED!\n\n"
for line in lines:
    if line[:9] == "#!INCLUDE":
        path = line[10:].strip()
        with open(path, "r") as f:
            build += "#START OF MODULE: " + path + "\n"
            build += f.read()
            build += "\n#END OF MODULE\n\n"
    elif "#!REMOVE" in line:
        continue
    else:
        build += line + '\n'

with open("./build.py", "w") as f:
    f.write(build)