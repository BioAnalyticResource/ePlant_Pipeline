#!/usr/bin/python3
"""
This program creates an XML file, given an SVG file.
Use this program if the ID in SVG matches data_bod_id's in database.
Author: Asher
Date: September, 2017
Usage: python3 createXML.py
"""

import sys
import re
import xml.etree.ElementTree as ET

from xml.dom import minidom

def getSamples():
    """
    Get the names of all the sample.
    Note that this script is only used if data_bod_id == id in svg

    :return: list of ids
    """
    
    ids = []

    try:
        svgFile = open('', 'r')
    except:
        print("Couldn't open file!")
        raise
        sys.exit(1)

    for line in svgFile:
        # Get ID
        if "<g id=" in line:
            matchObj = re.match(r'\s*<g id="(\S+)"', line, flags=re.IGNORECASE)
            if matchObj:
                ids.append(matchObj.group(1))
                continue

    svgFile.close()
    return ids

def getXML(ids):
    """
    This function returns the XML root, given a list of IDs

    :return: XML root
    """
    
    # Variables
    species = 'Poplar'
    
    xmlClass = 'View_leaf'
    db = 'poplar_leaf'
    img = 'poplar_leaf.svg'
    name = 'all'
    
    groupName = 'leaf'
    
    controlSample = 'Med_CTRL'

    colorKey = "#ffffff"

    # Add root
    root = ET.Element('specimen')
    root.set('name', species)

    # Add sub elements
    view = ET.SubElement(root, 'view', {'class':xmlClass, 'db': db, 'img': img, 'name': name})
    group = ET.SubElement(view, 'group', {'name': groupName})
    control = ET.SubElement(group, 'control', {'sample': controlSample})

    # Add IDs
    for Id in ids:
        tissue = ET.SubElement(group, 'tissue', {'colorKey': colorKey, 'id': Id, 'name': Id})
        ET.SubElement(tissue, 'sample', {'name': Id})

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

    roughString = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(roughString)
    return reparsed.toprettyxml(indent="\t")

def main():
    """
    The main program for write XML file

    :return: 0 or 1, 0 for success
    """

    outFile = open('output.xml', 'w')

    # List of Sample IDs.
    ids = getSamples()
    root = getXML(ids)


    outFile.write(prettify(root))
    outFile.write("\n")
    outFile.close()

    return 0


if __name__ == '__main__':
    main()

