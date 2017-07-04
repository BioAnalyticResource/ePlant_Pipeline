#!/usr/bin/python3
"""
This program updates SVG files. This is done manually. 
If you find a good SVG parser, drop us a line.
Author: Asher
Date: May, 2017
Usage: python3 updateSVG.py
"""

import re

def main():
	"""
	The main program
	
	:return 0 or 1 for success or fail
	"""

	# Open files
	try:
		inputFile = open('Populus_trichocarpa.svg', 'r')
		outputFile = open('Populus_trichocarpa_new.svg', 'w')
	except:
		print("Counldn't open files!")
		raise
	
	for line in inputFile:
		# Fix group ids
		if "<g id=" in line:
			matchObj = re.match(r'\s+<g id="\S+"', line, flags=re.IGNORECASE)
			if matchObj:
				outputFile.write(matchObj.group(0) + ">\n")

				continue	# So we don't pring the line twice

		# Delete old path styles
		if "<path id=" in line:
			line = re.sub(r' fill.+\/', '/', line, flags=re.IGNORECASE)

		# Fix paths
		if "<path id=" in line:
			line = re.sub(r'<path id="\S+"', '<path fill="none" stroke="#000000" stroke-width="0.5" stroke-miterlimit="10"', line, flags=re.IGNORECASE)
		outputFile.write(line)
	
	inputFile.close()
	outputFile.close()

if __name__ == '__main__':
	main()
