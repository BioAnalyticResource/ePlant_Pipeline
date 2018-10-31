#!/usr/bin/python3
"""
This program extracts DNA sequences for Gene Info View.
Author: Asher
Date: October, 2018
Usage: python3 extract_DNA.py
Notes: Update file name before running.
"""

def main():
    chr_file = 'Slycopersicum_390_v2.5.fa'
    outfile = ''

    chr_fh = open(chr_file, 'r')

    for line in chr_fh:
        line = line.rstrip()

        # FASTA header found
        if line[0] == '>':

            # If outfile has a name, then this is not the first seq
            if outfile != '':
                outfh.write('\n')
                outfh.close()

            outfile = line[1:] + '.fas'
            outfh = open(outfile, 'w')
            continue
        else:
            outfh.write(line)

    chr_fh.close()
    outfh.write('\n')
    outfh.close()

if __name__ == '__main__':
    main()
