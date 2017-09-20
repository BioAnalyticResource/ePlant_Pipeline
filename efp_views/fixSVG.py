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
		inputFile = open('', 'r')
		outputFile = open('', 'w')
	except:
		print("Couldn't open files!")
		raise
	
	for line in inputFile:
		# Add grous
		if "<circle id=" in line:
			# Read id
			matchObj = re.match(r'\s+<circle id="(\S+)"', line, flags=re.IGNORECASE)
			if matchObj:
				groupId = matchObj.group(1)
			else:
				print("No id in circle. Adding as is.")
				outputFile.write(line)
				continue
			
			# Add group
			outputFile.write('<g id="' + groupId + '">' + "\n")
			outputFile.write(line)
			outputFile.write('</g>' + "\n")
		elif "<ellipse id=" in line:
			# Now for eclipses
			# Read id
			matchObj = re.match(r'\s+<ellipse id="(\S+)"', line, flags=re.IGNORECASE)
			if matchObj:
				groupId = matchObj.group(1)
			else:
				print("No id in circle. Adding as is.")
				outputFile.write(line)
				continue
			
			# Add group
			outputFile.write('<g id="' + groupId + '">' + "\n")
			outputFile.write(line)
			outputFile.write('</g>' + "\n")
		else:
			outputFile.write(line)

	inputFile.close()
	outputFile.close()

if __name__ == '__main__':
	main()

