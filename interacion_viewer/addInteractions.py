#!/usr/bin/python3
"""
This program uploads interactions from excel file.
Author: Asher
Date: October, 2017
Usage: python3 addInteractions.py
"""

import sys
import MySQLdb
import warnings
import re

# Note: Pandas xlrd is much slower.
from openpyxl import load_workbook


def connect():
	"""
	Connect to the database

	:returns conn: A connection
	"""
	
	try:
		conn = MySQLdb.connect(host='', user='', passwd='', db='')
	except MySQLdb.Error:
		print('Can not connect to database!')
		sys.exit(1)
	
	return conn


def formatPubmedID(pubmed):
	"""
	This function formats pubmed IDs, given a pubmed id

	:return: formated pubmed ID.
	"""

	# Check if it is none	
	if pubmed is None:
		return pubmed
	
	pubmed = str(pubmed)
	
	# patterns
	pttrn1 = re.compile(r'^\d+$')
	pttrn2 = re.compile(r'pubmed:\d+$')
	pttrn3 = re.compile(r'|imex:IM-\d+')
	pttrn4 = re.compile(r'ET')	# Not sure what this is

	# Pattern 1
	if pttrn1.match(pubmed):
		return "PubMed" + pubmed

	# Pattern 3
	if pttrn3.match(pubmed):
		pubmed = pttrn3.sub('', pubmed)
	
	# Pattern 2
	if pttrn2.match(pubmed):
		pubmed = pubmed.replace('pubmed:','')
		return "PubMed" + pubmed

	# Pattern 4
	if pttrn4.match(pubmed):
		return None

	return None


def getList(wb):
	"""
	Get the list of all interactions in wb

	:return: Interactions table
	"""

	interactome = {}
	p = re.compile(r'_.*$')

	ws = wb['Master Interactome']
	
	for row in ws.rows:
		# Skip the first row
		if "Maize A" in row[0].value:
			continue

		pubmed = formatPubmedID(row[20].value)	

		# check if Key is already there
		# Then add as: Protein1, Protein12, CV, PCC, Pubmed IDs.
		if row[2].value in interactome:
			if interactome[row[2].value][4] is None and pubmed is not None:
				interactome[row[2].value][4] = pubmed
			elif pubmed is not None:
				if pubmed in interactome[row[2].value][4]:
					# It is already in there
					pass
				else:
					interactome[row[2].value][4] += "\n" + pubmed
			else:
				pass
		else:
			interactome[row[2].value] = [p.sub('', row[0].value), p.sub('', row[1].value), None, None, pubmed]
	
	return interactome	


def getCV(wb, interactome):
	"""
	Get confidence values given interactome in wb

	:return: updated interactome data
	"""

	ws = wb['CV']

	for row in ws.rows:
		if "Protein A" in row[0].value:
			continue

		# Check if Key is already there
		# If there is a CV and PCC, then add it
		if row[4].value in interactome:
			interactome[row[4].value][2] = row[8].value
			interactome[row[4].value][3] = row[9].value

	return interactome


def main():
	"""
	The main program.

	:return: 0 or 1, 0 for success.
	"""
	
	# Variables
	interactions_file = ''

	# Note that read_only is required the speed up the load.
	warnings.simplefilter('ignore')
	wb = load_workbook(filename = interactions_file, read_only=True)
	warnings.simplefilter('default')

	interactome = getList(wb)
	interactome = getCV(wb, interactome)

	conn = connect()
	cursor = conn.cursor()
	sql = "INSERT INTO interactions (Protein1, Protein2, Quality, aiv_index, Pcc, bind_id) VALUES (%s, %s, %s, %s, %s, %s)"

	for k, v in interactome.items():
		try:
			cursor.execute(sql, (v[0], v[1], v[2], 0, v[3], v[4]))
			if v[0] != v[1]:
				cursor.execute(sql, (v[1], v[0], v[2], 1, v[3], v[4]))
		except MySQLdb.Error as e:
			if e.args[0] == 1062:
				print("Duplicate entry: ", k, v[0], v[1], v[2], 1, v[3], v[4])
			else:
				conn.rollback()
				return 1

	try:
		conn.commit()
	except MySQLdb.Error:
		print("Commit to database failed!")
		conn.rollback()
		return 1

	conn.close()
	return 0


if __name__ == '__main__':
	main()

