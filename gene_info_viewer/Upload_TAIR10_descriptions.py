#!/usr/bin/python3
"""
This program uploads TAIR10 descriptions to the BAR database
Author: Asher
Date: January, 2018
Usage: Add passwords an run: Python3 Upload_TAIR10_descriptions.py
"""
from sys import exit
import MySQLdb


def connect():
    """
    Connect to database
    :return: connection to database
    """
    try:
        # Connect to database and get a cursor
        conn = MySQLdb.connect(host='', user='', passwd='', db='', charset='utf8')
    except MySQLdb.Error:
        print('Can not connect to database!')
        sys.exit(1)

    return conn

def main():
    """
    The main program

    :return: boolean 0 or 1
    """
    # Variables
    descFile = 'Araport11_functional_descriptions_20171231.txt'  # GFF3 file

    # Read GFF3 Data
    try:
        descfh = open(descFile, 'r')
    except FileNotFoundError:
        print('File not found.!')
        exit(-1)

    # Get the connection
    conn = connect()
    cursor = conn.cursor()

    for line in descfh:
        # Split the remaining lines for database table
        line = line.replace('"', '')
        columns = line.split("\t")

        model_name = columns[0].rstrip()
        type = columns[1].rstrip()

        if 'name' in columns[0]:
            continue

        if columns[2].rstrip() == "":
            short_description = None
        else:
            short_description = columns[2].rstrip()

        if columns[3].rstrip() == "":
            curator_summary = None
        else:
            curator_summary = columns[3].rstrip()

        if columns[4].rstrip() == "":
            computational_description = None
        else:
            computational_description = columns[4].rstrip()

        # Now insert into database
        try:
            sql = "INSERT INTO TAIR10_functional_descriptions (Model_name, Type, Short_description, Curator_summary, Computational_description) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (
                    model_name, type, short_description, curator_summary, computational_description
                )
            )
        except MySQLdb.Error as e:
            print("Error inserting data into database. Error:" + str(e.args[0]) + ", " + str(e.args[1]))
            conn.rollback()
            conn.close()
            descfh.close()
            return 1

    try:
        conn.commit()
    except MySQLdb.Error:
        print("Commit to database failed!")
        conn.rollback()
        conn.close()
        descfh.close()
        return 1

    conn.close()
    descfh.close()
    return 0


if __name__ == '__main__':
    main()
