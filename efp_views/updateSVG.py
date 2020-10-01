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
		input_file = open('Populus_trichocarpa.svg', 'r')
		output_file = open('Populus_trichocarpa_new.svg', 'w')
	except FileNotFoundError:
		print("Counldn't open files!")
		raise
	
	for line in input_file:
		# Fix group ids
		if "<g id=" in line:
			match_obj = re.match(r'\s+<g id="\S+"', line, flags=re.IGNORECASE)
			if match_obj:
				output_file.write(match_obj.group(0) + ">\n")

				continue # So we don't pring the line twice

		# Delete old path styles
		if "<path id=" in line:
			line = re.sub(r' fill.+\/', '/', line, flags=re.IGNORECASE)

		# Fix paths
		if "<path id=" in line:
			line = re.sub(r'<path id="\S+"', '<path fill="none" stroke="#000000" stroke-width="0.5" stroke-miterlimit="10"', line, flags=re.IGNORECASE)
		output_file.write(line)
	
	input_file.close()
	output_file.close()


if __name__ == '__main__':
	main()
