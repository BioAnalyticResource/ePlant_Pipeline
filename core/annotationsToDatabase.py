#!/usr/bin/python3
"""
This program upload annotations into ePlant database as a part of ePlant Pipeline
Author: Asher
Date: Febuary, 2017
Usage: Add passwords to dbConfig.py file and run: Python3 annotationsToDatabase.py
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
	The main program for annotations to database program
	
	:returns: 0 or 1, 0 for success
	"""

	# Suppress MySQL Warnings
	warnings.filterwarnings("ignore", category = MySQLdb.Warning)

	# Variables
	annotationsFile = 'Ptrichocarpa_210_v3.0.defline.txt'	# Annotations File
	commentLineRegEx = re.compile('^#')	# Comments
	
	# Read Annotations Data
	try:
		annotationsfh = open(annotationsFile, 'r')
	except:
		print('An error has occured: ', sys.exc_info()[0])
		raise
		return 1

	# Get the connection
	conn = connect()
	cursor = conn.cursor();

	for line in annotationsfh:
		line = line.rstrip()
		line = line.rstrip("\n\r")

		# GFF3 has comment starting with '#"
		matchComment = commentLineRegEx.match(line)
		if matchComment:
			# Comment is found. move the next line
			continue	
		
		# Split the remaining lines for database table
		columns = line.split("\t")
		
		# Now insert into database
		try:
			sql = "INSERT INTO gene_annotation (gene, annotation) VALUES (%s, %s)"
			cursor.execute(sql, (columns[0], columns[1]))
			cursor.execute("SHOW WARNINGS")
			sqlWarnings = cursor.fetchall()
			for i in range(len(sqlWarnings)):
				print("Warning - " +sqlWarnings[i][2])
		except MySQLdb.Error as e:
			print("Error inserting data into database:" + e.args[0] + " + " + e.args[1])
			conn.rollback()
			return 1

	try:
		conn.commit()
	except:
		print("Commit to database failed!")
		conn.rollback()
		return 1

	conn.close()
	annotationsfh.close()
	return 0

if __name__ == '__main__':
	main()
	

