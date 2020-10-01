#!/usr/bin/python3
"""
This program uploads TAIR10 Gene Aliases to the BAR Database
Author: Asher
Date: January, 2018
Usage: Add passwords an run: Python3 Upload_gene_alias.py
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
        conn = MySQLdb.connect(host='', user='', passwd='', db='')
    except MySQLdb.Error:
        print('Can not connect to database!')
        exit(1)

    return conn


def main():
    """
    The main program

    :return: boolean 0 or 1
    """
    # Variables
    desc_file = 'gene_aliases_20171231.txt'  # GFF3 file

    # Read GFF3 Data
    try:
        descfh = open(desc_file, 'r')
    except FileNotFoundError:
        print('File is not found')
        exit(-1)

    # Get the connection
    conn = connect()
    cursor = conn.cursor()

    for line in descfh:
        line = line.replace('"', '')
        if 'name' in line:
            continue

        # Split the remaining lines for database table
        columns = line.split("\t")

        locus = columns[0].rstrip()

        if columns[1].rstrip() == "":
            symbol = None
        else:
            symbol = columns[1].rstrip()

        if columns[2].rstrip() == "":
            full_name = None
        else:
            full_name = columns[2].rstrip()

        # Now insert into database
        try:
            sql = "INSERT INTO gene_alias (gene, symbol, synonyms) VALUES (%s, %s, %s)"
            cursor.execute(sql, (
                    locus, symbol, full_name
                )
            )
        except MySQLdb.Error as e:
            print("Error inserting data into database " + line + ". Error:" + str(e.args[0]) + ", " + str(e.args[1]))
            conn.rollback()
            conn.close()
            descfh.close()
            exit(-1)

    try:
        conn.commit()
    except MySQLdb.Error:
        print("Commit to database failed!")
        conn.rollback()
        conn.close()
        descfh.close()
        exit(-1)

    conn.close()
    descfh.close()
    exit()


if __name__ == '__main__':
    main()
