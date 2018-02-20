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
        sys.exit(-1)

    return conn


def main():
    """
    The main program for annotations to database program

    :returns: 0 or 1, 0 for success
    """

    # Variables
    annotationsFile = 'Spurpurea_289_v1.0.defline.txt'  # Annotations File
    commentLineRegEx = re.compile('^#')  # Comments

    # Read Annotations Data
    try:
        annotationsfh = open(annotationsFile, 'r')
    except FileNotFoundError:
        print('An error has occurred: ', sys.exc_info()[0])
        sys.exit(-1)

    # Get the connection
    conn = connect()
    cursor = conn.cursor()

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
        sql = "INSERT INTO gene_annotation (gene, annotation) VALUES (%s, %s)"
        try:
            cursor.execute(sql, (columns[0], columns[2]))
        except MySQLdb.Error as e:
            print("Error inserting data into database: Error: " + str(e.args[0]) + ": " + e.args[1])
            conn.rollback()
            conn.close()
            annotationsfh.close()
            sys.exit(-1)

    try:
        conn.commit()
    except MySQLdb.Error:
        print("Commit to database failed!")
        annotationsfh.close()
        conn.rollback()
        conn.close()
        sys.exit(-1)

    conn.close()
    annotationsfh.close()
    return 0


if __name__ == '__main__':
    main()
