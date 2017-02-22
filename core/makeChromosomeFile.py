#!/usr/bin/python3
"""
This program generated the chromosome file for ePlant
Author: Asher
Date: February, 2017
usage: python3 makeChromosomeFile.py
Notes: This program uses BioPython for Python 3
"""
from Bio import SeqIO
import json

def main():
	"""
	The main program that create a json file for ePlant

	:return: 0 or 1 for sucess or fail
	"""

	fasta_sequences = SeqIO.parse(open("Ptrichocarpa_210_v3.0.fa"), 'fasta')
	chrData = {'species': 'Populus trichocarpa'}
	chrInfo = []

	# Get the sequence lengths
	for fasta in fasta_sequences:
		name, length = fasta.id, len(fasta.seq)
		
		# Lets skip the Scaffolds for now.
		if "scaffold" in name:
			pass
		else:
			chrInfo.append({'id': name, 'name': name, 'size': str(length), 'centromeres': []})

	chrData['chromosomes'] = chrInfo

	# Save the data into output file: Populus_trichocarpa.json
	try:
		fh = open('Populus_trichocarpa.json', 'w')
		json.dump(chrData, fh, indent=4)
		fh.close()
	except:
		print("An error has occurred with trying to save the file.")

if __name__ == '__main__':
	main()
