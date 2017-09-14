#!/usr/bin/python3
"""
This program uploads lookup data.
Author: Asher
Date: September, 2017
Usage: Python3 uploadLookup.py
"""

import sys
import MySQLdb

def connect():
	"""
	Connect to the database

	:returns conn: A connection to the database
	"""

	try:
		# Connect to BAR MySQL
		conn = MySQLdb.connect(host='', user='', passwd='', db='')
	except MySQLdb.Error:
		print('Can not connect to database!')
		raise
		sys.exit(1)

	return conn

def main():
	"""
	The main program for uploading expression data

	:return: 0 or 1, 0 for success
	"""

	# Variables
	lookupFile = ''

	# Read the expression data file
	try:
		lookupfh = open(lookupFile, 'r')
	except:
		print('An error has occured: ', sys.exc_info()[0])
		raise
		sys.exit(1)

	# Get the connection
	conn = connect()
	cursor = conn.cursor()

	for line in lookupfh:
		line = line.rstrip()
		line = line.rstrip("\n\n")

		lineData = line.split(" ")

		# Skip comments
		if lineData[0][0] == "#":
			continue

		# Skip the header, we don't need it
		if lineData[0][0] == "Probe_set":
			continue

		# Skip the ones with no ID
		if len(lineData) <= 1:
			continue

		# Skip no probeset
		if lineData[1] == "":
			continue

		# Skip na
		if lineData[1] == "na":
			continue

		# Now upload to database
		try:
			sql = "INSERT INTO maize_lookup_v4(probeset, gene_id) VALUES (%s, %s)"
			cursor.execute(sql, (lineData[0], lineData[1]))
		except:
			print("Failed to inserted data into MySQL!")
			raise
			conn.rollback()
			sys.exit(1)

	try:
		conn.commit()
	except:
		print("Commit to database failed!")
		conn.rollback()
		sys.exit(1)

	conn.close()
	lookupfh.close()

	print("Uploaded lookup. Don't forget to index databases!")
	return 0

if __name__ == '__main__':
	main()

