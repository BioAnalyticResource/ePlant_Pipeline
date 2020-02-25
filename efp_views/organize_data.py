#!/usr/bin/python3
# This program formats data provided in columns into a table for upload
# Copy list of sample in the header.txt before running
# Author: Asher
# Date: February 24, 2020
# Usage: python3 organize_data.py


def sample_list_header(sample_list):
    """
    This function reads the sample list
    :param sample_list:
    :return: List of sample_ids
    """

    line_data = []

    try:
        listfh = open(sample_list, 'r')
    except FileNotFoundError:
        print('File is not found')
        exit(-1)

    for line in listfh:
        line = line.rstrip()
        line = line.rstrip("\n\r")
        line_data.append(line)

    listfh.close()

    return line_data


def main():
    """
    This is the main program

    :return:
    """

    expression_file = ''
    sample_list = 'header.txt'
    data_set = {}
    current_sample = ''
    sample_num = 0

    # Get the list of samples
    data_set['ID'] = sample_list_header(sample_list)

    # Now read the big table
    try:
        datafh = open(expression_file, 'r')
    except FileNotFoundError:
        print('File not found!')
        exit(-1)

    for line in datafh:
        line = line.rstrip()
        line = line.rstrip("\n\r")

        line_data = line.split("\t")

        # Skip header
        if line_data[0] == 'Tissue':
            continue

        if line_data[1] in data_set.keys():
            pass
        else:
            # Fist gene ID
            data_set[line_data[1]] = []

        current_sample = line_data[0]
        current_sample = 0
        # Sample check
        if current_sample == line_data[0] and sample_list[sample_num] == current_sample:
            # Everything okay
            data_set[line_data[1]].append(line_data[2])
        else:
            current_sample = line_data[0]
            sample_num += 1
            data_set[line_data[1]].append(line_data[2])

    datafh.close()

    # Output file is the table to be loaded!
    outfh = open('output.tsv', 'w')
    for k, v in data_set.items():
        outfh.write(k)
        for x in v:
            outfh.write("\t" + x)
        outfh.write("\n")
    outfh.close()


if __name__ == '__main__':
    main()
