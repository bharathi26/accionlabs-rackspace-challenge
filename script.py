#!/usr/bin/env python
#/***********************************************************************/
# * description        :   This python module is used for parses text file and produces formatted output text file
# * author             :   Bharathi Kannan D
# * email              :   bharathi26.kannan@gmail.com
# * lib dependencies   :   pip install lxml 
#/***********************************************************************/
import sys
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

root = etree.Element("html")
root.set('version', '1.0.1')
processedLines = []

def transform_data():
    my_list = [line.strip() for line in sys.stdin if len(line.strip()) != 0]
    # with open(inFile, 'r') as f:
    #     my_list = [line.strip() for line in f if len(line.strip()) != 0]

    # start transforming the data
    h1_count, h2_count, h3_count, h4_count, ul_count = (1,0,0,0,0)
    parent_element = None
    try:
        for x in my_list:
            if x.startswith("* "):
                h2_count = 1
                h1 = etree.SubElement(root, "h1")
                h1.set("text_val", x[2:])
                h1.set("index", str(h1_count))
                parent_element = h1
                h1_count += 1
            elif x.startswith("** "):
                h3_count = 1
                h2 = etree.SubElement(h1, "h2")
                parent_element = h2
                h2.set("text_val", x[3:])
                h2.set("index", "%s.%s" %(h1.get("index"), str(h2_count)))
                h2_count += 1
            elif x.startswith("*** "):
                h4_count = 1
                h3 = etree.SubElement(h2, "h3")
                h3.set("text_val", x[4:])
                h3.set("index", "%s.%s" % (h2.get("index"), str(h3_count)))
                parent_element = h3
                h3_count += 1
            elif x.startswith("**** "):
                h4 = etree.SubElement(h3, "h4")
                h4.set("text_val", x[5:])
                h4.set("index", "%s.%s" % (h3.get("index"), str(h4_count)))
                parent_element = h4
                h4_count += 1
            elif x.startswith(". "):
                ul1 = etree.SubElement(parent_element, "ul1")
                ul1.set("text_val", x[2:])
                ul1.set("index", str(ul_count))
                ul1.set("indent", "  -")
                ul_parent_element = ul1
                ul_count += 1
            elif x.startswith(".. "):
                ul1.set("indent", "  +")
                ul2 = etree.SubElement(ul1, "ul2")
                ul2.set("text_val", x[3:])
                ul2.set("index", str(ul_count))
                ul2.set("indent", "   -")
                ul_parent_element = ul2
                ul_count += 1
            elif x.startswith("... "):
                ul2.set("indent", "   +")
                ul3 = etree.SubElement(ul2, "ul3")
                ul3.set("text_val", x[4:])
                ul3.set("index", str(ul_count))
                ul3.set("indent", "    -")
                ul_parent_element = ul3
                ul_count += 1
            else:
                update_value = ul_parent_element.get("text_val")+'\n'+'    '+x
                ul_parent_element.set("text_val",update_value)

    except Exception as e:
        print("Error: %s." % (str(e)))


def load_data():
    try:
        for elt in root.iter():
            if elt is not root:
                if elt.tag in ["h1", "h2", "h3", "h4"]:
                    processedLines.append("%s %s" % (elt.get("index"), elt.get("text_val")))
                else:
                    processedLines.append("%s %s" % (elt.get("indent", "-"), elt.get("text_val")))
    except Exception as e:
        print("Error: %s." % (str(e)))

    for line in processedLines:
        print(line)


if __name__ == "__main__":
    transform_data()
    load_data()

