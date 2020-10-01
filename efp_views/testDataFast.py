#!/usr/bin/python3
"""
This script tests data from one-liner.
Author: Asher
Date: December 3, 2017
Usage: python3 testData.tsv filefromdb.txt file_rpkm.txt > output.txt
"""

import sys
import math


def main():
    """
    The main program.
    """
    
    with open(sys.argv[1]) as f:
        db_file = f.readlines()

    with open(sys.argv[2]) as f:
        rpkm_file = f.readlines()

    start = 0

    # No way to avoid a nested loop?
    for db_line in db_file:
        found = 0
        db_line = db_line.rstrip()
        db_line_data = db_line.split("\t")

        for index in range(start, len(rpkm_file)):
            rpkm_line = rpkm_file[index]
            rpkm_line = rpkm_line.rstrip()
            rpkm_line_data = rpkm_line.split("\t")

            # A hit
            if db_line_data[0] == rpkm_line_data[0]:
                if math.isclose(float(rpkm_line_data[1]), float(db_line_data[1]), rel_tol=0.001):
                    print(db_line_data[0], rpkm_line_data[0], db_line_data[1], rpkm_line_data[1], "Ok")
                else:
                    print(db_line_data[0], rpkm_line_data[0], db_line_data[1], rpkm_line_data[1], "Not Ok")
                found = 1
                start = index
                continue
            
        if not found:   
            print(db_line_data[0], None, db_line_data[1])
            if db_line_data[1] != '0':
                print('Something wrong with', db_line_data[0])


if __name__ == '__main__':
    main()
