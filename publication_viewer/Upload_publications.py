#!/usr/bin/python3
"""
This program uploads NCBI geneRIFs to the BAR Database
Author: Asher
Date: January, 2018
Usage: Add passwords and run: Python3 Upload_publications.py
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
        conn = MySQLdb.connect(host='', user='', passwd='', db='', charset='utf8')
    except MySQLdb.Error:
        print('Can not connect to database!')
        exit(1)

    return conn


def main():
    """
    The main function to upload data to BAR database
    :return:
    """

    try:
        pubmed_file = open('pubmed_dump.tsv', 'r')
    except FileNotFoundError:
        print('Pubmed dump file is not found.')
        exit(-1)

    conn = connect()
    cursor = conn.cursor()

    sql = "INSERT INTO publications (gene, author, year, journal, title, pubmed) VALUES (%s, %s, %s, %s, %s, %s)"

    for line in pubmed_file:
        line = line.rstrip()
        columns = line.split('\t')

        try:
            cursor.execute(sql, (
                columns[0], columns[1], str(columns[2]), columns[3], columns[4], str(columns[5]))
            )
        except MySQLdb.Error as e:
            print("Error inserting data into database " + line + ". Error:" + str(e.args[0]) + ", " + str(e.args[1]))
            conn.rollback()
            conn.close()
            pubmed_file.close()
            exit(-1)

    conn.commit()
    conn.close()
    pubmed_file.close()
    return 0


if __name__ == '__main__':
    main()
