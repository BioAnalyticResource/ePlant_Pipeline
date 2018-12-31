#!/usr/bin/python3
"""
This program process info files from phyre server
Author: Asher
Date: December, 2018
Usage: python3 processData.py
Notes: Make sure pdb files and summary file are in the same directory. Output is in processed directory
"""
import re
import os
import pandas as pd
from sys import exit, warnoptions
from shutil import copyfile
from Bio import SeqIO


def get_gene_id(data):
    """
    The gene names for summary file

    :param data: Description column of summaryinfo
    :return: gene id
    """
    # Regular expression replace
    match = re.search(r'ID=(Solyc\d+g\d+)\.', data, re.I)
    if match:
        return match.group(1)
    else:
        print('Regex Error in gene name: ' + data)
        exit(-1)


def get_template(data):
    """
    This function gets the template.

    :param data: full template data
    :return: 4 letter code
    """

    match = re.search(r'\s*.(....).', data, re.I)
    if match:
        return match.group(1)
    else:
        print('Regex Error in template name: ' + data)
        exit(-1)


def get_summary_table():
    """
    This function reads data from summaryinfo file and returns a python pandas object

    :return: python3 pandas table
    """

    try:
        data = pd.read_csv('summaryinfo', header=0, sep='|', names=['gene', 'file', 'template', 'confidence'], usecols=[0, 1, 2, 3], )
    except FileNotFoundError:
        print('Summary info file is not found!')
        exit(-1)

    # Remove spaces
    data['gene'] = data['gene'].apply(lambda x: x.strip())
    data['file'] = data['file'].apply(lambda x: x.strip())
    data['template'] = data['template'].apply(lambda x: x.strip())

    # Drop rows that don't have template
    data = data[data.template != '']    # This alone might not work
    data = data.dropna(subset=['confidence'])

    data['gene'] = data['gene'].apply(get_gene_id)
    data['template'] = data['template'].apply(get_template)

    return data


def prepare_files(data):
    """
    Prepare pdf files and FASTA files.
    Acknowledgement: http://www.bioinfopoint.com/index.php/code/41-extracting-the-sequence-from-a-protein-structure-using-biopython
    :param data: pandas data frame
    :return: None
    """

    # Disable warning in this function
    if not warnoptions:
        from warnings import simplefilter
        simplefilter('ignore')

    for index, row in data.iterrows():
        src = row['file'] + '.final.pdb'
        dst = 'processed/' + row['gene'] + '.pdb'
        fasta = 'processed/' + row['gene'] + '.fas'
        copyfile(src=src, dst=dst)

        try:
            file = open(src, 'rU')
        except FileNotFoundError:
            print('Pdb file is not found: ' + src)
            exit(-1)

        for record in SeqIO.parse(file, 'pdb-atom'):

            # Save data
            fasta_out = open(fasta, 'w')
            fasta_out.write('>' + row['gene'] + '\n' + str(record.seq) + '\n')
            fasta_out.close()

        file.close()


def save_file_for_db(data):
    """
    Save the file for db:

    :param data: Pandas data frame
    :return: None
    """

    data = data.drop(['file'], axis=1)
    data.to_csv('databasefile.tsv', sep='\t', header=True, index=False)


def main():
    """
    The main program.

    :return:
    """

    # Get the summary data
    summary = get_summary_table()

    # Check if directory exists
    if os.path.isdir('proccesed') or os.path.exists('processed'):
        pass
    else:
        os.mkdir('processed')

    # Copy pdf files and generate FASTA files
    prepare_files(summary)

    # Save the file for database upload
    save_file_for_db(summary)


if __name__ == '__main__':
    main()
