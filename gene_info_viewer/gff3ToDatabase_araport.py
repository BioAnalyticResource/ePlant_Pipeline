#!/usr/bin/python3
"""
This program uploads a gff3 file into ePlant database as a part of ePlant Pipeline
Author: Asher
Date: January, 2018
Usage: Add passwords an run: Python3 gff3ToDatabase_araport.py
"""
import sys
import re
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
        sys.exit(1)

    return conn


def main():
    """
    The main program

    :return: boolean 0 or 1
    """
    # Variables
    gff3File = 'Araport11_GFF3_genes_transposons.201606.gff'  # GFF3 file
    commentLineRegEx = re.compile('^#')  # Comments
    parentRegEx = re.compile('Parent=(.*?);')  # Parent column
    idRegEx = re.compile('ID=(.*?);')  # ID column
    nameRegEx = re.compile('Name=(.*?);')  # Name

    # Read GFF3 Data
    try:
        gff3fh = open(gff3File, 'r')
    except FileNotFoundError:
        print('An error has occurred: ', sys.exc_info()[0])
        return 1

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
            parent_line = matchParent.group(1)
        else:
            if geneId != "":
                parent_line = geneId
            else:
                print("Warning: No parent!")

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

        # This is for Araport only
        parents = parent_line.split(',')

        # Now insert into database
        for parent in parents:
            try:
                sql = "INSERT INTO araport11_gff3 (SeqID, Source, Type, Start, End, Score, Strand, Phase, Id, geneId, Parent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (
                    columns[0], columns[1], columns[2], columns[3], columns[4], columns[5], columns[6], columns[7],
                    geneName,
                    geneId, parent)
                )
            except MySQLdb.Error as e:
                print("Error inserting data into database: :" + str(e.args[0]) + " + " + str(e.args[1]))
                conn.rollback()
                conn.close()
                gff3fh.close()
                return 1

    try:
        conn.commit()
    except MySQLdb.Error:
        print("Commit to database failed!")
        conn.rollback()
        conn.close()
        gff3fh.close()
        return 1

    conn.close()
    gff3fh.close()
    return 0


if __name__ == '__main__':
    main()
