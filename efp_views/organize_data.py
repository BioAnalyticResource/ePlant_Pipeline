#!/usr/bin/python3
# This program formats data provided in columns into a table
# Copy list of sample in the header.txt
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
        list_fh = open(sample_list, 'r')
    except FileNotFoundError:
        print('File is not found')
        exit(-1)

    for line in list_fh:
        line = line.rstrip()
        line = line.rstrip("\n\r")
        line_data.append(line)

    list_fh.close()

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
    sample_header = sample_list_header(sample_list)
    data_set['ID'] = sample_header

    # Now read the big table
    try:
        data_fh = open(expression_file, 'r')
    except FileNotFoundError:
        print('File not found!')
        exit(-1)

    for line in data_fh:
        line = line.rstrip()
        line = line.rstrip("\n\r")

        line_data = line.split("\t")

        for i in range(len(line_data)):
            line_data[i] = line_data[i].strip()

        # Skip header
        if line_data[0] == 'Tissue':
            continue

        if line_data[1] in data_set.keys():
            pass
        else:
            # Fist gene ID
            data_set[line_data[1]] = ["NAN"] * len(sample_header)

        current_sample = line_data[0]
        sample_num = 0

        while sample_header[sample_num] != current_sample:
            sample_num += 1

        # Sample check
        if (current_sample == line_data[0]) and (sample_header[sample_num] == current_sample):
            # Everything okay
            data_set[line_data[1]][sample_num] = line_data[2]
        else:
            print("Something went wrong")
            exit()

    data_fh.close()

    # Output file is the table to be loaded!
    out_fh = open('output.tsv', 'w')
    for k, v in data_set.items():
        out_fh.write(k)
        for x in v:
            out_fh.write("\t" + x)
        out_fh.write("\n")
    out_fh.close()


if __name__ == '__main__':
    main()
