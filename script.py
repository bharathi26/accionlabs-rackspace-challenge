#!/usr/bin/env python
#/***********************************************************************/
# * description        :   This python module is used for parses text file and produces formatted output text file
# * author             :   Bharathi Kannan D
# * email              :   bharathi26.kannan@gmail.com
# * lib dependencies   :   pip install lxml 
#/***********************************************************************/
import sys
from collections import defaultdict
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

root = etree.Element("html")
root.set('version', '1.0.1')
tag_dict = defaultdict(lambda: 1)
processedLines = []


def transform_data():
    line_list = [line.strip() for line in sys.stdin if len(line.strip()) != 0]

    # start transforming the data
    parent_element = root
    ul_parent_element = None
    try:
        for line in line_list:
            tag_len = len(line.partition(' ')[0])
            if line.startswith("*"):
                p_element = root if tag_len == 1 else tag_dict["ph%s" % (tag_len-1)]
                h1 = etree.SubElement(p_element, "h%s" % tag_len)
                h1.set("text_val", line[tag_len + 1:])
                index = str(tag_dict["h%s" % tag_len]) if tag_len == 1 else "%s.%s" % \
                         (p_element.get("index"), str(tag_dict["h%s" % tag_len]))
                h1.set("index", index)
                parent_element, tag_dict["ph%s" % tag_len] = h1, h1
                tag_dict["h%s" % tag_len] += 1
            elif line.startswith("."):
                p_element = parent_element if tag_len == 1 else tag_dict["pu%s" % (tag_len -1)]
                ul1 = etree.SubElement(p_element, "ul%s" % tag_len)
                ul1.set("text_val", line[tag_len + 1:])
                ul1.set("indent", " " * (tag_len + 1) + "-")
                ul_parent_element, tag_dict["pu%s" % tag_len] = ul1, ul1
                tag_dict["ul%s" % tag_len] += 1
            else:
                update_value = ul_parent_element.get("text_val") + '\n' + '    ' + line
                ul_parent_element.set("text_val", update_value)

    except Exception as e:
        print("Error: %s." % (str(e)))


def load_data():
    try:
        for elt in root.iter():
            if elt is not root:
                if elt.tag.startswith("h"):
                    processedLines.append("%s %s" % (elt.get("index"), elt.get("text_val")))
                else:
                    elt.set("indent", elt.get("indent").replace("-", "+" if len(elt) else "-" ))
                    processedLines.append("%s %s" % (elt.get("indent", "-"), elt.get("text_val")))

    except Exception as e:
        print("Error: %s." % (str(e)))

    for line in processedLines:
        print(line)


if __name__ == "__main__":
    transform_data()
    load_data()

