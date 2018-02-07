#!/usr/bin/python3
"""
This program uploads NCBI GeneRIFs to the BAR Database
Author: Asher
Date: January, 2018
Usage: Add passwords and run: Python3 Upload_geneRIFs.py
"""
import re
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


def ncbi_lookup_dictionary():
    """
    TAIR has a lookup file for AGI to NCBI gene conversion.
    We get NCBI gene IDs from this lookup file
    :return: dictionary of NCBI lookups
    """
    lookup = dict()

    lookup_file = 'TAIR10_NCBI_REFSEQ_mapping_PROT'

    try:
        fh = open(lookup_file, 'r')
    except FileNotFoundError:
        print('Lookup file is not found')
        exit(-1)

    for line in fh:
        columns = line.split("\t")

        ncbi = columns[0].rstrip()
        tair = columns[2].rstrip()

        # Remove variants such as .1
        try:
            agi = re.search('(AT[12345CM]G\d+)', tair, re.IGNORECASE).group(1)
        except AttributeError:
            print('RegEx problem')
            exit(-1)

        lookup[ncbi] = agi

    fh.close()
    return lookup


def main():
    """
    The main program

    :return: boolean 0 or 1
    """
    # Variables
    # So, this file only has generifs for Arabidopsis
    descFile = 'arabidopsis_generifs.csv'  # GFF3 file


    # Get lookups
    lookup = ncbi_lookup_dictionary()

    # Read GFF3 Data
    try:
        descfh = open(descFile, 'r')
    except FileNotFoundError:
        print('Gene RIFs file is not found.')
        exit(-1)

    # Get the connection
    conn = connect()
    cursor = conn.cursor()

    for line in descfh:
        line = line.rstrip()

        # Split the columns
        columns = line.split('\t')

        # If it is not Arabidopsis, next
        if columns[0] != '3702':
            continue

        # Check if the gene has a geneRIF
        if columns[1] in lookup:
            agi = lookup[columns[1]]
        else:
            continue

        # Ok, it does
        pubmed_id = columns[2]
        RIF = columns[4]

        # Now insert into database
        try:
            sql = "INSERT INTO geneRIFs (gene, pubmed, RIF) VALUES (%s, %s, %s)"
            cursor.execute(sql, (
                    agi, pubmed_id, RIF
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
    return 0


if __name__ == '__main__':
    main()
