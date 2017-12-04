#!/usr/bin/python3
"""
This program uploads gene expression data for ePlant and eFP views
Author: Asher
Date: February, 2017
Usage: Change file name, update passwords and run: python3 uploadData.py
"""
import sys
import MySQLdb
import copy
import statistics

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
	The main program for uploading expression data

	:return: 0 or 1, 0 for success
	"""

	# Variables
	expressionFile = ''

	# Read the expression data
	try:
		expfh = open(expressionFile, 'r')
	except:
		print('An error has occured: ', sys.exc_info()[0])
		raise
		return 1

	# Get the connection
	conn = connect()
	cursor = conn.cursor()

	for line in expfh:
		line = line.rstrip()
		line = line.rstrip("\n\r")

		lineData = line.split("\t")

		# Get the header if there is any
		if lineData[0] == 'ID':
			header = copy.deepcopy(lineData)
			continue
		
		sample_id = 1
		proj_id = 1

		# Calculate median, if there is no control
		medCtrl = statistics.median(map(float,lineData[1:len(lineData)]))
		lineData.append(medCtrl)
		header.append("Med_CTRL")

		for i in range(len(lineData)):
			if i == 0:
				continue

			# Upload data to the database			
			try:
				sql = "INSERT INTO sample_data(proj_id, sample_id, data_probeset_id, data_signal, data_bot_id) VALUES (%s, %s, %s, %s, %s)"
				cursor.execute(sql, (str(proj_id), int(sample_id), lineData[0], float(lineData[i]), header[i]))
			except MySQLdb.Error as e:
				print("Error inserting data into database. Error: " + str(e.args[0]) + ": " + str(e.args[1]))
				conn.rollback()
				return 1

			sample_id = sample_id + 1

	try:
		conn.commit()
	except:
		print("Commit to database failed!")
		conn.rollback()
		conn.close()
		expfh.close()
		return 1

	conn.close()
	expfh.close()
	return 0

if __name__ == '__main__':
	main()
