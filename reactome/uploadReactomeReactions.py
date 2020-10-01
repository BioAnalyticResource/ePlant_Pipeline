#!/usr/bin/python3
"""
This program uploads Reactome Pathway lookups
Author: Asher
Date: October, 2017
Usage: python3 uploadReactome.py
"""

import sys
import MySQLdb


def connect():
	"""
	Connect to the database

	:returns conn: A connections
	"""

	try:
		# Connect to database and get a cursor
		conn = MySQLdb.connect(host='', user='', passwd='', db='')
	except MySQLdb.Error:
		print('Can not connect to database!')
		sys.exit(1)
	
	return conn


def main():
	"""
	The main program for uploading the data

	:return: 0 or 1, 1 for success
	"""

	# Variables
	reactome_file = 'Ensembl2PlantReactomeReactions.txt'
	speacies_name = 'Arabidopsis thaliana'

	# Read the Reactome data
	try:
		reactfh = open(reactome_file, 'r')
	except FileNotFoundError:
		print('An error has occurred: ', sys.exec_info()[0])
		raise

	# Get the connection
	conn = connect()
	cursor = conn.cursor()

	for line in reactfh:
		line = line.rstrip()
		line = line.rstrip("\n\r")

		line_data = line.split("\t")

		if line_data[5] != speacies_name:
			continue
		
		if line_data[0] == "" or line_data[1] == "":
			continue

		try:
			sql = "INSERT INTO reactome_reactions(gene_id, reaction_id) VALUES (%s, %s)"
			cursor.execute(sql, (line_data[0], line_data[1]))
		except MySQLdb.Error as e:
			print("Error inserting data into database. Error: " + str(e.args[0]) + ": " + str(e.args[1]))
			conn.rollback()
			return 1

	try:
		conn.commit()
	except MySQLdb.Error:
		print("Commit to database failed!")
		conn.rollback()
		return 1

	conn.close()
	reactfh.close()
	return 0


if __name__ == '__main__':
	main()

