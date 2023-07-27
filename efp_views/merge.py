#!/usr/bin/python3
"""
This program merges two TSV files based on Gene IDs for eFP Browser
NaNs are filled with 0s
Author: Asher
Date: July, 2023
"""
import pandas as pd


def main():
    # Names of files
    file1 = "data4.tsv"
    file2 = "data5.tsv"
    file3 = "data6.tsv"

    # Load data into Pandas frame
    data1 = pd.read_csv(file1, sep="\t")
    data2 = pd.read_csv(file2, sep="\t")
    data3 = pd.read_csv(file3, sep="\t")

    # Merge the data
    data_m1 = data1.merge(data2, how="outer", on="ID", sort=True)
    data_merged = data_m1.merge(data3, how="outer", on="ID", sort=True)

    # Save the data with NaN
    data_merged.to_csv("data7_NaN.tsv", sep="\t", na_rep="NaN", index=False)

    # Save the data without NaN, fill with 0
    data_merged.fillna(0, inplace=True)
    data_merged.to_csv("data7.tsv", sep="\t", index=False)


main()

if '__name__' == '__main__':
    main()
