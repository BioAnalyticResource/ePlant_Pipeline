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
    gff3_file = 'Spurpurea_289_v1.0.gene_exons.gff3'  # GFF3 file
    comment_line_reg_ex = re.compile('^#')  # Comments
    parent_reg_ex = re.compile('Parent=(.*?);')  # Parent column
    id_reg_ex = re.compile('ID=(.*?);')  # ID column
    name_reg_ex = re.compile('Name=(.*?);')  # Name

    # Read GFF3 Data
    try:
        gff3fh = open(gff3_file, 'r')
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
        match_comment = comment_line_reg_ex.match(line)
        if match_comment:
            # Comment is found. move the next line
            continue

        # Split the remaining lines for database table
        columns = line.split("\t")

        # Skip the scaffolds
        if 'Scaffold' in columns[0]:
            continue

        # Get ID
        match_id = id_reg_ex.search(columns[8])
        if match_id:
            gene_id = match_id.group(1)
        else:
            gene_id = ""
            print("Warning: No ID!")

        # Get Parent
        match_parent = parent_reg_ex.search(columns[8])
        if match_parent:
            parent = match_parent.group(1)
        else:
            if gene_id != "":
                parent = gene_id
            else:
                print("Warning: No parrent!")

        # Get name
        gene_name = None
        match_name = name_reg_ex.search(columns[8])
        if match_name:
            gene_name = match_name.group(1)

        # Replace '.' by NULL
        if columns[5] == ".":
            columns[5] = None

        if columns[7] == ".":
            columns[7] = None

        if gene_name is not None:
            gene_name = re.sub(r'.v1.0', '', gene_name)

        if gene_id is not None:
            gene_id = re.sub(r'.v1.0', '', gene_id)

        if parent is not None:
            parent = re.sub(r'.v1.0', '', parent)

        # Now insert into database
        sql = "INSERT INTO gff3 (SeqID, Source, Type, Start, End, Score, Strand, Phase, Id, gene_id, Parent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql, (
                columns[0], columns[1], columns[2], columns[3], columns[4], columns[5], columns[6], columns[7], gene_name, gene_id, parent)
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
