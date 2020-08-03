import xml.etree.ElementTree as xml
import re
from operator import attrgetter
import sys

class CommentedTreeBuilder(xml.TreeBuilder):
    def comment(self, data):
        self.start(xml.Comment, {})
        self.data(data)
        self.end(xml.Comment)

class SoteriaCleanup:

    def __init__(self, file_name = 'pom3.xml'):
        file = file_name
        self.final_file = file_name
        self.name_space = 'http://maven.apache.org/POM/4.0.0'
        self.pomFile = xml.parse(file, xml.XMLParser(target=CommentedTreeBuilder()))
        self.dependency_path = '{http://maven.apache.org/POM/4.0.0}dependencies/{http://maven.apache.org/POM/4.0.0}dependency'
        self.properties_path = '{http://maven.apache.org/POM/4.0.0}properties'
        self.pattern = '\\$\\{.*\\}'
        self.root = self.pomFile.getroot()

        self.find_and_extract_versions()
        self.remove_duplicate_properties()
        self.sort_properties()
        self.remove_soteria_comments()
        self.final_write()


    def find_and_extract_versions(self):

        for count, actor in enumerate(self.root.findall(self.dependency_path)):
            version = actor.find('{http://maven.apache.org/POM/4.0.0}version')
            group_id = actor.find('{http://maven.apache.org/POM/4.0.0}groupId')

            # print(version.text)

            if not bool(re.search(self.pattern, version.text)):

                original_version = version.text
                version.text = '${' + group_id.text + '.version}'

                self.put_in_props(group_id.text + '.version', original_version)



    def put_in_props(self, verion_prop, version_text):

        parent = self.root.find('{http://maven.apache.org/POM/4.0.0}properties')

        element = xml.Element("{http://maven.apache.org/POM/4.0.0}"+verion_prop)

        element.text = version_text
        element.tail = "\n    "

        parent.append(element)

    def sort_properties(self):

        for node in self.root.findall(self.properties_path):

            node[:] = sorted(node, key=attrgetter("tag"))

    def remove_soteria_comments(self):

        for child in self.root:
            if 'Soteria' in child.text:
                self.root.remove(child)


    def final_write(self):
        xml.register_namespace('', self.name_space)

        self.pomFile.write(open(self.final_file, 'w'), encoding='unicode')

    def remove_duplicate_properties(self):

        unique_elements = []
        elements_to_remove = []

        for node in self.root.find(self.properties_path):

            if (node.tag, node.text) in unique_elements:
                elements_to_remove.append(node)
            else:
                unique_elements.append((node.tag,node.text))

        for elem in elements_to_remove:
            self.root.find(self.properties_path).remove(elem)

        for node in self.root.find(self.properties_path):
            print(node.tag, node.text)




if __name__ == "__main__":
    # print(str(sys.argv[1]))
    # SoteriaCleanup(str(sys.argv[1]))
    SoteriaCleanup()