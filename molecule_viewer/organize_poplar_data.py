#!/usr/bin/python3
"""
This script organizes poplar files.
Author: Asher
Data: January 2019
Usage: Python3 organize_poplar_data.py
Notes: It also generates a file for databases upload
"""
import os
import re
import pandas as pd
from sys import exit, warnoptions
from shutil import copyfile
from Bio import SeqIO


def get_list(file):
    """
    This functions gets the list of genes

    :param file: file name
    :return: list of genes
    """
    genes = []

    try:
        f = open(file, 'r')
    except FileNotFoundError:
        print('Primary transcript file not found!')
        exit(-1)

    for line in f:
        # Grab the headers
        if '>' in line:
            columns = line.split(' ')
            gene = columns[3].replace('locus=', '')
            genes.append(gene)

        else:
            continue

    return genes


def get_model(directory):
    """
    This function get model data
    :param directory: path
    :return: template, file, confidence
    """

    details_file = directory + '/details.csv'
    try:
        data = pd.read_csv(details_file, header=0, sep='\t', names=['template', 'model', 'evalue', 'prob'], usecols=[1, 2, 4, 5])
    except FileNotFoundError:
        print(details_file + ' not found.')
        exit(-1)

    data = data.sort_values(by=['evalue', 'prob']).reset_index()

    # Get data for template
    template = str(data['template'][0])
    match = re.search(r'^(....)_.+', template, re.I)
    if match:
        template = match.group(1)
    else:
        print('Template did not match.')
        exit(-1)

    # Get data file name
    file_name = data['model'][0]

    # Confidence
    confidence = data['prob'][0]

    return template, file_name, confidence


def save_fasta(gene, directory, file_name):
    if not warnoptions:
        from warnings import simplefilter
        simplefilter('ignore')

    pdb_file = directory + '/' + file_name
    fasta = 'processed/' + gene + '.fas'

    try:
        file = open(pdb_file, 'rU')
    except FileNotFoundError:
        print('pdb file is not found: ' + pdb_file)
        exit(-1)

    for record in SeqIO.parse(file, 'pdb-atom'):
        fasta_out = open(fasta, 'w')
        fasta_out.write('>' + gene + '\n' + str(record.seq) + '\n')
        fasta_out.close()

    file.close()


def move_files(genes):

    # Open database file
    out_f = open('databasefile.tsv', 'w')

    for gene in genes:
        # See if the pdb file exists somewhere.
        # If exits, set the directory path for that gene
        directory = ''
        for i in range(20):
            if os.path.exists('../poplar/' + gene + '.' + str(i) + '.p'):
                directory = '../poplar/' + gene + '.' + str(i) + '.p'
                break

        # The pdb file for the gene does not exist.
        # Move on to the next
        if directory == '':
            continue

        # Get the model we are going to use in ePlant
        template, file_name, confidence = get_model(directory)

        # Move pdb file
        in_file_name = directory + '/' + file_name
        out_file_name = 'processed/' + gene + '.pdb'
        copyfile(src=in_file_name, dst=out_file_name)

        # Save fasta seq
        save_fasta(gene, directory, file_name)

        # Write gene, template and confidence
        out_f.write(gene + '\t' + template + '\t' + str(confidence) + '\n')

    out_f.close()


def main():
    """
    The main program.

    :return:
    """
    transcripts_file = 'Ptrichocarpa_210_v3.0.protein_primaryTranscriptOnly.fa'

    # Get the list of genes
    genes = get_list(transcripts_file)

    # Move the pdb files
    move_files(genes)


if __name__ == '__main__':
    main()
