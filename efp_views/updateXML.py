#!/usr/bin/python3
"""
This program updates the XML file and add IDs
Author: Asher
Date: May, 2017
Usage: python3 updateXML.py
"""
import sys
import xml.etree.ElementTree as ET


def main():
	"""
	The main program for rewriting XML file

	:return: 0 or 1, 0 for success
	"""

	# Using Poplar data as a example
	old_xml = "Populus_trichocarpa.xml"
	new_xml = "Populus_trichocarpa_new.xml"	# Rename this when copying to ePlant

	try:
		tree = ET.parse(old_xml)
		root = tree.getroot()
	except:
		print("Failed to parse the XML file.")
		return 1

	# Add and id to tissue key, which will be used by ePlant to color SVG file.
	# The ID here should match ID in SVG file
	for tissue in root.iter('tissue'):
		name = tissue.get('name')
		name = name.replace(' ', '_')
		tissue.set('id', name)
		
	tree.write(new_xml)

	return 0


if __name__ == '__main__':
	main()
