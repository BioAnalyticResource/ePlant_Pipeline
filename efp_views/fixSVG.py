#!/usr/bin/python3
"""
This program add group tags to svg files, if the don't have <g></g> tags!
Author: Asher
Date: September, 2017
Usage: python3 fixSVG.py
"""

import re


def main():
	"""
	The main program

	:return 0 or 1 for success or fail
	"""

	# Open files
	try:
		input_file = open('', 'r')
		output_file = open('', 'w')
	except FileNotFoundError:
		print("Couldn't open files!")
		raise
	
	for line in input_file:
		# Add grous
		if "<circle id=" in line:
			# Read id
			match_obj = re.match(r'\s+<circle id="(\S+)"', line, flags=re.IGNORECASE)
			if match_obj:
				group_id = match_obj.group(1)
			else:
				print("No id in circle. Adding as is.")
				output_file.write(line)
				continue
			
			# Add group
			output_file.write('<g id="' + group_id + '">' + "\n")
			output_file.write(line)
			output_file.write('</g>' + "\n")
		elif "<ellipse id=" in line:
			# Now for eclipses
			# Read id
			match_obj = re.match(r'\s+<ellipse id="(\S+)"', line, flags=re.IGNORECASE)
			if match_obj:
				group_id = match_obj.group(1)
			else:
				print("No id in circle. Adding as is.")
				output_file.write(line)
				continue
			
			# Add group
			output_file.write('<g id="' + group_id + '">' + "\n")
			output_file.write(line)
			output_file.write('</g>' + "\n")
		else:
			output_file.write(line)

	input_file.close()
	output_file.close()


if __name__ == '__main__':
	main()

