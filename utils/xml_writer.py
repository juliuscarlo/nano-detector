import xml.etree.cElementTree as ET


def create_tree(object_list, filename="filename.pic", date="14.02.1999"):
    root = ET.Element("xs:schema", {"targetNamespace": "http://www.fernuni-hagen.de/gmaf",
                                    "elementFormDefault": "qualified", "xmlns": "gmaf_schema.xsd",
                                    "xmlns:xs": "http://www.w3.org/2001/XMLSchema"})

    gmaf_data = ET.SubElement(root, "xs:gmaf-data")

    ET.SubElement(gmaf_data, "xs:file").text = filename
    ET.SubElement(gmaf_data, "xs:date").text = date
    objects = ET.SubElement(gmaf_data, "xs:objects")

    for item in object_list:
        object = ET.SubElement(objects, "xs:object")

        ET.SubElement(object, "xs:term").text = item["term"]
        bounding_box = ET.SubElement(object, "xs:bounding-box")

        ET.SubElement(bounding_box, "xs:x").text = str(item["x"])
        ET.SubElement(bounding_box, "xs:y").text = str(item["y"])
        ET.SubElement(bounding_box, "xs:width").text = str(item["width"])
        ET.SubElement(bounding_box, "xs:height").text = str(item["height"])

        ET.SubElement(object, "xs:probability").text = str(item["probability"])

    tree = ET.ElementTree(root)
    return tree


def convert_box_dimensions(relative_coordinates):
    """ Calculates absolute from relative coordinates for the xml schema. """
    
    return absolute_coordinates


def write():
    tree.write("data/out/xml/annotations.xml",
               encoding='utf-8', xml_declaration=True)


tree = create_tree(object_list=[
                   {"term": "cat", "x": 231, "y": 132, "width": 300, "height": 178, "probability": 0.93}])
write()
