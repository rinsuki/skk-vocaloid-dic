import csv
import sys
import glob
import re
import os

result = []

def find_duplicate(name, yomi):
    for r in result:
        if r[0] == name and r[1] == yomi:
            return True
        print(r)
    return False

for filename in glob.glob("./src/*.csv"):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        csvname = os.path.basename(filename).replace(".csv", "")
        for row in reader:
            full_name = ""
            full_yomi = ""
            for (name, yomi) in zip(*[iter(row)]*2):
                full_name += name
                full_yomi += yomi
                if find_duplicate(name, yomi):
                    continue
                if re.search(r"^[\u3040-\u3096]*$", yomi) is None:
                    print("--------------")
                    print("ERR: よみにひらがなでない文字が含まれています:", yomi)
                    exit(1)
                if re.search(r"^([\u3041-\u3096]|[\u30a1-\u30fa])+$", name) is None: # よみがカタカナ/ひらがなだけだったらスルー
                    result.append((name, yomi, csvname))
            result.append((full_name, full_yomi, csvname))
r = ""
for line in result:
    r += "%s /%s;[vocaloid-dic] %s/\n" % (line[1], line[0], line[2])

with open("./SKK-JISYO.vocaloid.utf8", "w") as f:
    f.write(r)