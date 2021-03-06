"""Module to write information about objects in an image to an XML file.

Creates an element tree from specified object information, which can be used to generate
a corresponding XML file.

Author: Julius Nick (julius.nick@gmail.com)

"""

import xml.etree.cElementTree as etree


def create_tree(img_shape, object_list, filename, date):
    """Creates an element tree structure, which can easily be exported to an XML
    file.

    Args:
        img_shape: the shape of the image (resolution)
        object_list: the list of detected objects
        filename: the filename of the image
        date: the date on which the image is annotated (current date)
    """
    root = etree.Element("gmaf-collection", {"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                                             "xsi:noNamespaceSchemaLocation": "gmaf_schema.xsd"})

    gmaf_data = etree.SubElement(root, "gmaf-data")

    etree.SubElement(gmaf_data, "file").text = filename
    etree.SubElement(gmaf_data, "date").text = date
    objects = etree.SubElement(gmaf_data, "objects")

    for item in object_list:
        object = etree.SubElement(objects, "object")

        etree.SubElement(object, "term").text = item["term"]
        bounding_box = etree.SubElement(object, "bounding-box")

        box = convert_box(img_shape, relative_box=item["loc"])

        etree.SubElement(bounding_box, "x").text = str(box[0])
        etree.SubElement(bounding_box, "y").text = str(box[1])
        etree.SubElement(bounding_box, "width").text = str(box[2])
        etree.SubElement(bounding_box, "height").text = str(box[3])

        etree.SubElement(object, "probability").text = str(
            item["probability"])

    tree = etree.ElementTree(root)
    return tree


def convert_box(img_shape, relative_box):
    """Calculates absolute from relative coordinates of a bounding box for the
    xml schema. Returns the absolute bounding box values.

    Args:
        img_shape: the shape of the image (resolution)
        relative_box: relative bounding box
    """
    h = img_shape[0]
    w = img_shape[1]
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
    """ Writes an element tree structure to an XML file.
    Args:
        tree: the element tree
        path: the path where the XML file is saved
    """
    tree.write(path, encoding='utf-8', xml_declaration=True)
