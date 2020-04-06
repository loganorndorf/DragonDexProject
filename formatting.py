import os
import re

directory = "C:\\Users\\SirRunnerMan\\Desktop\\PythonProjects\\formatting.py"

charIconRef = []
cName       = []
baseStar    = []
attribute   = []
unitType    = []


regex = "([a-z_]*[a-z]+_[a-z]+_03\.png)\|([A-Za-z &-]+)\|([0-5])\|([0-5])\|([0-5])"
with open("dragons_info.csv", "r") as a_file:
    for line in a_file:
        print(line)
        m = re.match(regex, line)
        charIconRef.append(m.group(1))
        cName.append(m.group(2))
        baseStar.append(m.group(3))
        attribute.append(m.group(4))
        unitType.append(m.group(5))
a_file.close()

# attribute|baseStarCount|cName|iconRef|unitType
with open("output.csv", "w") as f:
    for i in range(len(cName)):
        f.writelines('%d|%d|%d|%s|%s\n' % (int(attribute[i]), int(baseStar[i]), int(unitType[i]), cName[i], charIconRef[i]))

f.close()
