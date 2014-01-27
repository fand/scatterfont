import os

namelist = map(lambda x: x[:-4], filter(lambda x: x[-4:] == ".svg", os.listdir("svg")))

with open("droidsans.css", "r") as f:
    template = f.read()

for n in namelist:
    temp = template.replace("droidsans", n)
    with open(n+".css", "w") as f:
        f.write(temp)
