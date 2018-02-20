#!/usr/bin/python3
"""
This program uploads a gff3 file into ePlant database as a part of ePlant Pipeline
Author: Asher
Date: January, 2017
Usage: Add passwords to dbConfig.py file and run: Python3 gff3ToDatabase.py
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
        sys.exit(-11)

    return conn


def main():
    """
    The main program for gff3 to database program

    :returns: 0 or 1, 0 for success
    """

    # Variables
    gff3File = 'Spurpurea_289_v1.0.gene_exons.gff3'  # GFF3 file
    commentLineRegEx = re.compile('^#')  # Comments
    parentRegEx = re.compile('Parent=(.*?);')  # Parent column
    idRegEx = re.compile('ID=(.*?);')  # ID column
    nameRegEx = re.compile('Name=(.*?);')  # Name

    # Read GFF3 Data
    try:
        gff3fh = open(gff3File, 'r')
    except FileNotFoundError:
        print('An error has occurred: ', sys.exc_info()[0])
        sys.exit(-1)

    # Get the connection
    conn = connect()
    cursor = conn.cursor()

    for line in gff3fh:
        line = line.rstrip()
        line = line.rstrip("\n\r")

        # GFF3 has comment starting with '#"
        matchComment = commentLineRegEx.match(line)
        if matchComment:
            # Comment is found. move the next line
            continue

        # Split the remaining lines for database table
        columns = line.split("\t")

        # Skip the scaffolds
        if 'Scaffold' in columns[0]:
            continue

        # Get ID
        matchId = idRegEx.search(columns[8])
        if matchId:
            geneId = matchId.group(1)
        else:
            geneId = ""
            print("Warning: No ID!")

        # Get Parent
        matchParent = parentRegEx.search(columns[8])
        if matchParent:
            parent = matchParent.group(1)
        else:
            if geneId != "":
                parent = geneId
            else:
                print("Warning: No parrent!")

        # Get name
        geneName = None
        matchName = nameRegEx.search(columns[8])
        if matchName:
            geneName = matchName.group(1)

        # Replace '.' by NULL
        if columns[5] == ".":
            columns[5] = None

        if columns[7] == ".":
            columns[7] = None

        if geneName is not None:
            geneName = re.sub(r'.v1.0', '', geneName)

        if geneId is not None:
            geneId = re.sub(r'.v1.0', '', geneId)

        if parent is not None:
            parent = re.sub(r'.v1.0', '', parent)

        # Now insert into database
        sql = "INSERT INTO gff3 (SeqID, Source, Type, Start, End, Score, Strand, Phase, Id, geneId, Parent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql, (
                columns[0], columns[1], columns[2], columns[3], columns[4], columns[5], columns[6], columns[7], geneName, geneId, parent)
            )
        except MySQLdb.Error as e:
            print("Error inserting data into database: Error: " + str(e.args[0]) + ": " + e.args[1])
            conn.rollback()
            conn.close()
            gff3fh.close()
            sys.exit(-1)

    try:
        conn.commit()
    except MySQLdb.Error:
        print("Commit to database failed!")
        conn.rollback()
        conn.close()
        gff3fh.close()
        sys.exit(-1)

    conn.close()
    gff3fh.close()
    sys.exit(-1)


if __name__ == '__main__':
    main()
