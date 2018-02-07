#!/usr/bin/python3
"""
This function returns pubmed publications meta data for a given pubmed id
Author: Asher
Date: February, 2018
Usage: python3 get_pubmed_data.py
"""
from sys import exit
from datetime import datetime

import urllib.request
import json
import re


def get_date(date):
    """
    This function returns year given a date
    :param date:
    :return: string year
    """
    full = datetime.strptime(date, '%Y/%m/%d %H:%M')
    return str(full.year)


def get_tair_data(publications):
    """
    Get publications from TAIR file
    :param publications:
    :return:
    """

    tair_file = 'Locus_Published_20161231.txt'

    try:
        fh = open(tair_file, 'r')
    except FileNotFoundError:
        print('TAIR_file does not exist!')
        exit(-1)

    for line in fh:
        line = line.rstrip()
        columns = line.split('\t')

        # Remove variants .1 etc
        try:
            agi = re.search('.+(AT[12345CM]G\d+)', columns[0], re.IGNORECASE).group(1).upper()
        except AttributeError:
            continue

        if agi in publications:
            if columns[2] in publications[agi]:
                pass
            else:
                publications[agi].append(columns[2])
        else:
            publications[agi] = []
            publications[agi].append(columns[2])

    fh.close()
    return publications


def get_agi_publication():
    """
    This function uses ncbi publications list
    :return:
    """

    lookups = ncbi_lookup_dictionary()
    publications = dict()
    pubmed_file = 'arabidopsis_gene2pubmed.tsv'

    try:
        fh = open(pubmed_file, 'r')
    except FileNotFoundError:
        print('gene2pubmed file does not exist!')
        exit(-1)

    for line in fh:
        line = line.rstrip()
        columns = line.split('\t')

        # Not Arabidopsis somehow.
        if columns[0] != '3702':
            continue

        if columns[1] in lookups:
            agi = lookups[columns[1]]
            if agi in publications:
                if columns[2] in publications[agi]:
                    pass
                else:
                    publications[agi].append(columns[2])
            else:
                publications[agi] = []
                publications[agi].append(columns[2])

    fh.close()

    # Now add TAIR data
    publications = get_tair_data(publications)

    return publications


def ncbi_lookup_dictionary():
    """
    Create a TAIR AGI to NCBI mapping
    :return:
    """
    lookup = dict()
    lookup_file = 'TAIR10_NCBI_REFSEQ_mapping_PROT'

    try:
        fh = open(lookup_file, 'r')
    except FileNotFoundError:
        print('Lookup file is not found')
        exit(-1)

    for line in fh:
        columns = line.split("\t")

        ncbi = columns[0].rstrip()
        tair = columns[2].rstrip()

        # Remove variants .1 etc
        try:
            agi = re.search('(AT[12345CM]G\d+)', tair, re.IGNORECASE).group(1)
        except AttributeError:
            print('RegEx problem')
            exit(-1)

        lookup[ncbi] = agi.upper()

    fh.close()
    return lookup


def query_ncbi(pubmed):
    """
    Get data from NCBI API
    :param pubmed:
    :return:
    """

    headers = dict()
    headers['User-Agent'] = 'BAR University of Toronto'

    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=' + pubmed + '&retmode=json&tool=ePlant'

    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        resp_decoded = resp.read().decode('utf-8')
        resp_json = json.JSONDecoder().decode(resp_decoded)

        data = dict()
        data['author'] = resp_json['result'][pubmed]['sortfirstauthor']
        data['date'] = get_date(resp_json['result'][pubmed]['sortpubdate'])
        data['journal'] = resp_json['result'][pubmed]['source']
        data['title'] = resp_json['result'][pubmed]['title']
        data['pubmed'] = pubmed

    except Exception:
        raise 

    return data


def get_existing_agis():
    """
    This function is using when connection to API timed out and program crashes.
    It is useful so we don't query genes that are already in the database.
    :return:
    """
    agis = []

    try:
        inputfile = open('pubmed_dump.tsv', 'r')
    except FileNotFoundError:
        print('No AGIs are present')
        inputfile.close()
        return agis

    for line in inputfile:
        line = line.rstrip()

        if line == "":
            continue

        columns = line.split('\t')

        if columns[0] in agis:
            continue

        agis.append(columns[0])

    print('Found {} AGIs'.format(len(agis)))
    inputfile.close()
    return agis


def save_data(publications):
    """
    This function gets data and save it.
    :param publications:
    :return:
    """

    # First get the array of downloaded AGIs
    agis_downloaded = get_existing_agis()

    # Save file, with 1 buffer size (auto flush)
    try:
        outfh = open('pubmed_dump.tsv', 'a', 1)
    except Exception:
        print('File to open output file!')
        exit(-1)

    # Get data for each k, v pair
    for agi, pubmeds in sorted(publications.items()):
        if agi in agis_downloaded:
            continue

        for pubmed in pubmeds:
            data = query_ncbi(pubmed)
            outfh.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(agi, data['author'], data['date'], data['journal'], data['title'], data['pubmed']))

    outfh.close()


def main():
    """
    The main function
    :return:
    """

    # Get a dictionary with list of pubmed ids for each agi
    publications = get_agi_publication()

    # Now query ncbi
    save_data(publications)


if __name__ == '__main__':
    main()
