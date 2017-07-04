#!/usr/bin/python3
"""
This program uploads a gff3 file into ePlant database as a part of ePlant Pipeline
Author: Asher
Date: January, 2017
Usage: Add passwords and run: Python3 gff3ToDatabase.py
Data Source: ftp://ftp.ensemblgenomes.org/pub/plants/release-22/gff3/zea_mays
"""
import sys
import re
import MySQLdb
import warnings

def connect():
    """
    Connect to the database

    :returns conn: A connections
    """

    # Supress MySQL Warnings
    warnings.filterwarnings("ignore", category = MySQLdb.Warning)

    try:
        # Connect to database and get a cursor
        conn = MySQLdb.connect(host='', user='', passwd='', db='')
        cur = conn.cursor()
    except MySQLdb.Error:
        print('Can not connect to database!')
        sys.exit(1)

    return conn

def main():
    """
    The main program for gff3 to database program

    :returns: 0 or 1, 0 for success
    """

    # Variables
    gff3File = 'Zea_mays.AGPv3.22.gff3'     # GFF3 file # This is the filed used for Maize GFF3 data!
    commentLineRegEx = re.compile('^#')     # Comments
    parentRegEx = re.compile('Parent=.*?:(.*?);') # Parent column
    idRegEx = re.compile('ID=.*?:(.*?);') # ID column
    nameRegEx = re.compile('Name=(.*?);')   # Name
    repeatRegEx = re.compile('repeat_region')

    # Read GFF3 Data
    try:
        gff3fh = open(gff3File, 'r')
    except:
        print('An error has occured: ', sys.exc_info()[0])
        raise
        sys.exit(1)

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

        # Skip "repeat_region" in maize
        matchId = repeatRegEx.search(columns[2])
        if matchId:
            continue

        # Get ID
        matchId = idRegEx.search(columns[8])
        if matchId:
            geneId = matchId.group(1)
        else:
            geneId = ""
            #print("Warning: No ID!")

        # Get Parent
        matchParent = parentRegEx.search(columns[8])
        if matchParent:
            parent = matchParent.group(1)
        else:
            if geneId != "":
                parent = geneId
            else:
                pass
                #print("Warning: No parrent!")

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

        if (geneName != None):
            geneName = re.sub(r'_.+$', '', geneName)

        if (geneId != None):
            geneId = re.sub(r'_.+$', '', geneId)

        if (parent != None):
            parent  = re.sub(r'_.+$', '', parent)


        # Now insert into database
        try:
            sql = "INSERT INTO gff3_v3 (SeqID, Source, Type, Start, End, Score, Strand, Phase, Id, geneId, Parent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (columns[0], columns[1], columns[2], columns[3], columns[4], columns[5], columns[6], columns[7], geneName, geneId, parent))
            cursor.execute("SHOW WARNINGS")
            sqlWarnings = cursor.fetchall()
            for i in range(len(sqlWarnings)):
                print("Warning - " +sqlWarnings[i][2])
        except MySQLdb.Error as e:
            print("Error inserting data into database: :" + e.args[0] + " + " + e.args[1])
            conn.rollback()
            return 1

    try:
        conn.commit()
    except:
        print("Commit to database failed!")
        conn.rollback()
        return 1

    conn.close()
    gff3fh.close()
    return 0

if __name__ == '__main__':
    main()
