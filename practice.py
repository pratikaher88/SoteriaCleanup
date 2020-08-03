# lines = open('pom.xml').readlines()
#
# for aline in lines:
#
#     print(aline)

file = "pom.xml"

# a_file = open(file, "r")
#
# lines = a_file.readlines()
# a_file.close()


with open(file, "r") as f:
    lines = f.readlines()


with open(file, "w") as f:
    for line in lines:

        if "Soteria" not in line:
            f.write(line)
