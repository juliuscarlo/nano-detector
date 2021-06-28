import xml.etree.cElementTree as etree


def create_tree(img, object_list, filename="filename.pic", date="14.02.1999"):
    root = etree.Element("xs:schema", {"targetNamespace": "http://www.fernuni-hagen.de/gmaf",
                                       "elementFormDefault": "qualified", "xmlns": "gmaf_schema.xsd",
                                       "xmlns:xs": "http://www.w3.org/2001/XMLSchema"})

    gmaf_data = etree.SubElement(root, "xs:gmaf-data")

    etree.SubElement(gmaf_data, "xs:file").text = filename
    etree.SubElement(gmaf_data, "xs:date").text = date
    objects = etree.SubElement(gmaf_data, "xs:objects")

    for item in object_list:
        object = etree.SubElement(objects, "xs:object")

        etree.SubElement(object, "xs:term").text = item["term"]
        bounding_box = etree.SubElement(object, "xs:bounding-box")

        print(item["loc"])
        box = convert_box(img, relative_box=item["loc"])

        etree.SubElement(bounding_box, "xs:x").text = str(box[0])
        etree.SubElement(bounding_box, "xs:y").text = str(box[1])
        etree.SubElement(bounding_box, "xs:width").text = str(box[2])
        etree.SubElement(bounding_box, "xs:height").text = str(box[3])

        etree.SubElement(object, "xs:probability").text = str(item["probability"])

    tree = etree.ElementTree(root)
    return tree


def convert_box(img, relative_box):
    """ Calculates absolute from relative coordinates of a box for the xml schema. """
    h = img.shape[0]
    w = img.shape[1]
    y_min = int(max(1, (relative_box[0] * h)))
    x_min = int(max(1, (relative_box[1] * w)))
    y_max = int(min(h, (relative_box[2] * h)))
    x_max = int(min(w, (relative_box[3] * w)))

    x = x_min
    y = y_min
    width = x_max - x_min
    height = y_max - y_min

    return x, y, width, height


def write(tree, path):
    tree.write(path,
               encoding='utf-8', xml_declaration=True)

# tree = create_tree(object_list=[
#                    {"term": "cat", "x": 231, "y": 132, "width": 300, "height": 178, "probability": 0.93}])
# write()
