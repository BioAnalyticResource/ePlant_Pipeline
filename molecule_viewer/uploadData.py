#!/usr/bin/python3
"""
This program uploads data into the database
Author: Asher
Date: January 2, 2019
Usage: python3 uploadData.py
Notes: databasefile.tsv should be present.
"""
import MySQLdb
from sys import exit


def connect():
    """
    Connect to database
    :return: connection to database
    """
    try:
        # Connect to database and get a cursor
        conn = MySQLdb.connect(host='', user='', passwd='', db='')
    except MySQLdb.Error:
        print('Can not connect to database!')
        exit(1)

    return conn


def main():
    """
    The main program.

    :return:
    """

    conn =  connect()
    cursor = conn.cursor()

    # Open the input data file
    try:
        f = open('databasefile.tsv', 'r')
    except FileNotFoundError:
        print('Input data not found')
        exit(-1)

    for line in f:
        line = line.rstrip()

        # Skip empty lines and header
        if line == "":
            continue

        columns = line.split('\t')

        if columns[0] == 'gene':
            continue

        sql = 'INSERT INTO pdb_predicted_files (gene, template, confidence) VALUES (%s, %s, %s)'

        # Now insert the data into database
        try:
            cursor.execute(sql, (columns[0], columns[1], columns[2]))
        except MySQLdb.Error as e:

            print('Error inserting data ' + line + ' into database: ' + str(e.args[0]) + ", " + e.args[1])
            conn.rollback()
            conn.close()
            f.close()
            exit(-1)

    # Finally Save the data
    try:
        conn.commit()
    except MySQLdb.Error:
        print('Commit to database failed!')
        conn.rollback()
    finally:
        conn.close()
        f.close()


if __name__ == '__main__':
    main()