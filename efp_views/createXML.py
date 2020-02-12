#!/usr/bin/python3
"""
This program creates an XML file, given an SVG file.
Use this program if the ID in SVG matches data_bod_id's in database.
Some manual editing is still required!
Author: Asher
Date: September, 2017
Usage: python3 createXML.py
"""

import sys
import re
import xml.etree.ElementTree as ET

from xml.dom import minidom


def get_tissues():
    """
    This function returns all the tissues per sample

    :return: dictionary of tissues
    """

    tissues = {}

    try:
        # NOTE: Samples file name
        tissues_fh = open('tissues.txt', 'r')
    except FileNotFoundError:
        print('tissues.txt now found!')
        exit(-1)

    for line in tissues_fh:
        line = line.rstrip()
        line = line.strip()

        line_data = line.split("\t")

        if line_data[0] in tissues.keys():
            tissues[line_data[0]].append(line_data[1])
        else:
            tissues[line_data[0]] = []
            tissues[line_data[0]].append(line_data[1])

    tissues_fh.close()

    return tissues


def get_samples():
    """
    Get the names of all the sample.
    Note that this script is only used if data_bod_id == id in svg

    :return: list of ids
    """

    ids = []

    try:
        svg_file = open('sugarcane_culm_optimized.svg', 'r')
    except FileNotFoundError:
        print("Couldn't open file!")
        sys.exit(-1)

    for line in svg_file:
        # Get ID
        if "<g id=" in line:
            match_obj = re.match(r'\s*<g id="(\S+)"', line, flags=re.IGNORECASE)
            if match_obj:
                ids.append(match_obj.group(1))
                continue

    svg_file.close()
    return ids


def get_XML(ids, tissues):
    """
    This function returns the XML root, given a list of IDs

    :return: XML root
    """

    # Variables: NOTE: These need to be changed
    species = 'Poplar'
    xml_class = 'View_leaf'
    db = 'poplar_leaf'
    img = 'poplar_leaf.svg'
    name = 'all'
    group_name = 'leaf'
    control_sample = 'Med_CTRL'

    # Other variables
    color_key = "#ffffff"

    # Add root
    root = ET.Element('specimen')
    root.set('name', species)

    # Add sub elements
    view = ET.SubElement(root, 'view', {'class':xml_class, 'db': db, 'img': img, 'name': name})
    group = ET.SubElement(view, 'group', {'name': group_name})
    control = ET.SubElement(group, 'control', {'sample': control_sample})

    # Add IDs
    for Id in ids:
        # Now add samples
        if Id in tissues.keys():
            tissue = ET.SubElement(group, 'tissue', {'colorKey': color_key, 'id': Id, 'name': Id})

            for replicate in tissues[Id]:
                ET.SubElement(tissue, 'sample', {'name': replicate})

    if root is not None:
        return root
    else:
        print("No document root!")
        sys.exit(1)


def prettify(elem):
    """
    Pretty print XML. Modified from:
    Source: https://pymotw.com/2/xml/etree/ElementTree/create.html

    :return: xml
    """

    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


def main():
    """
    The main program for write XML file

    :return: 0 or 1, 0 for success
    """

    out_file = open('output.xml', 'w')

    # List of Sample IDs.
    ids = get_samples()
    tissues = get_tissues()
    root = get_XML(ids, tissues)

    out_file.write(prettify(root))
    out_file.write("\n")
    out_file.close()

    return 0


if __name__ == '__main__':
    main()

