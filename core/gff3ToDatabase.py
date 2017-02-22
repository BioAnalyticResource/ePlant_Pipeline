#!/usr/bin/python3
"""
This program uploads a gff3 file into ePlant database as a part of ePlant Pipeline
Author: Asher
Date: January, 2017
Usage: Add passwords to dbConfig.py file and run: Python3 gff3ToDatabase.py
"""
import sys
import re
import MySQLdb
import warnings

def connect():
	"""
	Connect to the database

	:returns conn: A connections
	"""

	# Supress MySQL Warnings
	warnings.filterwarnings("ignore", category = MySQLdb.Warning)

	try:
		# Connect to database and get a cursor
		conn = MySQLdb.connect(host='', user='', passwd='', db='')
		cur = conn.cursor()
	except MySQLdb.Error:
		print('Can not connect to database!')
		sys.exit(1)
	
	return conn

def main():
	"""
	The main program for gff3 to database program
	
	:returns: 0 or 1, 0 for success
	"""

	# Variables
	gff3File = 'Ptrichocarpa_210_v3.0.gene_exons.gff3'	# GFF3 file
	commentLineRegEx = re.compile('^#')	# Comments
	parentRegEx = re.compile('Parent=(.*?);')	# Parent column
	idRegEx = re.compile('ID=(.*?);')	# ID column
	nameRegEx = re.compile('Name=(.*?);')	# Name

	# Read GFF3 Data
	try:
		gff3fh = open(gff3File, 'r')
	except:
		print('An error has occured: ', sys.exc_info()[0])
		raise
		return 1

	# Get the connection
	conn = connect()
	cursor = conn.cursor();

	for line in gff3fh:
		line = line.rstrip()
		line = line.rstrip("\n\r")

		# GFF3 has comment starting with '#"
		matchComment = commentLineRegEx.match(line)
		if matchComment:
			# Comment is found. move the next line
			continue	
		
		# Split the remaining lines for database table
		columns = line.split("\t")
		
		# Get ID
		matchId = idRegEx.search(columns[8])
		if matchId:
			geneId = matchId.group(1)
		else:
			geneId = ""
			print("Warning: No ID!")
		
		# Get Parent
		matchParent = parentRegEx.search(columns[8])
		if matchParent:
			parent = matchParent.group(1)
		else:
			if geneId != "":
				parent = geneId
			else:
				print("Warning: No parrent!")
		
		# Get name
		geneName = None
		matchName = nameRegEx.search(columns[8])
		if matchName:
			geneName = matchName.group(1)

		# Replace '.' by NULL
		if columns[5] == ".":
			columns[5] = None

		if columns[7] == ".":
			columns[7] = None
		
		if (geneName != None):	
			geneName = re.sub(r'.v3.0', '', geneName)
	
		if (geneId != None):
			geneId = re.sub(r'.v3.0', '', geneId)

		if (parent != None):
			parent  = re.sub(r'.v3.0', '', parent)

		# Now insert into database
		try:
			sql = "INSERT INTO gff3_v3 (SeqID, Source, Type, Start, End, Score, Strand, Phase, Id, geneId, Parent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(sql, (columns[0], columns[1], columns[2], columns[3], columns[4], columns[5], columns[6], columns[7], geneName, geneId, parent))
			cursor.execute("SHOW WARNINGS")
			sqlWarnings = cursor.fetchall()
			for i in range(len(sqlWarnings)):
				print("Warning - " +sqlWarnings[i][2])
		except MySQLdb.Error as e:
			print("Error inserting data into database: :" + e.args[0] + " + " + e.args[1])
			conn.rollback()
			return 1

	try:
		conn.commit()
	except:
		print("Commit to database failed!")
		conn.rollback()
		return 1

	conn.close()
	gff3fh.close()
	return 0

if __name__ == '__main__':
	main()
	

