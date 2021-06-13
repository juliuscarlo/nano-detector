import xml.etree.cElementTree as ET


def create_tree(object_list):
    root = ET.Element("xs:schema", {"targetNamespace": "http://www.fernuni-hagen.de/gmaf",
                                    "elementFormDefault": "qualified", "xmlns": "gmaf_schema.xsd",
                                    "xmlns:xs": "http://www.w3.org/2001/XMLSchema"})

    gmaf_data = ET.SubElement(root, "xs:gmaf-data")

    ET.SubElement(gmaf_data, "xs:file").text = "filename.pic"
    ET.SubElement(gmaf_data, "xs:date").text = "14.02.1999"
    objects = ET.SubElement(gmaf_data, "xs:objects")

    for item in object_list:
        object = ET.SubElement(objects, "xs:object")

        ET.SubElement(object, "xs:term").text = item["term"]
        bounding_box = ET.SubElement(object, "xs:bounding-box")

        ET.SubElement(bounding_box, "xs:x").text = item["x"]
        ET.SubElement(bounding_box, "xs:y").text = item["y"]
        ET.SubElement(bounding_box, "xs:width").text = item["width"]
        ET.SubElement(bounding_box, "xs:height").text = item["height"]

        ET.SubElement(object, "xs:probability").text = "0.87"

    tree = ET.ElementTree(root)
    return tree


def write():
    tree.write("data/out/xml/annotations.xml",
               encoding='utf-8', xml_declaration=True)


tree = create_tree(object_list="axy")
write()
