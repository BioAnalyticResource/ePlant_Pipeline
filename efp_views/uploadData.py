#!/usr/bin/python3
"""
This program uploads gene expression data for ePlant and eFP views
Author: Asher
Date: February, 2017
Usage: Change file name, update passwords and run: python3 uploadData.py
"""
from sys import exit
import MySQLdb
import copy
import statistics


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
        exit(-1)

    return conn


def main():
    """
    The main program for uploading expression data

    :return: 0 or -1, 0 for success
    """

    # Variables
    expression_file = ''

    # Read the expression data
    try:
        exp_fh = open(expression_file, 'r')
    except FileNotFoundError:
        print('Gene Expression data file can not be found')
        exit(-1)

    # Get the connection
    conn = connect()
    cursor = conn.cursor()

    for line in exp_fh:
        line = line.rstrip()
        line = line.rstrip("\n\r")

        line_data = line.split("\t")

        # Get the header if there is any
        if line_data[0] == 'ID':
            header = copy.deepcopy(line_data)
            continue

        sample_id = 1
        proj_id = 1

        # Calculate median, if there is no control
        med_ctrl = statistics.median(map(float, line_data[1:len(line_data)]))
        line_data.append(med_ctrl)
        header.append("Med_CTRL")

        sql = "INSERT INTO sample_data(proj_id, sample_id, data_probeset_id, data_signal, data_bot_id) VALUES (%s, %s, %s, %s, %s)"

        for i in range(len(line_data)):
            if i == 0:
                continue

            # Upload data to the database
            try:
                cursor.execute(sql, (str(proj_id), int(sample_id), line_data[0], float(line_data[i]), header[i]))
            except MySQLdb.Error as e:
                print("Error inserting data into database. Error: " + str(e.args[0]) + ": " + str(e.args[1]))
                conn.rollback()
                exit(-1)

            sample_id = sample_id + 1

    try:
        conn.commit()
    except MySQLdb.Error:
        print("Commit to database failed!")
        conn.rollback()
        conn.close()
        exp_fh.close()
        exit(-1)

    conn.close()
    exp_fh.close()
    return 0


if __name__ == '__main__':
    main()
