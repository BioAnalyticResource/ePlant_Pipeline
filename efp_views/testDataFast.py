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
        dbFile = f.readlines()

    with open(sys.argv[2]) as f:
        rpkmFile = f.readlines()

    start = 0

    # No way to avoid a nested loop?
    for dbLine in dbFile:
        found = 0
        dbLine = dbLine.rstrip()
        dbLineData = dbLine.split("\t")

        for index in range(start, len(rpkmFile)):
            rpkmLine = rpkmFile[index]
            rpkmLine = rpkmLine.rstrip()
            rpkmLineData = rpkmLine.split("\t")

            # A hit
            if dbLineData[0] == rpkmLineData[0]:
                if math.isclose(float(rpkmLineData[1]), float(dbLineData[1]), rel_tol=0.001):
                    print(dbLineData[0], rpkmLineData[0], dbLineData[1], rpkmLineData[1], "Ok")
                else:
                    print(dbLineData[0], rpkmLineData[0], dbLineData[1], rpkmLineData[1], "Not Ok")
                found = 1
                start = index
                continue
            
        if not found:   
            print(dbLineData[0], None, dbLineData[1])
            if dbLineData[1] != '0':
                print('Something wrong with', dbLineData[0])

if __name__ == '__main__':
    main()
