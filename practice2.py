import xml.etree.ElementTree as xml
import re
from operator import attrgetter

pomFile = xml.parse('pom.xml')
pattern = '\\$\\{.*\\}'

root = pomFile.getroot()

print(root)

# print(root.findall(''))

# for child in root:
#     # print(child.tag, child.attrib)
#     print(child)

def put_in_props(count):
    parent = root.find('{http://maven.apache.org/POM/4.0.0}properties')

    if count>7:
        a = xml.Element("{http://maven.apache.org/POM/4.0.0}a")
        a.text = "2"
        a.tail = "\n    "
    else:
        a = xml.Element("{http://maven.apache.org/POM/4.0.0}b")
        a.text = str(count)
        a.tail = "\n    "

    parent.append(a)

    # for child in parent:
    #     print(child.text)

    # new = xml.SubElement( parent, 'cdn.v')
    # new.text = '7.5.5.5'
    #
    # data = root.find('{http://maven.apache.org/POM/4.0.0}properties')
    # new = xml.SubElement(data, 'mvp')
    # new.text = 'FOUR'

    # item_id = root.findtext('dependencies')

    # new_data = xml.SubElement(parent, 'xmmm')
    # new_data.text = 'New Data'


for count,actor in enumerate(root.findall('{http://maven.apache.org/POM/4.0.0}dependencies/{http://maven.apache.org/POM/4.0.0}dependency')):
    version = actor.find('{http://maven.apache.org/POM/4.0.0}version')
    group_id = actor.find('{http://maven.apache.org/POM/4.0.0}groupId')

    # print(version.text)

    if not bool(re.search(pattern, version.text)):
        version.text = '${' + group_id.text + '.version}'
        put_in_props(count)


parent = root.find('{http://maven.apache.org/POM/4.0.0}properties')

for child in parent:
    print(child.tag, child.text)


for node in root.findall("{http://maven.apache.org/POM/4.0.0}properties"):
    node[:] = sorted(node, key=attrgetter("tag"))

print('--------')

for child in parent:
    print(child.tag, child.text)

# print(root)

# root.write('file-after-edits.xml', encoding='utf8')

# pomFile.write('file-after-edits.xml')

xml.register_namespace('', "http://maven.apache.org/POM/4.0.0")

pomFile.write(open('file-after-edits.xml', 'w'), encoding='unicode')


# for actor in root.findall('{http://maven.apache.org/POM/4.0.0}properties'):
#
#     # version = actor.find('{http://maven.apache.org/POM/4.0.0}version')
#
#     pp = actor.find('{http://maven.apache.org/POM/4.0.0}cdn.v')
#
#     print(pp.text)

# for mapping in root.findall('*//groupId'):
#
#     print(mapping)

# for stuff in root.findall('Soteria'):
#     print(stuff)
#     root.remove(stuff)

# print ET.tostring(root)


# word = "${gvsakj}"
#
# word2 = "2.4.5"
#
# print(bool(re.search('\\$\\{.*\\}', word)))